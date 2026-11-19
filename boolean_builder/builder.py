"""Build Boolean search strings for LinkedIn Recruiter, Google X-ray and GitHub X-ray."""
from __future__ import annotations

from dataclasses import dataclass, field

from .synonyms import DEFAULT_EXCLUDES, expand_skill, expand_title

# LinkedIn Recruiter keyword boxes get unreliable on very long queries
LINKEDIN_SOFT_LIMIT = 1000
GOOGLE_MAX_WORDS = 32


@dataclass
class Search:
    titles: list[str]
    must_have: list[str] = field(default_factory=list)       # every one of these groups is required
    nice_to_have: list[str] = field(default_factory=list)    # at least one of these
    exclude: list[str] = field(default_factory=list)
    locations: list[str] = field(default_factory=list)
    companies: list[str] = field(default_factory=list)       # e.g. competitors to target
    use_default_excludes: bool = True
    expand: bool = True


def quote(term: str) -> str:
    term = term.strip()
    if term.startswith('"') and term.endswith('"'):
        return term
    return f'"{term}"' if (" " in term or "-" in term or "/" in term or "." in term) else term


def or_group(terms: list[str]) -> str:
    seen, out = set(), []
    for t in terms:
        q = quote(t)
        if q.lower() not in seen:
            seen.add(q.lower())
            out.append(q)
    if not out:
        return ""
    return out[0] if len(out) == 1 else "(" + " OR ".join(out) + ")"


def _titles(s: Search) -> list[str]:
    if not s.expand:
        return s.titles
    return [t for title in s.titles for t in expand_title(title)]


def _skill_groups(skills: list[str], expand: bool) -> list[str]:
    return [or_group(expand_skill(k) if expand else [k]) for k in skills]


def _excludes(s: Search) -> list[str]:
    ex = list(s.exclude) + (DEFAULT_EXCLUDES if s.use_default_excludes else [])
    seen, out = set(), []
    for e in ex:
        if e.lower() not in seen:
            seen.add(e.lower())
            out.append(e)
    return out


def linkedin(s: Search) -> str:
    """Keyword string for LinkedIn Recruiter's Boolean keyword field."""
    parts = [or_group(_titles(s))]
    parts += _skill_groups(s.must_have, s.expand)
    if s.nice_to_have:
        parts.append(or_group([t for k in s.nice_to_have for t in (expand_skill(k) if s.expand else [k])]))
    if s.companies:
        parts.append(or_group(s.companies))
    q = " AND ".join(p for p in parts if p)
    ex = _excludes(s)
    if ex:
        q += " NOT " + or_group(ex)
    return q


def google_xray(s: Search, site: str = "linkedin.com/in") -> str:
    """Google X-ray search of public profiles. Google ignores AND and caps queries near 32 words,
    so this keeps titles to the top few synonyms and skips nice-to-haves."""
    titles = _titles(s)[:4]
    parts = [f"site:{site}", or_group(titles)]
    parts += [quote(expand_skill(k)[0] if s.expand else k) for k in s.must_have]
    if s.locations:
        parts.append(or_group(s.locations))
    if s.companies:
        parts.append(or_group(s.companies[:3]))
    parts += [f"-{quote(e)}" for e in _excludes(s)[:3]]
    return " ".join(p for p in parts if p)


def github_xray(s: Search) -> str:
    """Google X-ray for GitHub profiles: surfaces engineers by language and location."""
    parts = ["site:github.com", '"followers"', '"repositories"']
    parts += [quote(expand_skill(k)[0] if s.expand else k) for k in s.must_have]
    if s.locations:
        parts.append(or_group(s.locations))
    parts += ['-"jobs"', '-"topics"']
    return " ".join(parts)


def warnings(s: Search) -> list[str]:
    out = []
    li = linkedin(s)
    if len(li) > LINKEDIN_SOFT_LIMIT:
        out.append(f"LinkedIn string is {len(li)} characters; consider trimming synonyms (soft limit {LINKEDIN_SOFT_LIMIT}).")
    words = len(google_xray(s).replace("(", " ").replace(")", " ").split())
    if words > GOOGLE_MAX_WORDS:
        out.append(f"Google X-ray has about {words} words; Google ignores terms past ~{GOOGLE_MAX_WORDS}.")
    if not s.must_have:
        out.append("No must-have skills: results will be broad. Add one or two core skills.")
    if len(s.must_have) > 4:
        out.append("More than 4 must-haves usually shrinks the pool too far. Move some to nice-to-have.")
    return out


def build_all(s: Search) -> dict[str, object]:
    return {
        "linkedin_recruiter": linkedin(s),
        "google_xray_linkedin": google_xray(s),
        "github_xray": github_xray(s),
        "warnings": warnings(s),
    }
