"""Maintained offline checks; not part of the frozen generation methods."""
import csv
import io


def require(condition, message):
    if not condition:
        raise ValueError(str(message))


def csv_text(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def check_or_write(root, outputs, write=False):
    """Compare by default; explicit regeneration preserves existing newlines."""
    for name, expected in outputs.items():
        path = root / name
        normalized = expected.replace("\r\n", "\n")
        if write:
            existing = path.read_bytes() if path.exists() else b""
            newline = "\r\n" if b"\r\n" in existing else "\n"
            path.write_bytes(normalized.replace("\n", newline).encode("utf-8"))
        else:
            require(path.read_text(encoding="utf-8") == normalized,
                    f"{name}: retained derived output differs; no files were written. Inspect the difference before using --write.")
