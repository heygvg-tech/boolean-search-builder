"""Title and skill synonyms recruiters use to widen a search without losing precision."""

TITLES = {
    "software engineer": ["software engineer", "software developer", "SWE", "backend engineer", "full stack engineer"],
    "frontend engineer": ["frontend engineer", "front end engineer", "front-end developer", "UI engineer", "React developer"],
    "backend engineer": ["backend engineer", "back end engineer", "server engineer", "API engineer"],
    "ml engineer": ["machine learning engineer", "ML engineer", "applied scientist", "AI engineer", "deep learning engineer"],
    "data scientist": ["data scientist", "applied scientist", "research scientist", "quantitative analyst"],
    "data engineer": ["data engineer", "analytics engineer", "ETL developer", "big data engineer"],
    "devops engineer": ["devops engineer", "site reliability engineer", "SRE", "platform engineer", "infrastructure engineer"],
    "security engineer": ["security engineer", "application security engineer", "cloud security engineer", "AppSec engineer"],
    "engineering manager": ["engineering manager", "software engineering manager", "head of engineering", "director of engineering"],
    "product manager": ["product manager", "senior product manager", "technical product manager", "group product manager"],
    "product designer": ["product designer", "UX designer", "UI/UX designer", "interaction designer"],
    "embedded engineer": ["embedded engineer", "firmware engineer", "embedded software engineer", "embedded systems engineer"],
    "account executive": ["account executive", "AE", "enterprise account executive", "sales executive"],
    "solutions engineer": ["solutions engineer", "sales engineer", "solutions architect", "pre-sales engineer"],
}

SKILLS = {
    "python": ["Python"],
    "javascript": ["JavaScript", "TypeScript", "Node.js"],
    "typescript": ["TypeScript"],
    "react": ["React", "React.js", "ReactJS"],
    "go": ["Golang", '"Go developer"'],
    "kubernetes": ["Kubernetes", "K8s"],
    "aws": ["AWS", "Amazon Web Services"],
    "gcp": ["GCP", "Google Cloud"],
    "pytorch": ["PyTorch"],
    "tensorflow": ["TensorFlow"],
    "llm": ["LLM", "large language models", "GPT", "RAG"],
    "terraform": ["Terraform"],
    "postgres": ["Postgres", "PostgreSQL"],
    "spark": ["Spark", "PySpark"],
}

# Common noise when searching for individual contributors at the right level
DEFAULT_EXCLUDES = ["recruiter", "sourcer", "talent acquisition", "intern", "student"]


def expand_title(title: str) -> list[str]:
    return TITLES.get(title.strip().lower(), [title.strip()])


def expand_skill(skill: str) -> list[str]:
    return SKILLS.get(skill.strip().lower(), [skill.strip()])
