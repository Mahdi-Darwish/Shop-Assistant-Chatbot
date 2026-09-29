"""Turns tool results into small "cards" (product photos, cart / order
receipts) that the chat UI renders under the assistant's text reply.

Why this exists: the LLM only writes text. Rather than trusting it to copy
image URLs correctly, we watch what the tools returned and attach the images
ourselves. image_url is stripped from what the LLM sees (strip_image_urls),
so it can never print, mangle, or invent a link.
"""
import json
import re
from typing import Any

PRODUCT_LIST_TOOLS = {
    "get_products",
    "search_product_by_name",
    "get_products_by_max_price",
    "get_products_by_min_price",
    "list_products",  # admin
}
SINGLE_PRODUCT_TOOLS = {"add_to_cart", "add_product", "update_product"}
MAX_PRODUCT_CARDS = 8


def strip_image_urls(obj: Any) -> Any:
    """Copy of a tool result with every 'image_url' key removed."""
    if isinstance(obj, dict):
        return {k: strip_image_urls(v) for k, v in obj.items() if k != "image_url"}
    if isinstance(obj, list):
        return [strip_image_urls(v) for v in obj]
    return obj


def load_cards(raw: str | None) -> dict | None:
    if not raw:
        return None
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except (ValueError, TypeError):
        return None


def _norm(text: str | None) -> str:
    return re.sub(r"[\s\-_]+", " ", (text or "").lower()).strip()


def _mentioned(name: str, reply_norm: str) -> bool:
    n = _norm(name)
    if not n:
        return False
    return re.search(rf"(?<!\w){re.escape(n)}(?!\w)", reply_norm) is not None


def _product_card(p: dict) -> dict:
    return {
        "id": p.get("id"),
        "name": p.get("name"),
        "price": p.get("price"),
        "image_url": p.get("image_url"),
    }


def _cart_item(i: dict) -> dict:
    return {
        "name": i.get("product_name") or i.get("name"),
        "quantity": i.get("quantity"),
        "unit_price": i.get("unit_price"),
        "subtotal": i.get("subtotal"),
        "image_url": i.get("image_url"),
    }


class CardCollector:
    """Create one per chat request, call collect() after every tool call,
    then build(reply) once the final reply is known."""

    def __init__(self) -> None:
        self._products: dict[int, dict] = {}
        self._specific: list[int] = []
        self._cart: dict | None = None

    def collect(self, tool_name: str, result: Any) -> None:
        try:
            self._collect(tool_name, result)
        except Exception:
            # Cards are a nicety — never let them break a chat reply.
            pass

    def _add_product(self, p: Any, specific: bool) -> None:
        if not isinstance(p, dict) or p.get("id") is None or not p.get("name"):
            return
        self._products[p["id"]] = _product_card(p)
        if specific and p["id"] not in self._specific:
            self._specific.append(p["id"])

    def _collect(self, tool_name: str, result: Any) -> None:
        if isinstance(result, dict) and result.get("error"):
            return
        if tool_name in PRODUCT_LIST_TOOLS and isinstance(result, list):
            for p in result:
                self._add_product(p, specific=(tool_name == "search_product_by_name"))
        elif tool_name in SINGLE_PRODUCT_TOOLS and isinstance(result, dict):
            self._add_product(result.get("product"), specific=True)
        elif tool_name == "view_cart" and isinstance(result, dict):
            items = [_cart_item(i) for i in result.get("items", [])]
            if items:
                self._cart = {"kind": "cart", "items": items, "total": result.get("total")}
        elif tool_name == "checkout_cart" and isinstance(result, dict) and result.get("order_id"):
            self._cart = {
                "kind": "order",
                "order_id": result.get("order_id"),
                "items": [_cart_item(i) for i in result.get("items", [])],
                "total": result.get("total_price"),
            }

    def build(self, reply: str | None) -> dict | None:
        cards: dict = {}
        if self._cart:
            cards["cart"] = self._cart
        else:
            reply_norm = _norm(reply)
            shown = [c for c in self._products.values() if _mentioned(c["name"], reply_norm)]
            if not shown:
                # Reply may be in another language / paraphrased: fall back to
                # the specific items the tools actually looked up.
                shown = [self._products[i] for i in self._specific if i in self._products]
            if shown:
                cards["products"] = shown[:MAX_PRODUCT_CARDS]
        return cards or None
