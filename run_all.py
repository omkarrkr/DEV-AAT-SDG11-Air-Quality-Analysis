"""Run preprocessing, statistics, and the notebook in dependency order."""

import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parent
NOTEBOOK = PROJECT_ROOT / "notebooks" / "SDG11_Air_Quality_Analysis.ipynb"


def run_stage(label, *args, env, cwd=PROJECT_ROOT):
    print(label, flush=True)
    subprocess.run([sys.executable, *args], cwd=cwd, env=env, check=True)


def main():
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    try:
        run_stage("1. Preprocess the raw dataset", "src/dfmodif.py", env=env)
        run_stage("2. Export statistical tables", "src/analysis.py", env=env)
        with TemporaryDirectory(prefix="sdg11-jupyter-") as directory:
            runtime = Path(directory)
            # Use this interpreter and keep notebook history outside user profiles.
            kernel = runtime / "kernels" / "python3"
            kernel.mkdir(parents=True)
            (kernel / "kernel.json").write_text(
                json.dumps({
                    "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                    "display_name": "Python 3 (ipykernel)",
                    "language": "python",
                }),
                encoding="utf-8",
            )
            notebook_env = dict(
                env,
                JUPYTER_PATH=str(runtime),
                JUPYTER_RUNTIME_DIR=str(runtime / "runtime"),
                IPYTHONDIR=str(runtime / "ipython"),
            )
            run_stage(
                "3. Execute the notebook and save the charts",
                "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace",
                "--ExecutePreprocessor.kernel_name=python3",
                "--ExecutePreprocessor.timeout=300", str(NOTEBOOK),
                env=notebook_env, cwd=NOTEBOOK.parent,
            )
    except subprocess.CalledProcessError as error:
        print(f"Pipeline stopped with exit code {error.returncode}.", file=sys.stderr)
        return 1
    print("Pipeline completed. See dataset/processed, outputs, and notebooks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
