#!/usr/bin/env python3
"""
BreachRadar - Offline-safe password breach checker.

Checks whether a password has appeared in known public data breaches
using the "Have I Been Pwned" k-Anonymity API. Your full password is
NEVER sent over the network: only the first 5 characters of its SHA-1
hash are transmitted, and the match is confirmed locally.

Usage:
    python breachradar.py                  # interactive prompt (hidden input)
    python breachradar.py --password "x"   # check a single password (not recommended on shared machines)
    python breachradar.py --file passwords.txt   # check a list, one per line
"""

import argparse
import getpass
import hashlib
import sys
import time
from dataclasses import dataclass
from typing import Optional

import requests

HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{prefix}"
REQUEST_TIMEOUT = 10
USER_AGENT = "BreachRadar-CLI/1.0 (+https://github.com/Syed-Muhammad-Tayyab/BreachRadar)"


@dataclass
class CheckResult:
    password_label: str
    breached: bool
    times_seen: int
    error: Optional[str] = None


def sha1_upper(password: str) -> str:
    """Return the uppercase SHA-1 hex digest of a password."""
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


def query_hibp_range(prefix: str) -> str:
    """
    Query the HIBP k-Anonymity range endpoint for a 5-character
    SHA-1 prefix and return the raw response body (suffix:count lines).
    """
    headers = {"User-Agent": USER_AGENT, "Add-Padding": "true"}
    response = requests.get(
        HIBP_RANGE_URL.format(prefix=prefix),
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.text


def check_password(password: str, label: Optional[str] = None) -> CheckResult:
    """
    Check a single password against the HIBP breach database.
    Only the first 5 hash characters ever leave the machine.
    """
    label = label or "********"
    try:
        digest = sha1_upper(password)
        prefix, suffix = digest[:5], digest[5:]
        body = query_hibp_range(prefix)

        for line in body.splitlines():
            if ":" not in line:
                continue
            hash_suffix, count = line.strip().split(":")
            if hash_suffix == suffix:
                return CheckResult(label, True, int(count))

        return CheckResult(label, False, 0)

    except requests.exceptions.RequestException as exc:
        return CheckResult(label, False, 0, error=f"network error: {exc}")
    except Exception as exc:  # noqa: BLE001
        return CheckResult(label, False, 0, error=str(exc))


def format_result(result: CheckResult) -> str:
    if result.error:
        return f"[!] {result.password_label}: could not check ({result.error})"
    if result.breached:
        return (
            f"[X] {result.password_label}: FOUND in breaches "
            f"({result.times_seen:,} times) — change it immediately"
        )
    return f"[OK] {result.password_label}: not found in known breaches"


def run_file_mode(path: str) -> int:
    exit_code = 0
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = [line.rstrip("\n") for line in handle if line.strip()]
    except OSError as exc:
        print(f"[!] Could not read file '{path}': {exc}", file=sys.stderr)
        return 2

    print(f"Checking {len(lines)} password(s) from '{path}'...\n")
    for i, pwd in enumerate(lines, start=1):
        result = check_password(pwd, label=f"line {i}")
        print(format_result(result))
        if result.breached:
            exit_code = 1
        time.sleep(0.1)  # be polite to the public API
    return exit_code


def run_single_mode(password: str) -> int:
    result = check_password(password)
    print(format_result(result))
    return 1 if result.breached else 0


def run_interactive_mode() -> int:
    try:
        password = getpass.getpass("Enter password to check (input hidden): ")
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        return 130
    if not password:
        print("No password entered.")
        return 2
    return run_single_mode(password)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="breachradar",
        description="Check if a password has appeared in known data breaches (via HIBP k-Anonymity API).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--password", help="Check a single password (visible in shell history — use with care).")
    group.add_argument("--file", help="Path to a text file with one password per line.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.file:
        sys.exit(run_file_mode(args.file))
    elif args.password:
        sys.exit(run_single_mode(args.password))
    else:
        sys.exit(run_interactive_mode())


if __name__ == "__main__":
    main()
