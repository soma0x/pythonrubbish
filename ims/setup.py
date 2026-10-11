
from pathlib import Path
import argparse
import re
import tomllib


PROJECT_DIR = Path(__file__).resolve().parent
MANIFEST_FILE = PROJECT_DIR / "config" / "packages.toml"
INVENTORY_FILE = Path.home() / "savefiles" / "packages-explicit.txt"

PACKAGE_PATTERN = re.compile(r"[A-Za-z0-9@._+-]+")


def load_inventory():
    if not INVENTORY_FILE.exists():
        raise FileNotFoundError(
            f"Inventory not found: {INVENTORY_FILE}"
        )

    packages = {
        line.strip()
        for line in INVENTORY_FILE.read_text().splitlines()
        if line.strip()
    }

    invalid = sorted(
        package for package in packages
        if not PACKAGE_PATTERN.fullmatch(package)
    )

    if invalid:
        raise ValueError(f"Invalid package names: {invalid}")

    return packages


def load_manifest():
    if not MANIFEST_FILE.exists():
        raise FileNotFoundError(
            f"Manifest not found: {MANIFEST_FILE}"
        )

    with MANIFEST_FILE.open("rb") as file:
        config = tomllib.load(file)

    categorized = {}

    for category, details in config.items():
        packages = details.get("packages", [])

        if not isinstance(packages, list):
            raise ValueError(
                f"{category}: packages must be a list"
            )

        for package in packages:
            if not isinstance(package, str):
                raise ValueError(
                    f"{category}: package names must be strings"
                )

            if not PACKAGE_PATTERN.fullmatch(package):
                raise ValueError(
                    f"{category}: invalid package name {package!r}"
                )

            if package in categorized:
                raise ValueError(
                    f"{package!r} appears in multiple categories"
                )

            categorized[package] = category

    return categorized


def show_report(inventory, categorized):
    known = inventory & categorized.keys()
    unknown = categorized.keys() - inventory
    uncategorized = inventory - categorized.keys()

    print("\n=== IMS PACKAGE REPORT ===\n")
    print(f"Inventory packages: {len(inventory)}")
    print(f"Categorized matches: {len(known)}")
    print(f"Manifest-only packages: {len(unknown)}")
    print(f"Uncategorized packages: {len(uncategorized)}")

    print("\n--- Categories ---")

    categories = sorted(set(categorized.values()))

    for category in categories:
        names = sorted(
            package
            for package, group in categorized.items()
            if group == category
        )
        print(f"\n{category} ({len(names)}):")
        for name in names:
            print(f"  [x] {name}")

    if unknown:
        print("\n--- In manifest, not in inventory ---")
        for name in sorted(unknown):
            print(f"  [?] {name}")

    if uncategorized:
        print("\n--- Needs classification ---")
        for name in sorted(uncategorized):
            print(f"  [ ] {name}")


def main():
    parser = argparse.ArgumentParser(
        description="IMS: Linux setup and restoration tool"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Accepted for explicit dry-run mode",
    )
    args = parser.parse_args()

    try:
        inventory = load_inventory()
        categorized = load_manifest()
        show_report(inventory, categorized)

        print("\nReport complete. No system changes made.")

    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        raise SystemExit(f"IMS error: {error}")


if __name__ == "__main__":
    main()
