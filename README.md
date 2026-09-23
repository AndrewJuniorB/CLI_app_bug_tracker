# Bug Report CLI

A simple command-line tool for collecting bug reports interactively and exporting them to **CSV**, **JSON**, or **TXT**.

## Features

- Interactive prompts for all standard bug-report fields (title, description, steps to reproduce, expected/actual result, severity, priority, status, environment, reporter, date)
- Add as many bug reports as you want in a single session
- Export to CSV, JSON, or plain-text formats
- Non-interactive mode via CLI flags for scripting/automation
- Auto-generated short unique IDs for each report
- Sensible defaults (e.g. severity defaults to `Medium`, reporter defaults to `Anonymous`)

## Requirements

- Python 3.7+
- No external dependencies (uses only the standard library)

## Usage

### Interactive mode

```bash
python bug_report_cli.py
```

You'll be prompted for each field of a bug report. When done, you can choose to add another, then pick an output format and filename.

### Non-interactive mode

Skip the format/filename prompts by passing them as flags:

```bash
python bug_report_cli.py --format json --output bugs.json
```

| Flag | Description | Choices |
|---|---|---|
| `--format` | Output file format | `csv`, `json`, `txt` |
| `--output` | Output file path | any valid filename/path |

Run `python bug_report_cli.py --help` for full usage details.

## Fields Collected

| Field | Description |
|---|---|
| `id` | Auto-generated 8-character unique ID |
| `title` | Short summary of the bug |
| `description` | Full description (multi-line supported) |
| `steps_to_reproduce` | Steps to trigger the bug (multi-line supported) |
| `expected_result` | What should happen |
| `actual_result` | What actually happens |
| `severity` | `Low` / `Medium` / `High` / `Critical` |
| `priority` | `Low` / `Medium` / `High` / `Urgent` |
| `status` | `Open` / `In Progress` / `Resolved` / `Closed` / `Reopened` |
| `environment` | OS / browser / version info |
| `reporter` | Name of the person reporting the bug |
| `date_reported` | Timestamp, auto-filled at creation time |

## Output Examples

**CSV**
```
id,title,description,...
a1b2c3d4,Login button unresponsive,Clicking login does nothing on Safari,...
```

**JSON**
```json
[
  {
    "id": "a1b2c3d4",
    "title": "Login button unresponsive",
    "severity": "High",
    "priority": "Urgent",
    "status": "Open",
    ...
  }
]
```

**TXT**
```
============================================================
BUG REPORT #1 (ID: a1b2c3d4)
============================================================
Title:               Login button unresponsive
Severity / Priority: High / Urgent
Status:              Open
...
```

## License

_Add your project's license here._
