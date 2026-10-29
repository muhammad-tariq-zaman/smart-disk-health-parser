"""Parse `smartctl -a` output and summarise disk health.

Usage: python3 main.py smartctl-output.txt
"""
import argparse
import re
import sys


def _search(pattern, text):
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None


def parse_smart(text):
    """Extract model, serial, health result and key SMART attributes."""
    attrs = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 10 and parts[0].isdigit():
            attrs[parts[1]] = parts[9]
    health = _search(r"SMART overall-health self-assessment test result:\s*(\S+)", text)
    reallocated = int(attrs.get("Reallocated_Sector_Ct", "0") or 0)
    pending = int(attrs.get("Current_Pending_Sector", "0") or 0)
    if health and health.upper() != "PASSED":
        verdict = "FAIL"
    elif reallocated > 0 or pending > 0:
        verdict = "WARNING"
    else:
        verdict = "OK"
    return {
        "model": _search(r"Device Model:\s*(.+)", text),
        "serial": _search(r"Serial Number:\s*(\S+)", text),
        "health": health,
        "reallocated_sectors": reallocated,
        "pending_sectors": pending,
        "power_on_hours": attrs.get("Power_On_Hours"),
        "temperature_celsius": attrs.get("Temperature_Celsius"),
        "verdict": verdict,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to smartctl output text")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        result = parse_smart(f.read())
    for key, value in result.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
