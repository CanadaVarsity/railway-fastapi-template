import os
import sys
import subprocess

def main():
    port = os.getenv("PORT", "8080")
    cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", port,
    ]
    # Optional: reduce noise
    # cmd += ["--log-level", "info"]
    raise SystemExit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
