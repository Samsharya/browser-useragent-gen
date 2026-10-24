
#!/usr/bin/env python3

import argparse
import random
import sys

from exporter import export_records

PROFILES = [
    {
        "id": "chrome-windows-desktop",
        "browser": "chrome",
        "version": "131",
        "os": "windows",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    },
    {
        "id": "chrome-macos-desktop",
        "browser": "chrome",
        "version": "131",
        "os": "macos",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    },
    {
        "id": "chrome-linux-desktop",
        "browser": "chrome",
        "version": "131",
        "os": "linux",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    },
    {
        "id": "chrome-android-mobile",
        "browser": "chrome",
        "version": "131",
        "os": "android",
        "device": "mobile",
        "ua": (
            "Mozilla/5.0 (Linux; Android 10; K) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Mobile Safari/537.36"
        ),
    },
    {
        "id": "firefox-windows-desktop",
        "browser": "firefox",
        "version": "133",
        "os": "windows",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) "
            "Gecko/20100101 Firefox/133.0"
        ),
    },
    {
        "id": "firefox-macos-desktop",
        "browser": "firefox",
        "version": "133",
        "os": "macos",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) "
            "Gecko/20100101 Firefox/133.0"
        ),
    },
    {
        "id": "firefox-linux-desktop",
        "browser": "firefox",
        "version": "133",
        "os": "linux",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) "
            "Gecko/20100101 Firefox/133.0"
        ),
    },
    {
        "id": "firefox-android-mobile",
        "browser": "firefox",
        "version": "133",
        "os": "android",
        "device": "mobile",
        "ua": (
            "Mozilla/5.0 (Android 10; Mobile; rv:133.0) "
            "Gecko/133.0 Firefox/133.0"
        ),
    },
    {
        "id": "edge-windows-desktop",
        "browser": "edge",
        "version": "131",
        "os": "windows",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36 "
            "Edg/131.0.0.0"
        ),
    },
    {
        "id": "edge-macos-desktop",
        "browser": "edge",
        "version": "131",
        "os": "macos",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36 "
            "Edg/131.0.0.0"
        ),
    },
    {
        "id": "safari-macos-desktop",
        "browser": "safari",
        "version": "17.6",
        "os": "macos",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.6 Safari/605.1.15"
        ),
    },
    {
        "id": "safari-ios-mobile",
        "browser": "safari",
        "version": "17.6",
        "os": "ios",
        "device": "mobile",
        "ua": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.6 Mobile/15E148 Safari/604.1"
        ),
    },
    {
        "id": "safari-ipad-tablet",
        "browser": "safari",
        "version": "17.6",
        "os": "ios",
        "device": "tablet",
        "ua": (
            "Mozilla/5.0 (iPad; CPU OS 17_6 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.6 Mobile/15E148 Safari/604.1"
        ),
    },
    {
        "id": "opera-windows-desktop",
        "browser": "opera",
        "version": "115",
        "os": "windows",
        "device": "desktop",
        "ua": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/129.0.0.0 Safari/537.36 "
            "OPR/115.0.0.0"
        ),
    },
    {
        "id": "opera-android-mobile",
        "browser": "opera",
        "version": "85",
        "os": "android",
        "device": "mobile",
        "ua": (
            "Mozilla/5.0 (Linux; Android 10; K) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/129.0.0.0 Mobile Safari/537.36 "
            "OPR/85.0.0.0"
        ),
    },
]

BROWSERS = ("chrome", "firefox", "edge", "safari", "opera")
OPERATING_SYSTEMS = ("windows", "macos", "linux", "android", "ios")
DEVICES = ("desktop", "mobile", "tablet")


def filter_profiles(browser=None, os_name=None, device=None):
    
    profiles = PROFILES

    if browser:
        profiles = [
            p for p in profiles if p["browser"] == browser.lower()
        ]

    if os_name:
        profiles = [
            p for p in profiles if p["os"] == os_name.lower()
        ]

    if device:
        profiles = [
            p for p in profiles if p["device"] == device.lower()
        ]

    return profiles


def generate_random(count=1, browser=None, os_name=None,
                    device=None, seed=None):
    # Random
    if count < 1:
        raise ValueError("Count must be at least 1.")

    profiles = filter_profiles(browser, os_name, device)

    if not profiles:
        raise ValueError(
            "No profiles match those filters. "
            "Try different browser, OS, or device options."
        )

    rng = random.Random(seed)

    results = []
    while len(results) < count:
        batch = profiles.copy()
        rng.shuffle(batch)
        remaining = count - len(results)
        results.extend(batch[:remaining])

    return [dict(profile) for profile in results]


def generate_selected(browser, os_name, device=None, version=None,
                      count=1, seed=None):
    
    profiles = filter_profiles(browser, os_name, device)

    if version:
        profiles = [p for p in profiles if p["version"] == version]

    if not profiles:
        raise ValueError(
            "Unsupported combination or version. "
            "Use 'list' to inspect available profiles."
        )

    if count < 1:
        raise ValueError("Count must be at least 1.")

    rng = random.Random(seed)
    results = []

    for _ in range(count):
        results.append(dict(rng.choice(profiles)))

    return results


def print_records(records):
    
    for index, record in enumerate(records, start=1):
        print(f"\n[{index}] {record['browser'].upper()} "
              f"{record['version']} | {record['os']} | "
              f"{record['device']}")
        print(record["ua"])


def add_common_filters(parser):
    parser.add_argument(
        "--browser", choices=BROWSERS,
        help="Filter by browser."
    )
    parser.add_argument(
        "--os", dest="os_name", choices=OPERATING_SYSTEMS,
        help="Filter by operating system."
    )
    parser.add_argument(
        "--device", choices=DEVICES,
        help="Filter by device type."
    )
    parser.add_argument(
        "--format", choices=("txt", "json", "csv"),
        default="txt", help="Output format (default: txt)."
    )
    parser.add_argument(
        "--output", "-o",
        help="Write results to a file instead of the terminal."
    )
    parser.add_argument(
        "--seed", type=int,
        help="Seed for reproducible random selection."
    )


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ua-generator",
        description="Generate realistic, curated browser UA profiles.",
        epilog="Profile versions are representative and may be outdated."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    random_parser = subparsers.add_parser(
        "random", help="Randomly select browser profiles."
    )
    random_parser.add_argument(
        "--count", "-n", type=int, default=1,
        help="Number of results (default: 1)."
    )
    add_common_filters(random_parser)

    generate_parser = subparsers.add_parser(
        "generate", help="Generate profiles for selected parameters."
    )
    generate_parser.add_argument(
        "--browser", required=True, choices=BROWSERS
    )
    generate_parser.add_argument(
        "--os", dest="os_name", required=True,
        choices=OPERATING_SYSTEMS
    )
    generate_parser.add_argument(
        "--device", choices=DEVICES,
        help="Device type. If omitted, matching devices are allowed."
    )
    generate_parser.add_argument(
        "--version",
        help="Exact profile version, such as 131 or 17.6."
    )
    generate_parser.add_argument(
        "--count", "-n", type=int, default=1,
        help="Number of results (default: 1)."
    )
    generate_parser.add_argument(
        "--format", choices=("txt", "json", "csv"),
        default="txt"
    )
    generate_parser.add_argument("--output", "-o")
    generate_parser.add_argument("--seed", type=int)

    subparsers.add_parser(
        "list", help="List available curated profiles."
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "list":
            for profile in PROFILES:
                print(
                    f"{profile['id']:<29} "
                    f"{profile['browser']:<8} "
                    f"{profile['os']:<8} "
                    f"{profile['device']:<7} "
                    f"{profile['version']}"
                )
            return 0

        if args.command == "random":
            records = generate_random(
                count=args.count,
                browser=args.browser,
                os_name=args.os_name,
                device=args.device,
                seed=args.seed,
            )
        else:
            records = generate_selected(
                browser=args.browser,
                os_name=args.os_name,
                device=args.device,
                version=args.version,
                count=args.count,
                seed=args.seed,
            )

        if args.output:
            export_records(records, args.format, args.output)
            print(f"Exported {len(records)} profile(s) to {args.output}")
        elif args.format == "txt":
            for record in records:
                print(record["ua"])
        else:
            
            export_records(records, args.format, None)

        return 0

    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
