"""Sandbox worker: process a large attachment and write results next to it.

Locations are either local paths or az://<container>/<blob> (Azure Blob Storage, auth via
DefaultAzureCredential / managed identity, account from AZURE_STORAGE_ACCOUNT).

Usage:
    python worker.py --input az://input/sales.csv --output az://output/run-1 --task profile
    python worker.py --input data.xlsx --output out --task script --script my_job.py

`profile` writes summary.json. `script` runs a user script as `python script INPUT OUTPUT_DIR`
in a subprocess with a time limit; whatever it writes to OUTPUT_DIR is uploaded.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT = int(os.environ.get("SANDBOX_TIMEOUT_SECONDS", "900"))


def _blob_service():
    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient

    account = os.environ["AZURE_STORAGE_ACCOUNT"]
    return BlobServiceClient(f"https://{account}.blob.core.windows.net", credential=DefaultAzureCredential())


def _split(uri: str) -> tuple[str, str]:
    container, _, blob = uri.removeprefix("az://").partition("/")
    return container, blob


def fetch(uri: str, workdir: Path) -> Path:
    if not uri.startswith("az://"):
        return Path(uri)
    container, blob = _split(uri)
    dest = workdir / Path(blob).name
    with open(dest, "wb") as fh:
        _blob_service().get_blob_client(container, blob).download_blob().readinto(fh)
    return dest


def publish(local_dir: Path, uri: str) -> None:
    if not uri.startswith("az://"):
        return
    container, prefix = _split(uri)
    client = _blob_service().get_container_client(container)
    for f in local_dir.rglob("*"):
        if f.is_file():
            with open(f, "rb") as fh:
                client.upload_blob(f"{prefix}/{f.relative_to(local_dir)}".strip("/"), fh, overwrite=True)


def profile(path: Path, out: Path) -> dict:
    import duckdb
    import pandas as pd

    suffix = path.suffix.lower()
    con = duckdb.connect()
    if suffix == ".xlsx":
        con.register("t", pd.read_excel(path))
        source = "t"
    elif suffix == ".parquet":
        source = f"read_parquet('{path}')"
    else:
        source = f"read_csv_auto('{path}')"
    rows = con.execute(f"select count(*) from {source}").fetchone()[0]
    cols = con.execute(f"describe select * from {source}").fetchall()
    summary = {"file": path.name, "rows": rows, "columns": []}
    for name, dtype, *_ in cols:
        q = f'"{name}"'
        stats = {"name": name, "type": dtype, "nulls": con.execute(f"select count(*) - count({q}) from {source}").fetchone()[0],
                 "distinct": con.execute(f"select count(distinct {q}) from {source}").fetchone()[0]}
        if any(k in dtype for k in ("INT", "DOUBLE", "DECIMAL", "FLOAT")):
            lo, hi, avg = con.execute(f"select min({q}), max({q}), avg({q}) from {source}").fetchone()
            stats.update(min=lo, max=hi, mean=avg)
        summary["columns"].append(stats)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    return summary


def run_script(script: Path, path: Path, out: Path) -> None:
    res = subprocess.run([sys.executable, str(script), str(path), str(out)], capture_output=True, text=True, timeout=TIMEOUT)
    (out / "script.log").write_text(res.stdout + res.stderr)
    if res.returncode:
        raise SystemExit(f"script failed with exit {res.returncode}; see script.log")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--task", choices=["profile", "script"], default="profile")
    ap.add_argument("--script", type=Path)
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        out = work / "out" if args.output.startswith("az://") else Path(args.output)
        out.mkdir(parents=True, exist_ok=True)
        src = fetch(args.input, work)
        if args.task == "profile":
            result = profile(src, out)
            print(json.dumps({"rows": result["rows"], "columns": len(result["columns"])}))
        else:
            run_script(args.script, src, out)
        publish(out, args.output)


if __name__ == "__main__":
    main()
