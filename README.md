# boolean-search-builder

Build clean Boolean sourcing strings for **LinkedIn Recruiter**, **Google X-ray** and **GitHub X-ray** from a simple search brief: titles, must-have skills, nice-to-haves, locations, target companies and exclusions.

I'm a technical recruiter. Writing Boolean by hand is slow and easy to get wrong (a missing quote or parenthesis quietly breaks a search), and every platform has its own quirks. This tool handles the syntax and adds the title and skill synonyms recruiters usually forget, so you can spend your time on outreach instead.

![tests](https://github.com/heygvg-tech/boolean-search-builder/actions/workflows/ci.yml/badge.svg)

**[Try it live in your browser →](https://heygvg-tech.github.io/boolean-search-builder/)** (nothing to install). Source: [`docs/index.html`](docs/index.html).

## Example

```bash
boolean "ml engineer" --must python pytorch --nice llm kubernetes \
        --loc "New York" Brooklyn --companies Runway Pika "Luma AI" --exclude contract
```

```
LinkedIn Recruiter
("machine learning engineer" OR "ML engineer" OR "applied scientist" OR "AI engineer" OR "deep learning engineer")
AND Python AND PyTorch AND (LLM OR "large language models" OR GPT OR RAG OR Kubernetes OR K8s)
AND (Runway OR Pika OR "Luma AI") NOT (contract OR recruiter OR sourcer OR "talent acquisition" OR intern OR student)

Google X-ray (LinkedIn)
site:linkedin.com/in ("machine learning engineer" OR "ML engineer" OR "applied scientist" OR "AI engineer")
Python PyTorch ("New York" OR Brooklyn) (Runway OR Pika OR "Luma AI") -contract -recruiter -sourcer

GitHub X-ray
site:github.com "followers" "repositories" Python PyTorch ("New York" OR Brooklyn) -"jobs" -"topics"
```

## What it handles for you

- **Synonyms:** "ml engineer" expands to machine learning engineer, applied scientist, AI engineer and more; "kubernetes" adds K8s. Turn it off with `--no-expand`.
- **Correct quoting and grouping** for multi-word, hyphenated and dotted terms (`"Node.js"`, `"front-end developer"`).
- **Platform rules:** LinkedIn gets `AND`/`NOT`; Google X-ray drops `AND`, uses `-` exclusions and stays under Google's ~32-word limit.
- **Noise filters:** excludes recruiters, sourcers, interns and students by default.
- **Sanity warnings:** flags searches with no must-haves, too many must-haves, or strings that are too long.

## Install

```bash
pip install -e .
boolean --help
boolean --spec examples/senior_ml_engineer.json --json
```

Pure Python, no dependencies. Tests run in CI on every push (`pytest -q`).

## Layout

```
boolean_builder/
  builder.py    # string building for each platform + warnings
  synonyms.py   # title and skill synonym maps (easy to extend)
  cli.py        # `boolean` command
docs/index.html # browser version, same logic in JavaScript
examples/       # JSON search briefs
tests/
```

## Notes

Built with help from AI coding tools, then tested and tuned around how sourcing actually works. Contributions to the synonym lists are welcome.
