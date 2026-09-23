#!/usr/bin/env python3
"""
Bug Report CLI
--------------
Interactively collects bug-report information from the user and exports
one or more reports to CSV, JSON, or TXT.

Usage:
    python bug_report_cli.py
    python bug_report_cli.py --format json --output bugs.json
    python bug_report_cli.py --format csv --output bugs.csv --non-interactive-demo
"""

import argparse
import csv
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

FIELDS = [
    "id",
    "title",
    "description",
    "steps_to_reproduce",
    "expected_result",
    "actual_result",
    "severity",
    "priority",
    "status",
    "environment",
    "reporter",
    "date_reported",
]

SEVERITY_CHOICES = ["Low", "Medium", "High", "Critical"]
PRIORITY_CHOICES = ["Low", "Medium", "High", "Urgent"]
STATUS_CHOICES = ["Open", "In Progress", "Resolved", "Closed", "Reopened"]


def ask(prompt, default=None, required=False):
    """Prompt the user for a single line of text."""
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{prompt}{suffix}: ").strip()
        if not value and default is not None:
            return default
        if not value and required:
            print("  This field is required, please enter a value.")
            continue
        return value


def ask_multiline(prompt):
    """Prompt the user for multiple lines of text, ended by a blank line."""
    print(f"{prompt} (end with an empty line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def ask_choice(prompt, choices, default=None):
    """Prompt the user to pick from a fixed set of choices."""
    choice_str = "/".join(choices)
    default = default or choices[0]
    while True:
        value = input(f"{prompt} ({choice_str}) [{default}]: ").strip()
        if not value:
            return default
        for c in choices:
            if value.lower() == c.lower():
                return c
        print(f"  Please choose one of: {choice_str}")


def collect_bug_report():
    """Interactively collect a single bug report."""
    print("\n--- New Bug Report ---")
    report = {
        "id": str(uuid.uuid4())[:8],
        "title": ask("Title", required=True),
        "description": ask_multiline("Description"),
        "steps_to_reproduce": ask_multiline("Steps to reproduce"),
        "expected_result": ask("Expected result"),
        "actual_result": ask("Actual result"),
        "severity": ask_choice("Severity", SEVERITY_CHOICES, default="Medium"),
        "priority": ask_choice("Priority", PRIORITY_CHOICES, default="Medium"),
        "status": ask_choice("Status", STATUS_CHOICES, default="Open"),
        "environment": ask("Environment (OS / browser / version / build)"),
        "reporter": ask("Reporter name", default="Anonymous"),
        "date_reported": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return report


def collect_all_reports():
    """Loop, collecting bug reports until the user is done."""
    reports = []
    while True:
        reports.append(collect_bug_report())
        again = input("\nAdd another bug report? (y/N): ").strip().lower()
        if again != "y":
            break
    return reports


def write_csv(reports, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(reports)


def write_json(reports, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)


def write_txt(reports, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, r in enumerate(reports, 1):
            f.write(f"{'=' * 60}\n")
            f.write(f"BUG REPORT #{i} (ID: {r['id']})\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"Title:               {r['title']}\n")
            f.write(f"Severity / Priority: {r['severity']} / {r['priority']}\n")
            f.write(f"Status:              {r['status']}\n")
            f.write(f"Reporter:            {r['reporter']}\n")
            f.write(f"Date reported:       {r['date_reported']}\n")
            f.write(f"Environment:         {r['environment']}\n")
            f.write("\nDescription:\n")
            f.write(f"  {r['description'] or '(none provided)'}\n")
            f.write("\nSteps to reproduce:\n")
            f.write(f"  {r['steps_to_reproduce'] or '(none provided)'}\n")
            f.write(f"\nExpected result: {r['expected_result']}\n")
            f.write(f"Actual result:   {r['actual_result']}\n")
            f.write("\n\n")


WRITERS = {
    "csv": write_csv,
    "json": write_json,
    "txt": write_txt,
}


def choose_format():
    fmt = ask_choice("Output format", ["csv", "json", "txt"], default="csv")
    return fmt


def default_output_name(fmt):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"bug_report_{stamp}.{fmt}"


def main():
    parser = argparse.ArgumentParser(description="Collect bug reports and export to CSV, JSON, or TXT.")
    parser.add_argument("--format", choices=["csv", "json", "txt"], help="Output format (skips the prompt).")
    parser.add_argument("--output", help="Output file path (skips the prompt).")
    args = parser.parse_args()

    print("Bug Report CLI")
    print("==============")
    reports = collect_all_reports()

    fmt = args.format or choose_format()
    out_path = args.output or ask("Output file name", default=default_output_name(fmt))
    out_path = Path(out_path)

    WRITERS[fmt](reports, out_path)
    print(f"\nSaved {len(reports)} bug report(s) to {out_path.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)