import csv
import json
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent / "Generated User Agents"

CSV_FIELDS = ["id", "browser", "version", "os", "device", "ua"]


def get_unique_path(path):
    path = Path(path)

    if not path.exists():
        return path

    counter = 1

    while True:
        candidate = path.with_name(
            f"{path.stem} ({counter}){path.suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1


def export_records(records, format_name="txt", output=None):

    format_name = format_name.lower()

    if format_name not in {"txt", "json", "csv"}:
        raise ValueError("Choose txt, json, or csv.")

    records = list(records)

    if format_name == "txt":
        content = "\n".join(record["ua"] for record in records)
        if content:
            content += "\n"

    elif format_name == "json":
        content = json.dumps(
            records,
            indent=2,
            ensure_ascii=False,
        ) + "\n"

    else:
        content = None

    if output is None:
        if format_name in {"txt", "json"}:
            sys.stdout.write(content)
        else:
            writer = csv.DictWriter(
                sys.stdout,
                fieldnames=CSV_FIELDS,
                extrasaction="ignore",
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(records)

        return

    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    requested_path = Path(output)

    if not requested_path.is_absolute():
        requested_path = OUTPUT_DIR / requested_path

    requested_path.parent.mkdir(parents=True, exist_ok=True)

    destination = get_unique_path(requested_path)

    if format_name in {"txt", "json"}:
        destination.write_text(content, encoding="utf-8")

    else:
        with destination.open(
            "w",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=CSV_FIELDS,
                extrasaction="ignore",
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(records)

    print(f"Exported {len(records)} profile(s) to {destination}")
