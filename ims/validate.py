from pathlib import Path
import tomllib


PROJECT_DIR = Path(__file__).resolve().parent
MANIFEST_FILE = PROJECT_DIR / "config" / "packages.toml"
ALLOWED_CATEGORIES = {
    "desktop",
    "development",
    "security",
    "gaming",
    "media",
}

def load_manifest():
    if not MANIFEST_FILE.exists():
        raise FileNotFoundError(
            f"Manifest not found: {MANIFEST_FILE}"
        )

    with MANIFEST_FILE.open("rb") as file:
        return tomllib.load(file)


def validate_manifest(manifest):
    errors = []

    if not isinstance(manifest, dict):
        return ["Manifest root must be a TOML table."]

    if not manifest:
        errors.append("Manifest contains no categories.")

    seen_packages = {}

    for category, details in manifest.items():
        if category not in ALLOWED_CATEGORIES:
            errors.append(
                f"{category!r}: unknown category."
            )

        if not isinstance(details, dict):
            errors.append(
                f"{category}: category must be a TOML table."
            )
            continue

        packages = details.get("packages")

        if not isinstance(packages, list):
            errors.append(
                f"{category}: packages must be a list."
            )
            continue

        for package in packages:
            if not isinstance(package, str) or not package.strip():
                errors.append(
                    f"{category}: package names must be non-empty strings."
                )
                continue

            if package in seen_packages:
                errors.append(
                    f"{package!r} appears in both "
                    f"{seen_packages[package]!r} and {category!r}."
                )
            else:
                seen_packages[package] = category

    return errors




def main():
    manifest = load_manifest()
    errors = validate_manifest(manifest)

    if errors:
        print("Manifest validation failed:")

        for error in errors:
            print(f"  - {error}")

        raise SystemExit(1)

    print("Manifest validation passed.")
    print("\nCategories:")

    for category, details in manifest.items():
        print(f"{category}: {len(details['packages'])} packages")

        


if __name__ == "__main__":
    try:
        main()
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise SystemExit(f"IMS error: {error}")