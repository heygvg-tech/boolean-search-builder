"""Boolean search string builder for technical recruiters."""
from .builder import Search, build_all, github_xray, google_xray, linkedin

__all__ = ["Search", "build_all", "linkedin", "google_xray", "github_xray"]
__version__ = "0.1.0"
