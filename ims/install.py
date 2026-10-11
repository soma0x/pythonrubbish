
import argparse
import subprocess
import sys
import tomllib

from validate import (
    ALLOWED_CATEGORIES,
    REVIEW_CATEGORIES,
    REVIEW_MANIFEST_FILE,
    load_manifest,
    validate_manifest,
)
from plan import build_plan, get_installed_packages


CRITICAL_PACKAGES = {
    "base",
    "linux-cachyos",
    "linux-cachyos-lts",
    "linux-cachyos-headers",
    "linux-cachyos-lts-headers",
    "linux-firmware",
    "intel-ucode",
    "limine",
    "limine-mkinitcpio-hook",
    "limine-snapper-sync",
    "mkinitcpio",
    "systemd",
    "cryptsetup",
    "device-mapper",
    "efibootmgr",
    "lvm2",
    "sudo",
}


def install_packages(packages):
    """Install supplied packages using pacman."""
    if not packages:
        return 0

    result = subprocess.run(
        ["sudo", "pacman", "-S", "--needed", *packages],
        check=False,
    )
    return result.returncode


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="IMS: Install My Shit...made by nmesoma"
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Use the expanded restoration manifest.",
    )
    args = parser.parse_args([] if argv is None else argv)

    if args.restore:
        manifest = load_manifest(REVIEW_MANIFEST_FILE)
        allowed_categories = REVIEW_CATEGORIES
        mode_name = "RESTORATION"
    else:
        manifest = load_manifest()
        allowed_categories = ALLOWED_CATEGORIES
        mode_name = "NORMAL INSTALL"

    errors = validate_manifest(
        manifest,
        allowed_categories=allowed_categories,
    )

    if errors:
        print("Manifest validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    installed = get_installed_packages()
    missing = build_plan(manifest, installed)

    total = sum(
        len(details["packages"])
        for details in manifest.values()
    )

    print(f"\n=== IMS {mode_name} ===")
    print(f"Installed packages: {len(installed)}")
    print(f"Manifest packages:  {total}")
    print(f"Packages missing:   {len(missing)}")

    if not missing:
        print("\nAll packages in this manifest are already installed.")
        return 0

    print("\nPackages to install:")
    for package in missing:
        print(f"  - {package}")

    critical_missing = sorted(
        package for package in missing
        if package in CRITICAL_PACKAGES
    )

    if args.restore and critical_missing:
        print("\nWARNING: Missing system-critical packages:")
        for package in critical_missing:
            print(f"  - {package}")

        confirmation = input(
            '\nType "RESTORE SYSTEM PACKAGES" to continue: '
        ).strip()

        if confirmation != "RESTORE SYSTEM PACKAGES":
            print("System package restoration cancelled.")
            return 0

    answer = input(
        "\nContinue with installation? [y/N]: "
    ).strip().lower()

    if answer != "y":
        print("Installation cancelled. No changes made by IMS.")
        return 0

    try:
        return_code = install_packages(missing)
    except OSError as error:
        print(f"Could not start the package installer: {error}")
        return 1

    if return_code != 0:
        print(
            f"Package installation failed with exit code {return_code}."
        )
        return return_code

    print("\nIMS installation completed successfully.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (
        OSError,
        subprocess.CalledProcessError,
        tomllib.TOMLDecodeError,
    ) as error:
        raise SystemExit(f"IMS error: {error}")
