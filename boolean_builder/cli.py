"""Command line:

    boolean "ml engineer" --must python pytorch --nice llm kubernetes --loc Chicago "New York"
    boolean --spec examples/senior_ml_engineer.json --json
"""
from __future__ import annotations

import argparse
import json

from .builder import Search, build_all


def _from_spec(path: str) -> Search:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return Search(
        titles=d["titles"], must_have=d.get("must_have", []), nice_to_have=d.get("nice_to_have", []),
        exclude=d.get("exclude", []), locations=d.get("locations", []), companies=d.get("companies", []),
        use_default_excludes=d.get("use_default_excludes", True), expand=d.get("expand", True),
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="boolean", description="Build Boolean sourcing strings for recruiters.")
    p.add_argument("titles", nargs="*", help='Job titles, e.g. "ml engineer"')
    p.add_argument("--must", nargs="*", default=[], help="Must-have skills (all required)")
    p.add_argument("--nice", nargs="*", default=[], help="Nice-to-have skills (any one)")
    p.add_argument("--exclude", nargs="*", default=[], help="Terms to exclude")
    p.add_argument("--loc", nargs="*", default=[], help="Locations (used in X-ray searches)")
    p.add_argument("--companies", nargs="*", default=[], help="Target companies, e.g. competitors")
    p.add_argument("--no-expand", action="store_true", help="Use titles and skills exactly as typed")
    p.add_argument("--no-default-excludes", action="store_true")
    p.add_argument("--spec", help="JSON file describing the search")
    p.add_argument("--json", action="store_true", help="Print JSON instead of text")
    a = p.parse_args(argv)

    if a.spec:
        s = _from_spec(a.spec)
    else:
        if not a.titles:
            p.error("give at least one title or --spec")
        s = Search(titles=a.titles, must_have=a.must, nice_to_have=a.nice, exclude=a.exclude,
                   locations=a.loc, companies=a.companies, expand=not a.no_expand,
                   use_default_excludes=not a.no_default_excludes)

    out = build_all(s)
    if a.json:
        print(json.dumps(out, indent=2))
        return 0
    labels = {"linkedin_recruiter": "LinkedIn Recruiter", "google_xray_linkedin": "Google X-ray (LinkedIn)",
              "github_xray": "GitHub X-ray"}
    for k, label in labels.items():
        print(f"\n{label}\n{'-' * len(label)}\n{out[k]}")
    for w in out["warnings"]:
        print(f"\n! {w}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
