"""
Why did the AI place an order after the customer said "thanks"?

This script replays that moment against the REAL model (Groq) many times and
counts what it does, under different set-ups, so we can see which ingredient
caused it:

  A  the OLD set-up you had when it happened (old prompt + checkout tool)
  B  old set-up, but without the sentence "...unless a checkout tool call succeeded"
  C  the FIRST fix wording (rules added), checkout tool still offered
  D  old prompt, but NO checkout tool
  E  today's fix: current prompt + no tools at all for "thanks"
  F  current (refined) prompt, no checkout tool, tools offered  (the prompt on its own, without the "thanks" guard)

SAFE: it never runs a tool and never writes to the database. It only asks the
model "what would you do?" and records the answer. Orders cannot be created.

Run from the project folder (the same place you run alembic / uvicorn):

    python3 -m scripts.debug_thanks_bug                      # built-in history, 10 runs each
    python3 -m scripts.debug_thanks_bug --runs 20 --show 2   # more runs, print 2 raw answers per variant
    python3 -m scripts.debug_thanks_bug --message "ok"       # try another last message
    python3 -m scripts.debug_thanks_bug --conversation 12    # replay the REAL chat from your database (read-only)
"""
import argparse
import collections
import json
import re
import time

from openai import OpenAI

from app.core.config import settings
from app.routes import chat_routes
from app.tools_schema import tools as CURRENT_TOOLS

MODEL = chat_routes.MODEL_NAME

CHECKOUT_TOOL = {
    "type": "function",
    "function": {
        "name": "checkout_cart",
        "description": "Place an order from everything currently in the current user's active cart.",
        "parameters": {"type": "object", "properties": {}},
    },
}

# --- the prompts -------------------------------------------------------------------------------
NEW_PROMPT = chat_routes.SYSTEM_PROMPT
NEW_BULLET = (
    "- After you add something to the cart, the app shows the cart with Checkout and Add-more buttons "
    "under your reply. You may ask if they'd like to check out or add more items, but never tell them "
    "to type a command\n"
)
OLD_BULLET = NEW_BULLET.rstrip("\n") + ", and never say an order was placed unless a checkout tool call succeeded\n"
assert NEW_BULLET in NEW_PROMPT, "prompt text changed - update NEW_BULLET in this script"
OLD_PROMPT = re.sub(r"ORDERS AND ACTIONS:.*?(?=If the user asks for multiple)", "", NEW_PROMPT, flags=re.S)
OLD_PROMPT = OLD_PROMPT.replace(NEW_BULLET, OLD_BULLET)
OLD_PROMPT_NO_SENTENCE = OLD_PROMPT.replace(OLD_BULLET, NEW_BULLET)

# the wording of the first fix (kept so variant C can still be re-run)
FIRST_FIX_BLOCK = """ORDERS AND ACTIONS:
- You CANNOT place orders. The customer places an order by pressing the
  Checkout button the app shows under their cart. If they ask to check
  out or confirm their order, show their cart (view_cart) and tell them
  to press the Checkout button. Never say an order was placed or
  confirmed — the app confirms orders itself.
- Act ONLY on the customer's latest message. Never repeat or redo
  something from earlier in the conversation (adding items, ordering)
  unless the latest message clearly asks for it again.
- If the latest message is only thanks, a greeting or small talk, reply
  briefly and warmly in their language, and do not use any tools.

"""
FIRST_FIX_PROMPT = OLD_PROMPT_NO_SENTENCE.replace("If the user asks for multiple", FIRST_FIX_BLOCK + "If the user asks for multiple", 1)

TOOLS_WITH_CHECKOUT = list(CURRENT_TOOLS) + [CHECKOUT_TOOL]
TOOLS_WITHOUT_CHECKOUT = [t for t in CURRENT_TOOLS if t["function"]["name"] != "checkout_cart"]

# (name, system prompt, tools offered or None for "no tools at all")
VARIANTS = [
    ("A  OLD set-up (what you had)", OLD_PROMPT, TOOLS_WITH_CHECKOUT),
    ("B  old, minus the 'tool call succeeded' sentence", OLD_PROMPT_NO_SENTENCE, TOOLS_WITH_CHECKOUT),
    ("C  first fix wording, checkout tool still offered", FIRST_FIX_PROMPT, TOOLS_WITH_CHECKOUT),
    ("D  old prompt, NO checkout tool", OLD_PROMPT, TOOLS_WITHOUT_CHECKOUT),
    ("E  today's fix (no tools for 'thanks')", NEW_PROMPT, None),
    ("F  refined prompt alone, no checkout tool", NEW_PROMPT, TOOLS_WITHOUT_CHECKOUT),
]

# --- the conversation as the model saw it -------------------------------------------------------
BUILT_IN_HISTORY = [
    {"role": "user", "content": "add an iced coffee latte"},
    {"role": "assistant", "content": "Added 1 x Iced Coffee Latte to your cart."},
    {"role": "user", "content": "and a cappuccino"},
    {"role": "assistant", "content": "Added 1 x Cappuccino to your cart. Would you like to check out or add more items?"},
    {"role": "user", "content": "Checkout"},
    {
        "role": "assistant",
        "content": "Thank you for your order! Your order #9 totals $7.50, and we'll keep you updated right here as it progresses.",
    },
]


def history_from_database(conversation_id: int, last_message: str):
    """Real messages of one conversation, cut right after the customer's `last_message`. Read-only."""
    from app.database import SessionLocal
    from app.models.chat_model import ChatMessage

    db = SessionLocal()
    try:
        rows = (
            db.query(ChatMessage)
            .filter(ChatMessage.conversation_id == conversation_id)
            .order_by(ChatMessage.created_at, ChatMessage.id)
            .all()
        )
    finally:
        db.close()
    msgs = [{"role": m.role, "content": m.content} for m in rows]
    cut = None
    for i, m in enumerate(msgs):
        if m["role"] == "user" and m["content"].strip().lower().startswith(last_message.strip().lower()):
            cut = i  # keep the LAST matching one
    if cut is None:
        raise SystemExit(f"No customer message starting with {last_message!r} in conversation {conversation_id}")
    return msgs[max(0, cut - 20):cut]  # the app sends the last 20 messages


def ask(client, system_prompt, tools, history, message):
    kwargs = {}
    if tools is not None:
        kwargs["tools"] = tools
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt}, *history, {"role": "user", "content": message}],
        temperature=0.2,
        **kwargs,
    )
    return response.choices[0].message


def describe(message):
    """(list of 'tool(args)', reasoning text or None, reply text) for one model answer."""
    calls = [f"{c.function.name}({c.function.arguments})" for c in (message.tool_calls or [])]
    reasoning = getattr(message, "reasoning", None) or getattr(message, "reasoning_content", None)
    return calls, reasoning, message.content


def run(client, args, history):
    args.only = getattr(args, "only", None)
    print(f"\nModel: {MODEL}   last message: {args.message!r}   runs per variant: {args.runs}")
    print(f"History sent ({len(history)} earlier messages):")
    for m in history[-6:]:
        print(f"   {m['role']:>9}: {m['content'][:90]}")
    summary = []
    for name, prompt, tools in VARIANTS:
        if args.only and name[0].upper() not in [x.upper() for x in args.only]:
            continue
        used = 0
        tool_counter = collections.Counter()
        shown = 0
        for _ in range(args.runs):
            try:
                message = ask(client, prompt, tools, history, args.message)
            except Exception as exc:  # rate limit etc.
                print(f"   (call failed: {exc})")
                time.sleep(2)
                continue
            calls, reasoning, reply = describe(message)
            if calls:
                used += 1
                for c in calls:
                    tool_counter[c.split("(")[0]] += 1
            if shown < args.show and calls:
                shown += 1
                print(f"\n--- {name}: the model asked for tools ---")
                print("   tool calls:", calls)
                print("   reasoning :", (reasoning or "(the API did not return its reasoning)")[:1500])
            time.sleep(0.4)
        summary.append((name, used, args.runs, dict(tool_counter)))
    print("\n=================  RESULT: how often did it try to use tools after the message?  =================")
    for name, used, total, counter in summary:
        bar = "#" * used + "." * (total - used)
        print(f"{name:<52} {used:>2}/{total:<2} [{bar}]  {counter if counter else ''}")
    print(
        "\nHow to read it:\n"
        "  A high, B high  -> the old messages/pattern alone make it repeat itself\n"
        "  A high, B low   -> my sentence 'never say an order was placed unless a tool call succeeded' caused it\n"
        "  C high          -> the first fix wording is not enough (the model 'corrects' the history, e.g. by calling view_cart)\n"
        "  F low           -> the refined prompt stops that reaction even without the code guard\n"
        "  D low           -> without the checkout tool it cannot order at all\n"
        "  E 0/N           -> with today's fix it cannot happen\n"
        "It is random, so a single run proves nothing: look at the counts."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", nargs="+", help="run only these variants, e.g. --only F E")
    parser.add_argument("--runs", type=int, default=10, help="times to ask the model per variant (default 10)")
    parser.add_argument("--show", type=int, default=1, help="print this many raw tool-call answers per variant")
    parser.add_argument("--message", default="thanks", help="the customer's last message (default: thanks)")
    parser.add_argument("--conversation", type=int, help="replay the real history of this conversation id (read-only)")
    args = parser.parse_args()
    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=settings.groq_api_key)
    history = history_from_database(args.conversation, args.message) if args.conversation else BUILT_IN_HISTORY
    run(client, args, history)


if __name__ == "__main__":
    main()
