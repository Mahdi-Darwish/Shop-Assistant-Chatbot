import re
_INJECTION_PATTERNS = [
    r"ignore (all|any|the)? ?(previous|prior|above|earlier) instructions",
    r"forget (your|all|everything|previous) (instructions|knowledge|rules)",
    r"you are now",
    r"act as (a|an) (?!shop|coffee|barista)",
    r"new instructions",
    r"system prompt",
    r"developer mode",
    r"jailbreak",
    r"pretend (you're|you are|to be)",
    r"disregard (your|all|the) (rules|instructions|guidelines)",
    r"what (are|is) your (system prompt|instructions|rules)",
]
_COMPILED = [re.compile(p, re.IGNORECASE) for p in _INJECTION_PATTERNS]
def looks_like_injection_attempt(message: str) -> bool:
    return any(pattern.search(message) for pattern in _COMPILED)