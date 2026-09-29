"""Product image storage — files are saved on the server's own disk and served
back from /uploads (see server.py). No third-party service needed.

The database only stores a short relative path (Product.image_url), e.g.
    /uploads/products/3f9c...e1.jpg
so the site can be moved to another domain without touching any rows.
"""
import re
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import settings

UPLOAD_ROOT = Path(settings.upload_dir).resolve()
PRODUCT_IMAGE_DIR = UPLOAD_ROOT / "products"
PUBLIC_PREFIX = "/uploads/products/"
MAX_BYTES = settings.max_upload_mb * 1024 * 1024

# Files we create are always <32 hex chars>.<ext>, so anything else is rejected.
_LOCAL_RE = re.compile(r"^/uploads/products/[0-9a-f]{32}\.(jpg|png|gif|webp)$")
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


async def save_product_image(file: UploadFile) -> str:
    data = await file.read(MAX_BYTES + 1)
    if not data:
        raise HTTPException(400, "The uploaded file is empty.")
    if len(data) > MAX_BYTES:
        raise HTTPException(
            413,
            f"Image is too large (max {settings.max_upload_mb} MB).",
        )
    extension = _detect_extension(data[:16])
    if not extension:
        raise HTTPException(
            415,
            "Unsupported image type. Use JPG, PNG, WEBP or GIF.",
        )
    PRODUCT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    (PRODUCT_IMAGE_DIR / filename).write_bytes(data)
    return f"{PUBLIC_PREFIX}{filename}"


def _local_path(image_url: str) -> Path | None:
    if not _LOCAL_RE.match(image_url):
        return None
    return PRODUCT_IMAGE_DIR / image_url.rsplit("/", 1)[-1]


def is_valid_image_url(image_url: str | None) -> bool:
    """True for a file we uploaded (must exist) or a plain http(s) link."""
    if not image_url:
        return False
    path = _local_path(image_url)
    if path is not None:
        return path.is_file()
    return bool(_REMOTE_RE.match(image_url))


def delete_local_image(image_url: str | None) -> None:
    """Remove an uploaded file. External links and unknown paths are ignored."""
    if not image_url:
        return
    path = _local_path(image_url)
    if path is not None:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
