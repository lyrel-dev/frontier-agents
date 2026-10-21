"""Check the self-contained publication's data and generated HTML."""

import hashlib
import json
import sys

from build_dashboard import ROOT, render


def main() -> None:
    snapshot = json.loads((ROOT / "data/snapshot.json").read_text(encoding="utf-8"))
    fingerprint = snapshot.pop("fingerprint")
    raw = json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    assert hashlib.sha256(raw.encode("utf-8")).hexdigest() == fingerprint, "Dataset fingerprint mismatch"
    snapshot["fingerprint"] = fingerprint

    for collection in ("metrics", "alarms", "queries", "sops", "decisions", "documents"):
        items = snapshot[collection]
        assert isinstance(items, list) and items, f"Missing {collection} records"
        assert len({x["id"] for x in items}) == len(items), f"Duplicate {collection} ids"

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert html == render(), "Regenerated HTML differs"
    assert "connect-src 'none'" in html, "Unexpected network capability"
    assert "<script src=" not in html, "Unexpected remote script source"
    for file in (
        "documentation/Aperture-Consolidated-Documentation.html",
        "documentation/Aperture-Operational-Review.html",
        "documentation/Decision-Register.html",
    ):
        assert (ROOT / file).is_file(), f"Missing supporting document: {file}"
    print("Data integrity, unique IDs, reproducible build, CSP and primary source pages: PASS")
    print("Note: Other C2 historical source links require the separately distributed complete C2 package")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError, KeyError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
