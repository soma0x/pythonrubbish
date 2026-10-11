from pathlib import Path
import subprocess
import tomllib

from validate import load_manifest, validate_manifest


PROJECT_DIR = Path(__file__).resolve().parent


def get_installed_packages():
    result = subprocess.run(
        ["pacman", "-Qq"],
        capture_output=True,
        text=True,
        check=True,
    )

    return set(result.stdout.splitlines())


def build_plan(manifest, installed):
    required = {
        package
        for details in manifest.values()
        for package in details["packages"]
    }

    return sorted(required - installed)


def main():
    manifest = load_manifest()
    errors = validate_manifest(manifest)

    if errors:
        print("Manifest validation failed:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    installed = get_installed_packages()
    missing = build_plan(manifest, installed)

    print("\n=== IMS RESTORATION PLAN ===")
    print(f"Installed packages: {len(installed)}")
    print(f"Curated packages:   {sum(len(d['packages']) for d in manifest.values())}")
    print(f"Packages to install: {len(missing)}")

    if not missing:
        print("\nNothing to install. All curated packages are present.")
        return

    print("\n--- Proposed installation ---")
    for package in missing:
        print(f"  {package}")

    print("\nProposed command (not executed):")
    print("sudo pacman -S --needed " + " ".join(missing))
    print("\nDry run complete. No system changes made.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError, tomllib.TOMLDecodeError) as error:
        raise SystemExit(f"IMS error: {error}")
