"""Seeds baseline reference data (the product catalog) into a fresh
database. Safe to run every time the container starts — it checks first
and does nothing if products already exist, so it never duplicates rows
on a restart.
This is for REFERENCE/CATALOG data only (products). Never seed real user
data this way — users, carts, and orders should always start empty in any
new environment; only shared baseline data like a product catalog belongs
here.
"""
import pathlib
from sqlalchemy import text
from app.database import SessionLocal
from app.models.product_model import Product
SQL_FILE = pathlib.Path(__file__).resolve().parent.parent / "insert_products.sql"
def _extract_runnable_statements(sql_text: str) -> list[str]:
    """pg_dump output contains a lot we can't (and don't need to) run
    through a plain DB connection — comments, SET commands, and (in
    pg_dump 18+) \\restrict/\\unrestrict lines, which are psql-CLIENT-ONLY
    meta-commands, not valid SQL, and will error if executed directly.
    We only need the actual data: INSERT statements, and the sequence
    reset so future auto-generated ids don't collide with these seeded
    ones."""
    statements = []
    for line in sql_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("INSERT INTO") or stripped.upper().startswith(
            "SELECT PG_CATALOG.SETVAL"
        ):
            statements.append(stripped)
    return statements
def seed_products() -> None:
    db = SessionLocal()
    try:
        existing_count = db.query(Product).count()
        if existing_count > 0:
            print(f"Products table already has {existing_count} rows — skipping seed.")
            return
        if not SQL_FILE.exists():
            print(f"No seed file found at {SQL_FILE} — skipping seed.")
            return
        statements = _extract_runnable_statements(SQL_FILE.read_text())
        if not statements:
            print("Seed file had no runnable INSERT statements — skipping.")
            return
        for statement in statements:
            db.execute(text(statement))
        db.commit()
        print(f"Seeded product catalog ({len(statements)} statements executed).")
    finally:
        db.close()
if __name__ == "__main__":
    seed_products()