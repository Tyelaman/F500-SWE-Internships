import re

KEYWORDS = {
    "Python": (r"python",),
    "Java": (r"java(?!script)",),
    "C": (r"c language",),
    "C++": (r"c\+\+",),
    "C#": (r"c#",),
    "JavaScript": (r"javascript",),
    "TypeScript": (r"typescript",),
    "Go": (r"golang", r"go programming"),
    "Rust": (r"rust",),
    "SQL": (r"sql",),
    "React": (r"react(?:\.js)?",),
    "Node.js": (r"node\.?js",),
    "AWS": (r"aws", r"amazon web services"),
    "Azure": (r"azure",),
    "GCP": (r"gcp", r"google cloud platform"),
    "Docker": (r"docker",),
    "Kubernetes": (r"kubernetes", r"k8s"),
    "Terraform": (r"terraform",),
    "PostgreSQL": (r"postgres(?:ql)?",),
    "machine learning": (r"machine learning",),
    "artificial intelligence": (r"artificial intelligence",),
    "data science": (r"data science",),
    "analytics": (r"analytics",),
    "Excel": (r"excel",),
    "financial modeling": (r"financial model(?:ing)?",),
    "accounting": (r"accounting",),
    "audit": (r"audit",),
    "tax": (r"tax",),
    "risk management": (r"risk management",),
    "mechanical engineering": (r"mechanical engineering",),
    "electrical engineering": (r"electrical engineering",),
    "CAD": (r"cad",),
    "SolidWorks": (r"solidworks",),
    "supply chain": (r"supply chain",),
    "logistics": (r"logistics",),
    "procurement": (r"procurement",),
    "sales": (r"sales",),
    "CRM": (r"crm",),
    "SEO": (r"seo",),
    "digital marketing": (r"digital marketing",),
    "human resources": (r"human resources",),
    "recruiting": (r"recruiting",),
    "talent acquisition": (r"talent acquisition",),
    "compliance": (r"compliance",),
    "legal": (r"legal",),
    "contracts": (r"contracts?",),
}
COMPILED = [
    (name, [re.compile(rf"(?<![A-Za-z0-9])(?:{alias})(?![A-Za-z0-9])", re.I) for alias in aliases])
    for name, aliases in KEYWORDS.items()
]


def extract_keywords(text: str, limit: int = 12) -> list[str]:
    return [
        name
        for name, patterns in COMPILED
        if any(pattern.search(text or "") for pattern in patterns)
    ][:limit]
