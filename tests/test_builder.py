from boolean_builder import Search, build_all, github_xray, google_xray, linkedin
from boolean_builder.builder import or_group, quote


def test_quote_multiword_and_dotted_terms():
    assert quote("machine learning engineer") == '"machine learning engineer"'
    assert quote("Node.js") == '"Node.js"'
    assert quote("Python") == "Python"
    assert quote('"already quoted"') == '"already quoted"'


def test_or_group_dedupes_case_insensitively():
    assert or_group(["SRE", "sre", "DevOps"]) == "(SRE OR DevOps)"
    assert or_group(["Python"]) == "Python"
    assert or_group([]) == ""


def test_linkedin_string_structure():
    s = Search(titles=["ml engineer"], must_have=["python", "pytorch"], nice_to_have=["llm"])
    q = linkedin(s)
    assert q.startswith('("machine learning engineer" OR "ML engineer"')
    assert " AND Python AND PyTorch AND (LLM OR " in q
    assert q.endswith('NOT (recruiter OR sourcer OR "talent acquisition" OR intern OR student)')


def test_no_expand_uses_terms_exactly():
    s = Search(titles=["Staff Engineer"], must_have=["Rust"], expand=False, use_default_excludes=False)
    assert linkedin(s) == '"Staff Engineer" AND Rust'


def test_google_xray_has_site_and_minus_excludes():
    s = Search(titles=["data engineer"], must_have=["spark"], locations=["Chicago"])
    q = google_xray(s)
    assert q.startswith("site:linkedin.com/in ")
    assert "Spark" in q and "Chicago" in q and '-recruiter' in q
    assert " AND " not in q  # Google ignores AND


def test_github_xray():
    q = github_xray(Search(titles=["backend engineer"], must_have=["go"], locations=["Austin"]))
    assert q.startswith('site:github.com "followers" "repositories"')
    assert "Golang" in q and "Austin" in q


def test_warnings_flag_thin_and_overloaded_searches():
    assert any("No must-have" in w for w in build_all(Search(titles=["software engineer"]))["warnings"])
    heavy = Search(titles=["software engineer"], must_have=["python", "aws", "react", "postgres", "kubernetes"])
    assert any("More than 4" in w for w in build_all(heavy)["warnings"])
