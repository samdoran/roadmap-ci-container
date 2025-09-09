#!/usr/bin/env python

import pathlib
import sys
import urllib.request


def main():
    url = "https://raw.githubusercontent.com/RedHatInsights/digital-roadmap-backend/main/requirements"
    files = [
        "requirements",
        "requirements-test",
    ]
    print(url)
    requirements = []
    for file in files:
        with urllib.request.urlopen(f"{url}/{file}-{sys.version_info.major}.{sys.version_info.minor}.txt") as f:
            data = f.read().decode()

        requirements.extend(data.splitlines())

    requirements = sorted((req for req in requirements if "-r" != req[:2]), key=str.lower)
    requirements = [req for req in requirements if "psycopg-c" not in req]

    pathlib.Path("requirements.txt").write_text("\n".join(requirements))

if __name__ == "__main__":
    main()
