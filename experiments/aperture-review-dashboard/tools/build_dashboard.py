"""Rebuild the standalone HTML from the tracked template, script and snapshot."""

import argparse
import base64
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def render() -> str:
    script = (ROOT / "src/dashboard.js").read_text(encoding="utf-8")
    data = (ROOT / "data/snapshot.json").read_text(encoding="utf-8")
    template = (ROOT / "src/shell.html").read_text(encoding="utf-8")
    escaped_data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    signature = base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode("ascii")
    for marker in ("__DATASET__", "__SCRIPT__", "__SCRIPT_HASH__"):
        if template.count(marker) != 1:
            raise SystemExit(f"Invalid template: expected one {marker}")
    return (template.replace("__DATASET__", escaped_data)
                    .replace("__SCRIPT__", script)
                    .replace("__SCRIPT_HASH__", "'sha256-" + signature + "'"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Verify checked-in HTML equals regenerated output")
    args = parser.parse_args()
    target = ROOT / "index.html"
    output = render()
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != output:
            raise SystemExit("Dashboard differs from source; run python tools/build_dashboard.py")
        print("Build reproducibility: PASS")
    else:
        target.write_text(output, encoding="utf-8")
        print("Updated index.html")


if __name__ == "__main__":
    main()
