import argparse
import subprocess
import sys


COMMANDS = {
    "validate": "validate.py",
    "classify": "classify.py",
    "audit": "audit.py",
    "plan": "plan.py",
}


def main():
    parser = argparse.ArgumentParser(
        description="IMS: Linux inventory, auditing and restoration planning"
    )
    parser.add_argument(
        "command",
        choices=COMMANDS,
        help="Operation to run",
    )

    args = parser.parse_args()
    script = COMMANDS[args.command]

    result = subprocess.run(
        [sys.executable, script],
        check=False,
    )

    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
