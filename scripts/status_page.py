"""Render the status page (the pinned status issue) from a smoke-check result.

    python -m scripts.status_page ENVIRONMENT smoke.json [--live SHA]
"""
import json
import os
import sys
from datetime import datetime, timezone


def main():
    env, path = sys.argv[1], sys.argv[2]
    sha = sys.argv[sys.argv.index("--live") + 1] if "--live" in sys.argv else os.environ.get("GITHUB_SHA", "")
    smoke = json.load(open(path))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    run = f"{os.environ.get('GITHUB_SERVER_URL', '')}/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
    state = "🟢 Operational" if smoke["ok"] else "🔴 Degraded"
    print(f"## {env.capitalize()}: {state}\n")
    print("| | |\n|---|---|")
    print(f"| Live commit | `{sha[:7]}` |")
    print(f"| Checked | {now} ([run]({run})) |")
    print(f"| Workflow | {os.environ.get('GITHUB_WORKFLOW', '')} |\n")
    print("| Check | Result |\n|---|---|")
    for r in smoke["results"]:
        mark = "❌" if r["status"] >= 500 else "✅"
        print(f"| {r['check']} | {mark} HTTP {r['status']} |")
    print("\n_Updated automatically by the deploy and health-check workflows. Do not edit by hand._")


if __name__ == "__main__":
    main()
