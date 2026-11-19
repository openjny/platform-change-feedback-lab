import argparse
import json
import re
import sys
from pathlib import Path

ENVIRONMENTS = ("dev", "tst", "prd")
REGIONS = ("westeurope", "northeurope")
FIELDS = {"name", "environment", "region", "replicas"}


def validate(value: object) -> list[str]:
    if not isinstance(value, dict):
        return ["The plan must be a JSON object."]
    if set(value) != FIELDS:
        return [f"The plan must define exactly: {', '.join(sorted(FIELDS))}."]

    errors = []
    name = value["name"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]{2,23}", name):
        errors.append("name: use 3–24 lowercase letters, digits, or hyphens; start with a letter.")
    if value["environment"] not in ENVIRONMENTS:
        errors.append(f"environment: use one of {', '.join(ENVIRONMENTS)}.")
    if value["region"] not in REGIONS:
        errors.append(f"region: use one of {', '.join(REGIONS)}.")
    replicas = value["replicas"]
    if type(replicas) is not int or not 1 <= replicas <= 5:
        errors.append("replicas: use an integer from 1 to 5.")
    elif value["environment"] == "prd" and replicas < 2:
        errors.append("replicas: production requires at least 2.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a synthetic cloud plan.")
    parser.add_argument("profile", type=Path)
    profile = parser.parse_args().profile
    try:
        errors = validate(json.loads(profile.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"{profile}: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"{profile}: {error}", file=sys.stderr)
        return 2
    print(f"Valid plan: {profile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
