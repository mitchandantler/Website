import csv
import io
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

from .models import DietaryTag, MenuCategory, MenuItem

REQUIRED_COLUMNS = {"category", "name", "price"}
TRUE_VALUES = {"true", "yes", "y", "1"}


@dataclass
class MenuImportResult:
    created: int = 0
    updated: int = 0
    errors: list[str] = field(default_factory=list)


def _parse_dietary_tags(raw: str) -> list[DietaryTag]:
    tag_names = [t.strip() for t in raw.replace(";", ",").split(",") if t.strip()]
    tags = []
    for tag_name in tag_names:
        tag = DietaryTag.objects.filter(name__iexact=tag_name).first()
        if not tag:
            tag = DietaryTag.objects.create(name=tag_name)
        tags.append(tag)
    return tags


# Magic-number prefixes for common non-CSV files someone might upload by
# mistake (e.g. a real Excel workbook, or the menu PDF itself) — checked so
# we can give a specific, friendly error instead of a decode crash.
_BINARY_SIGNATURES = {
    b"PK\x03\x04": "an Excel (.xlsx) or Word file",
    b"%PDF": "a PDF file",
    b"\xff\xd8\xff": "a JPEG image",
    b"\x89PNG": "a PNG image",
}


def _decode_csv_bytes(raw: bytes) -> str:
    """Decode uploaded CSV bytes, tolerating the encodings real-world CSV
    exports actually show up in (Excel/Numbers rarely export plain UTF-8).

    Tries UTF-8 (with/without a BOM) first, then Windows-1252 (the most
    common Excel default), then falls back to Latin-1 — which maps every
    single byte to a character and therefore can never raise — so a bad
    encoding degrades to odd-looking characters in one field rather than a
    hard crash.
    """
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")


def import_menu_csv(csv_file) -> MenuImportResult:
    """Bulk create/update MenuItems from an uploaded CSV.

    Expected columns: category, name, price (required), description,
    dietary_tags, is_available, display_order (optional). Rows are matched
    on (category, name) — a matching existing item is updated, otherwise a
    new one is created — so re-uploading an edited CSV is always safe.
    `category` must match an existing MenuCategory name (case-insensitive);
    it is never auto-created, since guessing its food/drink type would be
    unreliable.

    Every imported row (created or updated) is saved with `is_approved=False`
    — the admin dashboard is the single source of truth for what's actually
    live on the website, so nothing from a CSV reaches the public Menu page
    until a staff member reviews it (including its dietary tags) and
    approves it in Django Admin.
    """
    result = MenuImportResult()

    raw = csv_file.read()
    for signature, file_kind in _BINARY_SIGNATURES.items():
        if raw.startswith(signature):
            result.errors.append(
                f"This looks like {file_kind}, not a CSV. Please export/save "
                "it as CSV (plain text, comma-separated) and upload that "
                "instead."
            )
            return result

    reader = csv.DictReader(io.StringIO(_decode_csv_bytes(raw)))

    if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(
        {f.strip().lower() for f in reader.fieldnames}
    ):
        result.errors.append(
            "CSV must include these column headers: category, name, price"
        )
        return result

    for row_number, raw_row in enumerate(reader, start=2):  # row 1 is the header
        row = {
            (k or "").strip().lower(): (v or "").strip()
            for k, v in raw_row.items()
        }

        category_name = row.get("category", "")
        name = row.get("name", "")
        price_raw = row.get("price", "")

        if not category_name or not name or not price_raw:
            result.errors.append(
                f"Row {row_number}: category, name, and price are all "
                "required — row skipped."
            )
            continue

        category = MenuCategory.objects.filter(name__iexact=category_name).first()
        if not category:
            result.errors.append(
                f"Row {row_number}: no Menu Category named "
                f"'{category_name}' — row skipped. Create the category "
                "first, or check spelling."
            )
            continue

        try:
            price = Decimal(price_raw)
        except InvalidOperation:
            result.errors.append(
                f"Row {row_number}: invalid price '{price_raw}' — row skipped."
            )
            continue

        try:
            display_order = int(row.get("display_order") or 0)
        except ValueError:
            display_order = 0

        is_available = row.get("is_available", "true").lower() in TRUE_VALUES

        item, created = MenuItem.objects.update_or_create(
            category=category,
            name=name,
            defaults={
                "description": row.get("description", ""),
                "price": price,
                "is_available": is_available,
                "display_order": display_order,
                "is_approved": False,
            },
        )

        tags_raw = row.get("dietary_tags", "")
        if tags_raw:
            item.dietary_tags.set(_parse_dietary_tags(tags_raw))

        if created:
            result.created += 1
        else:
            result.updated += 1

    return result
