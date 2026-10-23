"""Run one ticket through Copilot CLI in a sandboxed clone, then verify independently.

Usage:
    python harness/run_task.py agents/memory/DEMO-1.json [--docker-verify]

Reads `assignment`, `plan` and `relevant_files` from the ticket memory file, clones the
repo into runs/<ticket>/work on a fresh branch, lets Copilot edit and test there, then
re-runs the tests itself (Copilot's claim is never trusted) and writes the outcome back
to the memory file. It never pushes; shipping is the Release agent's job.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COPILOT_TIMEOUT = 600

ALLOW = ["write", "shell(pytest)", "shell(python)", "shell(git diff)", "shell(git status)", "shell(cat)", "shell(ls)", "shell(rg)"]
DENY = ["shell(git push)", "shell(git remote)", "shell(rm)", "shell(curl)", "shell(wget)", "shell(sudo)"]


def run(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)


def build_prompt(ticket: dict) -> str:
    files = "\n".join(f"- {f}" for f in ticket.get("relevant_files", [])) or "- (none listed, search the repo)"
    return (
        f"Ticket {ticket['ticket']}: {ticket['assignment']}\n\n"
        f"Plan:\n{ticket.get('plan') or '(none)'}\n\n"
        f"Relevant files:\n{files}\n\n"
        "Reproduce the problem by running the tests, fix the root cause in the source (do not edit "
        "tests to make them pass), re-run the tests, and finish with a one-paragraph summary. "
        "Do not commit or push."
    )


def prepare_workdir(ticket: dict, run_dir: Path) -> Path:
    work = run_dir / "work"
    if work.exists():
        shutil.rmtree(work)
    run(["git", "clone", "--quiet", "--local", str(ROOT), str(work)], cwd=ROOT).check_returncode()
    branch = f"fix/{ticket['ticket'].lower()}"
    run(["git", "checkout", "-q", "-b", branch], cwd=work).check_returncode()
    # sandbox keeps its own identity so nothing leaks from the global config
    run(["git", "config", "user.name", "ArmenMadoyan"], cwd=work)
    run(["git", "config", "user.email", "38354243+ArmenMadoyan@users.noreply.github.com"], cwd=work)
    ticket["branch"] = branch
    return work


def run_copilot(prompt: str, work: Path, run_dir: Path) -> subprocess.CompletedProcess:
    cmd = ["copilot", "-p", prompt, "-s", "--no-ask-user", "--add-dir", str(work),
           "--log-dir", str(run_dir / "copilot-logs"), "--share", str(run_dir / "session.md")]
    for t in ALLOW:
        cmd += ["--allow-tool", t]
    for t in DENY:
        cmd += ["--deny-tool", t]
    return run(cmd, cwd=work, timeout=COPILOT_TIMEOUT)


def verify(work: Path, docker: bool) -> tuple[bool, str]:
    if docker:
        tag = "microsoft-agentic-factory-verify"
        build = run(["docker", "build", "-q", "-t", tag, str(work)], cwd=work)
        if build.returncode:
            return False, f"docker build failed: {build.stderr.strip()}"
        res = run(["docker", "run", "--rm", tag], cwd=work)
    else:
        res = run([sys.executable, "-m", "pytest", "-q"], cwd=work)
    return res.returncode == 0, (res.stdout + res.stderr).strip().splitlines()[-1] if (res.stdout + res.stderr).strip() else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("memory", type=Path)
    ap.add_argument("--docker-verify", action="store_true", help="verify tests inside the Docker image")
    args = ap.parse_args()

    ticket = json.loads(args.memory.read_text())
    run_dir = ROOT / "runs" / ticket["ticket"]
    run_dir.mkdir(parents=True, exist_ok=True)

    work = prepare_workdir(ticket, run_dir)
    before_ok, before = verify(work, args.docker_verify)
    ticket["reproduction"] = before
    print(f"before: {before}")

    try:
        res = run_copilot(build_prompt(ticket), work, run_dir)
        (run_dir / "copilot-output.txt").write_text(res.stdout + res.stderr)
        copilot_rc = res.returncode
    except subprocess.TimeoutExpired:
        copilot_rc = -1

    ok, after = verify(work, args.docker_verify)
    diff = run(["git", "diff", "--stat"], cwd=work).stdout.strip()
    (run_dir / "fix.diff").write_text(run(["git", "diff"], cwd=work).stdout)
    print(f"after: {after}\n{diff}")

    ticket["status"] = "fixed" if ok and not before_ok else "failed"
    ticket["verification"] = {"before": before, "after": after, "copilot_exit": copilot_rc, "diff_stat": diff}
    args.memory.write_text(json.dumps(ticket, indent=2) + "\n")
    return 0 if ticket["status"] == "fixed" else 1


if __name__ == "__main__":
    sys.exit(main())
