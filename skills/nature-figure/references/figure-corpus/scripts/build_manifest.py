"""Create a skeleton manifest for an NCS figure reference folder.

This helper inventories local reference images only. It does not verify
metadata, analyze content, or grant permission to reuse any figure.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".svg", ".pdf"}
FIELDS = [
    "reference_id",
    "local_path",
    "source_url",
    "paper_title",
    "doi",
    "venue",
    "year",
    "article_type",
    "figure_id",
    "figure_role",
    "archetype",
    "license_status",
    "metadata_status",
    "notes",
]


def iter_assets(input_dir: Path) -> list[Path]:
    return sorted(
        path for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an NCS reference figure manifest skeleton.")
    parser.add_argument("--input", required=True, help="Directory containing reference images/PDFs.")
    parser.add_argument("--output", required=True, help="CSV manifest path to write.")
    args = parser.parse_args()

    input_dir = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")

    assets = iter_assets(input_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for index, path in enumerate(assets, start=1):
            writer.writerow({
                "reference_id": f"ref_{index:04d}",
                "local_path": str(path),
                "source_url": "",
                "paper_title": "",
                "doi": "",
                "venue": "",
                "year": "",
                "article_type": "",
                "figure_id": "",
                "figure_role": "",
                "archetype": "",
                "license_status": "unknown",
                "metadata_status": "UNVERIFIED",
                "notes": "",
            })

    print(f"Wrote {len(assets)} references to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
