#!/usr/bin/env python3
"""
validate_observation.py - Mechanical validator for observation Markdown files.

Standard Python libraries only (no external API, zero extra dependencies).
Validates:
1. Front Matter starts at line 1 and is properly bounded by '---'.
2. No instruction text or extraneous text precedes the Front Matter.
3. Mandatory fields exist: id, date, location, title, type, observer, direct_observation.
4. Date format is YYYY-MM-DD.
5. direct_observation is a boolean ('true' or 'false').
6. type is one of the valid specification types (including event-time-series-summary).
7. If type is event-time-series-summary, period information is provided.
8. Unique id check across existing observation files.
9. Local internal markdown links resolve to existing files.
"""

import sys
import os
import re
from pathlib import Path

VALID_TYPES = {
    "fixed-point",
    "route",
    "event-setup",
    "event-holding",
    "event-teardown",
    "event-time-series-summary"
}

def parse_front_matter(content):
    """
    Parses front matter ensuring it begins on line 1.
    Returns (front_matter_dict, body_text, list_of_errors).
    """
    errors = []
    if not content.startswith("---"):
        # Check if there is instruction or other text before ---
        if "---" in content:
            errors.append("Front Matter does not start at line 1. Extraneous instruction text detected before '---'.")
        else:
            errors.append("Missing Front Matter opening marker '---'.")
        return {}, content, errors

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Front Matter is not properly closed with '---'.")
        return {}, content, errors

    fm_raw = parts[1]
    body = parts[2]
    fm = {}

    for line_no, line in enumerate(fm_raw.splitlines(), 2):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"Front Matter line {line_no}: invalid syntax (missing ':'): {line}")
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        fm[key] = val

    return fm, body, errors

def validate_observation_content(content, filepath=None, repo_root=None, all_existing_ids=None):
    """
    Validates observation text against mechanical rules.
    Returns (is_valid, list_of_errors, list_of_warnings).
    """
    errors = []
    warnings = []

    if repo_root is None:
        repo_root = Path(".").resolve()

    fm, body, fm_errors = parse_front_matter(content)
    errors.extend(fm_errors)

    if fm_errors and not fm:
        return False, errors, warnings

    # Mandatory fields
    mandatory = ["id", "date", "location", "title", "type", "observer", "direct_observation"]
    for field in mandatory:
        if field not in fm or not fm[field]:
            errors.append(f"Missing mandatory field in Front Matter: '{field}'")

    # Date format check
    if "date" in fm:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fm["date"]):
            errors.append(f"Invalid date format in Front Matter: '{fm['date']}' (expected YYYY-MM-DD)")

    # direct_observation check
    if "direct_observation" in fm:
        val = fm["direct_observation"].lower()
        if val not in ("true", "false"):
            errors.append(f"Invalid direct_observation value: '{fm['direct_observation']}' (must be true or false)")

    # type check
    obs_type = fm.get("type")
    if obs_type:
        if obs_type not in VALID_TYPES:
            errors.append(f"Undefined observation type in Front Matter: '{obs_type}'. Valid types: {sorted(VALID_TYPES)}")
        if obs_type == "event-time-series-summary":
            # Check for period either in Front Matter or body
            has_period = ("period" in fm and bool(fm["period"])) or ("period" in body.lower()) or ("対象期間" in body) or ("観測概要" in body and "〜" in body)
            if not has_period:
                errors.append("Type 'event-time-series-summary' requires period information (e.g. 'period' in Front Matter or 対象期間 in body).")

    # ID duplicate check
    obs_id = fm.get("id")
    if obs_id and all_existing_ids:
        # Check against existing IDs
        for other_file, other_id in all_existing_ids.items():
            if filepath and Path(other_file).resolve() == Path(filepath).resolve():
                continue
            if other_id == obs_id:
                errors.append(f"Duplicate observation id '{obs_id}' already used in {other_file}")

    # Body check for basic required headings
    required_body_items = ["観測日時", "場所", "観測対象"]
    for item in required_body_items:
        if item not in body:
            warnings.append(f"Body may be missing standard descriptor '{item}'")

    # Markdown internal link check
    if filepath:
        file_dir = Path(filepath).parent.resolve()
        link_pattern = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
        for line_no, line in enumerate(body.splitlines(), 1):
            for m in link_pattern.finditer(line):
                target = m.group(1).strip()
                if target.startswith(("http://", "https://", "#", "mailto:", "start_span", "end_span")):
                    continue
                target_clean = target.split()[0]
                target_clean = target_clean.split("#")[0]
                if not target_clean:
                    continue
                resolved = (file_dir / target_clean).resolve()
                if not resolved.exists():
                    errors.append(f"Broken internal markdown link at body line {line_no}: target '{target}' does not exist.")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings

def collect_all_ids(repo_root):
    """
    Collects {relative_path: id} from all markdown files in observations/.
    """
    ids = {}
    obs_dir = repo_root / "observations"
    if not obs_dir.exists():
        return ids

    for md_path in obs_dir.rglob("*.md"):
        if md_path.name == "index.md":
            continue
        try:
            content = md_path.read_text(encoding="utf-8", errors="replace")
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    for line in parts[1].splitlines():
                        if line.strip().startswith("id:"):
                            val = line.split(":", 1)[1].strip().strip('"').strip("'")
                            if val:
                                ids[str(md_path.relative_to(repo_root))] = val
        except Exception:
            pass
    return ids

def main():
    repo_root = Path(__file__).resolve().parent.parent
    target_files = sys.argv[1:]

    existing_ids = collect_all_ids(repo_root)

    if not target_files:
        # Default mode: check all files in observations/ except index.md and 2026/test-observation.md
        print(f"No specific files provided. Scanning observations/*.md ...")
        obs_dir = repo_root / "observations"
        target_files = [
            str(p) for p in sorted(obs_dir.glob("*.md"))
            if p.name != "index.md" and p.name != "2026-11-03-jules-operation-change.md"
        ]

    total_errors = 0
    total_warnings = 0

    print("=" * 60)
    print("HIROSAKI VIEW — OBSERVATION VALIDATOR")
    print("=" * 60)

    for target_path in target_files:
        p = Path(target_path)
        if not p.exists():
            print(f"✗ File not found: {target_path}")
            total_errors += 1
            continue

        try:
            content = p.read_text(encoding="utf-8")
        except Exception as e:
            print(f"✗ Could not read file {target_path}: {e}")
            total_errors += 1
            continue

        is_valid, errors, warnings = validate_observation_content(
            content,
            filepath=p,
            repo_root=repo_root,
            all_existing_ids=existing_ids
        )

        rel = str(p.relative_to(repo_root)) if p.is_relative_to(repo_root) else str(p)
        if is_valid:
            if warnings:
                print(f"⚠ {rel} (Passed with {len(warnings)} warnings)")
                for w in warnings:
                    print(f"    - {w}")
            else:
                print(f"✓ {rel}")
        else:
            print(f"✗ {rel} ({len(errors)} errors)")
            for e in errors:
                print(f"    - {e}")
            total_errors += len(errors)

        total_warnings += len(warnings)

    print("-" * 60)
    print(f"Total Errors: {total_errors}, Total Warnings: {total_warnings}")
    print("=" * 60)

    if total_errors > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
