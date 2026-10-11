from pathlib import Path
import argparse
import re
import subprocess




PACKAGE_FILE = Path.home() / "savefiles" / "packages-explicit.txt"




def load_packages():
    if not PACKAGE_FILE.exists():
        raise FileNotFoundError(
                f"Package list not found: {PACKAGE_FILE}"
        )

    packages = PACKAGE_FILE.read_text().splitlines()

    packages = [
            package.strip()
            for package in packages
            if package.strip()
    ]

    invalid = [
            package
            for package in packages
            if not re.fullmatch(r"[A-Za-z0-9@._+-]+", package)
    ]

    if invalid:
        raise ValueError(f"Invalid package names: {invalid}")


    return list(dict.fromkeys(packages))



def show_plan(packages):
    print(f"\nLoaded {len(packages)} packages.")
    print("\nPackage installation plan:\n")

    for package in packages:
        print(f" [ ] {package}")


def install_packages(packages):
    command = [
            "sudo",
            "pacman",
            "-S",
            "--needed",
            *packages,
    ]

    print("\nStarting package installation...\n")

    result = subprocess.run(command, check=False)

    if result.returncode != 0:
        raise SystemExit(
                f"Package installation failed with "
                f"exiting {result.returncode}"
        )



def main():
    parser = argparse.ArgumentParser(
            description="ims: install my shit"
    )

    parser.add_argument(
            "--install",
            action="store_true",
            help="Actually install packages",
    )

    args = parser.parse_args()


    try:
        packages = load_packages()
        show_plan(packages)

        if args.install:
            install_packages(packages)
        else:
            print("\nDry run only. nothing installed relax")
            print("use --install when you're man enough or woman idk")

    except (OSError, ValueError) as error:
        raise SystemExit(f"Error: {error}")


if __name__  == "__main__":
    main()

