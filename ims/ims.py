
import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

COMMANDS = {
    "validate": "validate.py",
    "classify": "classify.py",
    "audit": "audit.py",
    "plan": "plan.py",
    "install": "install.py",
    "restore": "install.py",
}


def main():
    parser = argparse.ArgumentParser(
        description="IMS: Install My Shit...made by nmesoma"
    )
    parser.add_argument(
        "command",
        choices=COMMANDS,
        help="Operation to run",
    )

    args = parser.parse_args()
    script = PROJECT_DIR / COMMANDS[args.command]

    command = [sys.executable, str(script)]

    if args.command == "restore":
        command.append("--restore")

    result = subprocess.run(
        command,
        check=False,
    )

    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
