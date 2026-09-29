"""Product image storage — photos are saved INSIDE Postgres (table
`product_images`) and served back by GET /uploads/products/<id>.<ext>
(see app/routes/image_routes.py). No disk, no third-party service.

Product.image_url keeps a short relative path, e.g.
    /uploads/products/3f9c...e1.jpg
so the site can move to another domain without touching any rows.
"""
import io
import re
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy import delete, select
from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.database import SessionLocal
from app.models.image_model import ProductImage

PUBLIC_PREFIX = "/uploads/products/"
MAX_BYTES = settings.max_upload_mb * 1024 * 1024
MAX_DIMENSION = 1600          # longest side, in pixels, after optimisation
SKIP_OPTIMISE_UNDER = 400_000  # bytes: small files are stored untouched

CONTENT_TYPES = {
    "jpg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
}

# Images we create are always <32 hex chars>.<ext>, so anything else is rejected.
_LOCAL_RE = re.compile(r"^/uploads/products/([0-9a-f]{32})\.(jpg|png|gif|webp)$")
_REMOTE_RE = re.compile(r"^https?://[^\s]{4,490}$", re.IGNORECASE)


def _detect_extension(head: bytes) -> str | None:
    """Trust the file's real bytes, not the browser-supplied name/type."""
    if head.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if head[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return None


def _optimise(data: bytes, extension: str) -> bytes:
    """Shrink big phone photos before they go into the database (a 5 MB
    photo becomes roughly 200-400 KB). Any problem -> keep the original."""
    if extension == "gif" or len(data) <= SKIP_OPTIMISE_UNDER:
        return data
    try:
        from PIL import Image, ImageOps

        image = ImageOps.exif_transpose(Image.open(io.BytesIO(data)))
        image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
        out = io.BytesIO()
        if extension == "jpg":
            image.convert("RGB").save(out, "JPEG", quality=85, optimize=True)
        elif extension == "png":
            image.save(out, "PNG", optimize=True)
        else:
            image.save(out, "WEBP", quality=85)
        smaller = out.getvalue()
        return smaller if 0 < len(smaller) < len(data) else data
    except Exception:
        return data


def _store(data: bytes, extension: str) -> str:
    image_id = uuid.uuid4().hex
    db = SessionLocal()
    try:
        db.add(ProductImage(id=image_id, content_type=CONTENT_TYPES[extension], data=data))
        db.commit()
    finally:
        db.close()
    return f"{PUBLIC_PREFIX}{image_id}.{extension}"


async def save_product_image(file: UploadFile) -> str:
    data = await file.read(MAX_BYTES + 1)
    if not data:
        raise HTTPException(400, "The uploaded file is empty.")
    if len(data) > MAX_BYTES:
        raise HTTPException(413, f"Image is too large (max {settings.max_upload_mb} MB).")
    extension = _detect_extension(data[:16])
    if not extension:
        raise HTTPException(415, "Unsupported image type. Use JPG, PNG, WEBP or GIF.")

    def work() -> str:
        return _store(_optimise(data, extension), extension)

    return await run_in_threadpool(work)


def _local_id(image_url: str | None) -> str | None:
    match = _LOCAL_RE.match(image_url or "")
    return match.group(1) if match else None


def is_valid_image_url(image_url: str | None) -> bool:
    """True for an image we stored (must exist in the database) or a plain
    http(s) link."""
    if not image_url:
        return False
    image_id = _local_id(image_url)
    if image_id is not None:
        db = SessionLocal()
        try:
            return db.scalar(select(ProductImage.id).where(ProductImage.id == image_id)) is not None
        finally:
            db.close()
    return bool(_REMOTE_RE.match(image_url))


def delete_local_image(image_url: str | None) -> None:
    """Remove a stored image. External links and unknown paths are ignored."""
    image_id = _local_id(image_url)
    if image_id is None:
        return
    db = SessionLocal()
    try:
        db.execute(delete(ProductImage).where(ProductImage.id == image_id))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


def load_image(image_id: str) -> tuple[bytes, str] | None:
    db = SessionLocal()
    try:
        row = db.get(ProductImage, image_id)
        return (bytes(row.data), row.content_type) if row else None
    finally:
        db.close()
