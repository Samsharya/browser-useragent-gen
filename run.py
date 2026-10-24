
#!/usr/bin/env python3

import os
import random
import subprocess
import sys
from pathlib import Path

from ua import PROFILES

BASE_DIR = Path(__file__).resolve().parent
UA_SCRIPT = BASE_DIR / "ua.py"
OUTPUT_DIR = BASE_DIR / "output"

FORMATS = ["txt", "json", "csv"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    clear_screen()
    print("=" * 46)
    print("         BROWSER UA GENERATOR")
    print("=" * 46)
    print()


def pause():
    try:
        input("\nPress Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        raise SystemExit(0)


def ask_choice(prompt, options, allow_all=False):
    
    choices = list(options)

    if allow_all:
        choices.insert(0, "all")

    if not choices:
        return None

    print()
    for index, item in enumerate(choices, 1):
        print(f"  {index}. {item.title()}")

    while True:
        try:
            answer = input(f"\n{prompt}: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit(0)

        try:
            index = int(answer)
            if 1 <= index <= len(choices):
                return choices[index - 1]
        except ValueError:
            pass

        print("Invalid selection. Try again.")


def ask_count():
    while True:
        try:
            answer = input("\nNumber of user agents [10]: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit(0)

        if not answer:
            return 10

        try:
            count = int(answer)
            if count > 0:
                return count
        except ValueError:
            pass

        print("Enter a positive whole number.")


def ask_seed():
    try:
        answer = input("Random seed (blank for random): ").strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit(0)

    if not answer:
        return random.SystemRandom().randint(0, 2**31 - 1)

    try:
        return int(answer)
    except ValueError:
        print("Invalid seed. Using a random seed.")
        return random.SystemRandom().randint(0, 2**31 - 1)


def get_valid_values(field, browser=None, os_name=None, device=None):
    
    filters = {
        "browser": browser,
        "os": os_name,
        "device": device,
    }

    matches = [
        profile for profile in PROFILES
        if all(
            value is None or profile[key] == value
            for key, value in filters.items()
        )
    ]

    return sorted({profile[field] for profile in matches})


def choose_valid(field, label, browser=None, os_name=None, device=None,
                 allow_all=True):
    values = get_valid_values(
        field,
        browser=browser,
        os_name=os_name,
        device=device,
    )

    return ask_choice(label, values, allow_all=allow_all)


def run_cli(arguments):
    
    command = [sys.executable, str(UA_SCRIPT), *arguments]

    try:
        result = subprocess.run(command, cwd=BASE_DIR, check=False)
        return result.returncode == 0
    except OSError as exc:
        print(f"\nUnable to run generator: {exc}")
        return False


def export_results(mode, options, count, output_format, seed):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    formats = FORMATS if output_format == "all" else [output_format]

    for fmt in formats:
        print(f"\nGenerating {count} profile(s) as {fmt.upper()}...")

        arguments = [
            mode,
            *options,
            "--count", str(count),
            "--seed", str(seed),
            "--format", fmt,
            "--output", f"agents.{fmt}",
        ]

        if not run_cli(arguments):
            print(
                "\nGeneration failed. Check the profile catalog "
                "and the error reported by ua.py."
            )
            pause()
            return

    print(f"\nExports saved in: {OUTPUT_DIR}")
    pause()


def random_menu():
    header()
    print("RANDOM GENERATION")

    count = ask_count()

    browser = choose_valid("browser", "Browser")
    if browser is None:
        print("No browser profiles are available.")
        pause()
        return

    system = choose_valid(
        "os",
        "Operating system",
        browser=None if browser == "all" else browser,
    )
    if system is None:
        print("No compatible operating systems are available.")
        pause()
        return

    device = choose_valid(
        "device",
        "Device",
        browser=None if browser == "all" else browser,
        os_name=None if system == "all" else system,
    )
    if device is None:
        print("No compatible devices are available.")
        pause()
        return

    options = []

    if browser != "all":
        options.extend(["--browser", browser])
    if system != "all":
        options.extend(["--os", system])
    if device != "all":
        options.extend(["--device", device])

    output_format = ask_choice(
        "Export format", FORMATS, allow_all=True
    )
    seed = ask_seed()

    export_results("random", options, count, output_format, seed)


def selected_menu():
    header()
    print("SELECTED PROFILE")

    browser = choose_valid("browser", "Browser", allow_all=False)
    if browser is None:
        print("No profiles are available.")
        pause()
        return

    system = choose_valid(
        "os", "Operating system",
        browser=browser,
        allow_all=False,
    )
    if system is None:
        print("No compatible operating systems.")
        pause()
        return

    device = choose_valid(
        "device", "Device",
        browser=browser,
        os_name=system,
        allow_all=False,
    )
    if device is None:
        print("No compatible devices.")
        pause()
        return

    count = ask_count()

    options = [
        "--browser", browser,
        "--os", system,
        "--device", device,
    ]

    output_format = ask_choice(
        "Export format", FORMATS, allow_all=True
    )
    seed = ask_seed()

    export_results("generate", options, count, output_format, seed)


def list_profiles():
    header()
    if not run_cli(["list"]):
        print("Unable to list profiles.")
    pause()


def main():
    if not UA_SCRIPT.is_file():
        print(f"Error: missing file: {UA_SCRIPT}")
        return 1

    if not (BASE_DIR / "exporter.py").is_file():
        print("Error: exporter.py is missing.")
        return 1

    while True:
        header()
        print("  1. Generate random user agents [Realistic curated profiles]")
        print("  2. Generate selected profiles [Custom combinations; may be unrealistic]")
        print("  3. List available profiles")
        print("  4. Exit")
        try:
            choice = input("\nSelect an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0

        if choice == "1":
            random_menu()
        elif choice == "2":
            selected_menu()
        elif choice == "3":
            list_profiles()
        elif choice == "4":
            print("Goodbye.")
            return 0
        else:
            print("Invalid option.")
            pause()


if __name__ == "__main__":
    raise SystemExit(main())
