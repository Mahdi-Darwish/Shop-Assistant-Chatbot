import re

from fastapi import APIRouter, HTTPException, Response

from app.core.rate_limit import limiter
from app.services.image_services import load_image

router = APIRouter(tags=["images"])

_NAME_RE = re.compile(r"^([0-9a-f]{32})\.(jpg|png|gif|webp)$")


@router.get("/uploads/products/{filename}")
@limiter.exempt
def get_product_image(filename: str):
    """Public: serves a product photo stored in Postgres. Photos never
    change once created (every upload gets a new random name), so browsers
    may cache them for a year — repeat visits don't hit the server."""
    match = _NAME_RE.match(filename)
    found = load_image(match.group(1)) if match else None
    if not found:
        raise HTTPException(status_code=404, detail="Image not found")
    data, content_type = found
    return Response(
        content=data,
        media_type=content_type,
        headers={
            "Cache-Control": "public, max-age=31536000, immutable",
            "X-Content-Type-Options": "nosniff",
        },
    )
