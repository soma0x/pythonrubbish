
from pathlib import Path
import tomllib


PROJECT_DIR = Path(__file__).resolve().parent
SAVE_DIR = Path.home() / "savefiles"

INVENTORY_FILE = SAVE_DIR / "packages-explicit.txt"
DEPENDENCIES_FILE = SAVE_DIR / "packages-dependencies.txt"
FOREIGN_FILE = SAVE_DIR / "packages-foreign.txt"
MANIFEST_FILE = PROJECT_DIR / "config" / "packages.toml"


def load_package_file(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Required inventory not found: {path}"
        )

    return {
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip()
    }


def load_manifest():
    if not MANIFEST_FILE.exists():
        raise FileNotFoundError(
            f"Manifest not found: {MANIFEST_FILE}"
        )

    with MANIFEST_FILE.open("rb") as file:
        data = tomllib.load(file)

    packages = {}

    for category, details in data.items():
        names = details.get("packages", [])

        if not isinstance(names, list):
            raise ValueError(
                f"{category}: packages must be a list"
            )

        for package in names:
            if not isinstance(package, str):
                raise ValueError(
                    f"{category}: package names must be strings"
                )

            if package in packages:
                raise ValueError(
                    f"{package!r} appears in multiple categories"
                )

            packages[package] = category

    return packages


def show_overlap(name_a, packages_a, name_b, packages_b):
    overlap = packages_a & packages_b

    print(f"\n{name_a} ∩ {name_b}: {len(overlap)}")

    for package in sorted(overlap):
        print(f"  {package}")



def main():
    explicit = load_package_file(INVENTORY_FILE)
    dependencies = load_package_file(DEPENDENCIES_FILE)
    foreign = load_package_file(FOREIGN_FILE)
    manifest = load_manifest()

    installed = explicit | dependencies
    curated = set(manifest)

    matched = installed & curated
    missing = curated - installed
    unlisted_explicit = explicit - curated
    unlisted_dependencies = dependencies - curated

    print("\n=== IMS SYSTEM AUDIT ===")
    print(f"Explicit packages:              {len(explicit)}")
    print(f"Dependency packages:            {len(dependencies)}")
    print(f"Foreign packages:                {len(foreign)}")
    print(f"Unique installed packages:      {len(installed)}")
    print(f"Curated manifest packages:      {len(curated)}")
    print(f"Curated packages installed:     {len(matched)}")
    print(f"Curated packages missing:       {len(missing)}")
    print(f"Unlisted explicit packages:     {len(unlisted_explicit)}")
    print(f"Unlisted dependency packages:    {len(unlisted_dependencies)}")

    if missing:
        print("\n--- Curated packages missing ---")
        for package in sorted(missing):
            print(f"  {package} [{manifest[package]}]")

    if unlisted_explicit:
        print("\n--- Explicit packages not in manifest ---")
        for package in sorted(unlisted_explicit):
            print(f"  {package}")

    if foreign:
        print("\n--- Foreign packages ---")
        for package in sorted(foreign):
            category = manifest.get(package, "unclassified")
            print(f"  {package} [{category}]")
    else:
        print("\nNo foreign packages reported by pacman.")

    print("\nAudit complete. No system changes made.")



if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        raise SystemExit(f"IMS error: {error}")
