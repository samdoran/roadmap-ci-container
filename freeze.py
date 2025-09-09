#!/usr/bin/env python

import subprocess
import sys
import venv

from pathlib import Path


def main():
    file = Path(__file__)
    repo_root = file.parent
    venv_path = repo_root / ".venvs" / f"freezer-{sys.version_info.major}.{sys.version_info.minor}"
    python_bin = venv_path / "bin" / "python"
    requirements = repo_root / "requirements.in"
    freeze_file = repo_root / requirements.with_suffix(".txt").name

    print(f"🥶 Freezing Python {sys.version_info.major}.{sys.version_info.minor} {freeze_file.stem}...")

    # Create a fresh virtual environment
    venv.create(venv_path, with_pip=True, clear=True)
    subprocess.check_output([python_bin, "-m", "pip", "install", "--upgrade", "pip"])

    # Install requirements with constraints
    subprocess.check_output(
        [python_bin, "-m", "pip", "install", "--requirement", requirements,]
    )

    # Generate a freeze file
    result = subprocess.run([python_bin, "-m", "pip", "freeze"], check=True, capture_output=True)
    freeze_file.write_bytes(result.stdout)

    print(f"✅ {freeze_file.stem}-{sys.version_info.major}.{sys.version_info.minor} complete")


if __name__ == "__main__":
    main()
