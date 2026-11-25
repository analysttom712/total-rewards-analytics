"""Learning hub: a local study site built from the docs on every request.

Start it with `python -m hub`, then open http://127.0.0.1:8765.
Brief: docs/site/BRIEF.md.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PORT = 8765
ISSUES_URL = "https://github.com/analysttom712/total-rewards-analytics/issues"
PROGRESS_FILE = "progress.local.json"
