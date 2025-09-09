#!/usr/bin/env python

import pathlib
import urllib.request


def main():
    url = "https://raw.githubusercontent.com/RedHatInsights/digital-roadmap-backend/main/requirements"
    files = [
        "requirements.in",
        "requirements-test.in",
    ]

    requirements_in = pathlib.Path("requirements.in")
    requirements = set(requirements_in.read_text().splitlines())
    for file in files:
        with urllib.request.urlopen(f"{url}/{file}") as f:
            data = f.read().decode()

        requirements.update(data.splitlines())

    requirements.remove("psycopg[c]")
    requirements.add("psycopg")
    requirements = sorted(requirements)

    requirements_in.write_text("\n".join(requirements) + "\n")


if __name__ == "__main__":
    main()
