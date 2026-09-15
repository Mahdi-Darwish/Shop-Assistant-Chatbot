import pathlib
from sqlalchemy import text
from app.database import SessionLocal
from app.models.product_model import Product
SQL_FILE = pathlib.Path(__file__).resolve().parent.parent / "insert_products.sql"
def _extract_runnable_statements(sql_text: str) -> list[str]:
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