from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[1]
required = [
    "README.md", "docker-compose.yml", ".env.example", "apps/web/package.json",
    "apps/web/app/page.tsx", "services/api/app/main.py", "services/api/app/models.py",
    "services/worker/app/tasks.py", "infra/postgres/001_init.sql",
    "docs/architecture.md", "docs/security-and-abuse.md", ".github/workflows/ci.yml",
]
missing = [path for path in required if not (root / path).exists()]
for package_file in [root / "package.json", root / "apps/web/package.json"]:
    json.loads(package_file.read_text())
if missing:
    print("Missing foundation files:", *missing, sep="\n- ")
    process.exit(1)
print(f"Foundation verification passed: {len(required)} required files present; package JSON valid.")
