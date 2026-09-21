#!/usr/bin/env python3
"""Fail the build when the specification corpus under ``specs/`` drifts.

Nothing in ``specs/`` is a business rule until it is complete: the four
artefacts present, a ``## Decision`` block with a real polarity, at least one
proven scenario, and the link between that scenario and its sample files
intact. This tool checks all of that, and regenerates
``docs/00-project/10-decision-log.md`` — the one-page index of every rule,
its polarity and its decision — as a side effect of a clean run.

Usage::

    python tools/check_specs.py

Standard library only: this runs before any environment is set up.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger("check_specs")

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS_ROOT = REPO_ROOT / "specs"
WORK_ROOT = REPO_ROOT / "Work"
DOCS_ROOT = REPO_ROOT / "docs"
DECISION_LOG_PATH = DOCS_ROOT / "00-project" / "10-decision-log.md"

#: 2 MiB. The corpus is ~1.0 MiB today (60 rules, one seed photograph, forged
#: byte-level artefacts). This leaves better than 2x headroom for US-00-23
#: (GPS IFD + real nested zips, both replacing existing small samples rather
#: than adding many new ones) and for the rules F01-F09 will still add,
#: without every batch having to touch this budget.
SPECS_SIZE_BUDGET_BYTES = 2 * 1024 * 1024

DECISION_BLOCK_PATTERN = re.compile(r"## Decision\s*\n```\n(.*?)\n```", re.S)
DECISION_FIELD_PATTERN = re.compile(
    r"^(Status|Decided on|Rationale|Fallback|Revisit if|Supersedes):\s*(.*)$"
)
OWNER_PATTERN = re.compile(r"Owner:\s*(.*)$")
DECISION_REQUIRED_FIELDS = (
    "Status",
    "Decided on",
    "Owner",
    "Rationale",
    "Fallback",
    "Revisit if",
    "Supersedes",
)

TITLE_PATTERN = re.compile(r"^#\s*UC-\d+\s*—\s*(.+)$", re.M)
GROUP_PATTERN = re.compile(r"^\|\s*Group\s*\|\s*`([^`]+)`\s*\|$", re.M)
SCENARIO_PATTERN = re.compile(r"^\s*Scenario:", re.M)

#: Step shapes that name a source file expected to exist under the rule's
#: ``files/``. Drawn from specs/README.md's step vocabulary table (the media
#: under test, the operation's subject, the audited file). Excludes: "target
#: name" steps (RG-3/RG-4 naming outputs, not source files), "the folder ..."
#: steps (directories, not files), "handed the path" (RG-7 escape attempts,
#: deliberately outside the collection), and "the collection of ..." (names
#: the rule itself, not a file).
CITED_FILE_PATTERNS = (
    re.compile(r'\bthe media "([^"]+)"'),
    re.compile(r'\bthe operation on "([^"]+)"'),
    re.compile(r'\bthe metadata audit has recorded "([^"]+)"'),
    re.compile(r'\bthe file is back at "([^"]+)"'),
)
EXCLUDED_CITATION_LINE = re.compile(
    r"target name is|handed the path|\bthe folder \"|the collection of \""
)

UC_ID_PATTERN = re.compile(r"UC-(\d+)")


class Polarity(str, Enum):
    ENFORCED = "Enforced"
    ASSUMED_EXCLUSION = "Assumed exclusion"


#: Invariant 7 (every UC referenced by a lot fiche or a docs/ document): F01
#: through F09 have no fiches yet, so most rules they will implement are
#: unreferenced today. Warning-only would never fail — "a warning in a log
#: protects nothing" is this lot's own rule. Instead: a fixed, named list of
#: today's gaps. It can only shrink (a listed UC that becomes referenced is a
#: stale entry, and the check fails until it is removed) and never grow (an
#: unlisted UC going unreferenced fails immediately).
UNREFERENCED_UC_EXEMPTIONS = frozenset(
    {
        1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 15, 17, 19, 28, 29, 30, 31, 32,
        34, 35, 39, 40, 42, 43, 45, 46, 48, 49, 50, 51, 52, 53,
    }
)

#: Invariant 6 (every files/ sample named by rule.feature): a handful of
#: rules build their scenario around a *companion* file — a sibling .THM, a
#: sidecar .json, the sibling folder that does not flatten, decoy files that
#: only matter as a group for a pruning count. The file's presence is the
#: point; the scenario never needs to quote its name. Rewriting rule.feature
#: to name them is out of scope here (RG-* rule content belongs to US-00-06/
#: US-00-07, and this lot's own "Ne pas faire" forbids acceptance-test
#: changes) — so, like invariant 7, a named, shrinkable exemption list rather
#: than a silently weaker check.
UNCITED_SAMPLE_EXEMPTIONS = frozenset(
    {
        "RG-1-date-resolution/RG-1.2-folder-dates/UC-16-batch-suffix-is-not-a-month/files/2006-1/scan 001.jpg",
        "RG-1-date-resolution/RG-1.3-content-dates/UC-22-video-dated-by-thm-sidecar/files/CANON/MVI_2468.THM",
        "RG-1-date-resolution/RG-1.4-arbitration/UC-56-companion-json-ignored/files/2018-09 Rome/IMG_1234.JPG.json",
        "RG-2-file-classification/UC-38-sidecar-is-not-junk/files/CANON/MVI_3312.AVI",
        "RG-6-organizing/UC-47-flatten-leaves-undated-in-place/files/2011-06 corse/plage.jpg",
        "RG-6-organizing/UC-48-empty-folders-pruned/files/alpha/one.jpg",
        "RG-6-organizing/UC-48-empty-folders-pruned/files/alpha/beta/two.jpg",
        "RG-6-organizing/UC-48-empty-folders-pruned/files/gamma/keep.txt",
        "RG-6-organizing/UC-48-empty-folders-pruned/files/gamma/three.jpg",
    }
)


class SpecError(ValueError):
    """The corpus violates an invariant this tool is willing to enforce."""


@dataclass(frozen=True)
class Decision:
    status: str
    decided_on: str
    owner: str
    rationale: str
    fallback: str
    revisit_if: str
    supersedes: str


@dataclass(frozen=True)
class Rule:
    uc_id: str
    dir_path: Path
    title: str | None
    group: str | None
    decision: Decision | None


def find_rule_dirs(specs_root: Path) -> list[Path]:
    return sorted(p for p in specs_root.glob("**/UC-*") if p.is_dir())


def parse_decision_block(text: str) -> Decision | None:
    match = DECISION_BLOCK_PATTERN.search(text)
    if match is None:
        return None

    fields: dict[str, str] = {}
    current: str | None = None
    for line in match.group(1).splitlines():
        field_match = DECISION_FIELD_PATTERN.match(line)
        if field_match:
            label, value = field_match.groups()
            if label == "Decided on":
                owner_match = OWNER_PATTERN.search(value)
                if owner_match:
                    fields["Owner"] = owner_match.group(1).strip()
                    value = value[: owner_match.start()].strip()
            fields[label] = value.strip()
            current = label
        elif current is not None and line.strip():
            fields[current] = f"{fields[current]} {line.strip()}"

    if any(not fields.get(name) for name in DECISION_REQUIRED_FIELDS):
        return None

    return Decision(
        status=fields["Status"],
        decided_on=fields["Decided on"],
        owner=fields["Owner"],
        rationale=fields["Rationale"],
        fallback=fields["Fallback"],
        revisit_if=fields["Revisit if"],
        supersedes=fields["Supersedes"],
    )


def cited_files(feature_text: str) -> set[str]:
    cited: set[str] = set()
    for line in feature_text.splitlines():
        if EXCLUDED_CITATION_LINE.search(line):
            continue
        for pattern in CITED_FILE_PATTERNS:
            for found in pattern.finditer(line):
                cited.add(found.group(1))
    return cited


def check_rule(rule_dir: Path) -> tuple[Rule, list[str]]:
    """Check the four artefacts and the invariants local to one rule (1-6).

    Returns the parsed ``Rule`` (for the decision log) and the list of
    problems found, each naming the offending file and the violated rule.
    """
    relative = rule_dir.relative_to(SPECS_ROOT).as_posix()
    uc_id = rule_dir.name.split("-", 2)[0] + "-" + rule_dir.name.split("-", 2)[1]
    problems: list[str] = []

    rule_md = rule_dir / "rule.md"
    rule_feature = rule_dir / "rule.feature"
    samples_toml = rule_dir / "samples.toml"
    files_dir = rule_dir / "files"

    for artefact, path in (
        ("rule.md", rule_md),
        ("rule.feature", rule_feature),
        ("samples.toml", samples_toml),
    ):
        if not path.is_file():
            problems.append(f"{relative}: invariant 1 (four artefacts) - missing {artefact}")
    if not files_dir.is_dir():
        problems.append(f"{relative}: invariant 1 (four artefacts) - missing files/")

    title: str | None = None
    group: str | None = None
    decision: Decision | None = None

    if rule_md.is_file():
        text = rule_md.read_text(encoding="utf-8")
        title_match = TITLE_PATTERN.search(text)
        title = title_match.group(1).strip() if title_match else None
        group_match = GROUP_PATTERN.search(text)
        group = group_match.group(1).strip() if group_match else None

        decision = parse_decision_block(text)
        if decision is None:
            problems.append(f"{relative}/rule.md: invariant 2 (Decision block) - missing or incomplete")
        elif decision.status not in (Polarity.ENFORCED.value, Polarity.ASSUMED_EXCLUSION.value):
            problems.append(
                f"{relative}/rule.md: invariant 3 (polarity) - Status is {decision.status!r}, "
                f"must be 'Enforced' or 'Assumed exclusion'"
            )

    if rule_feature.is_file():
        feature_text = rule_feature.read_text(encoding="utf-8")
        if not SCENARIO_PATTERN.search(feature_text):
            problems.append(f"{relative}/rule.feature: invariant 4 (at least one scenario) - none found")

        if files_dir.is_dir():
            cited = cited_files(feature_text)
            on_disk = {p.relative_to(files_dir).as_posix() for p in files_dir.rglob("*") if p.is_file()}

            for name in sorted(cited - on_disk):
                problems.append(
                    f"{relative}/rule.feature: invariant 5 (cited file exists) - "
                    f"\"{name}\" is not under {relative}/files/"
                )
            for name in sorted(on_disk - cited):
                key = f"{relative}/files/{name}"
                if key in UNCITED_SAMPLE_EXEMPTIONS:
                    continue
                problems.append(
                    f"{relative}/files/{name}: invariant 6 (no orphan sample) - "
                    f"not named by any step in {relative}/rule.feature"
                )

    rule = Rule(uc_id=uc_id, dir_path=rule_dir, title=title, group=group, decision=decision)
    return rule, problems


def referenced_uc_ids() -> set[str]:
    """UC ids cited by a lot fiche (``Work/**/Plan/US-*.md``, not ``brief/``) or a docs/ page."""
    referenced: set[str] = set()

    fiche_paths = [
        p
        for p in WORK_ROOT.glob("**/Plan/US-*.md")
        if "brief" not in p.relative_to(WORK_ROOT).parts
    ]
    doc_paths = [p for p in DOCS_ROOT.glob("**/*.md") if p != DECISION_LOG_PATH] if DOCS_ROOT.is_dir() else []

    for path in fiche_paths + doc_paths:
        for match in UC_ID_PATTERN.finditer(path.read_text(encoding="utf-8")):
            referenced.add(f"UC-{match.group(1)}")
    return referenced


def check_referenced(rules: list[Rule]) -> list[str]:
    referenced = referenced_uc_ids()
    problems: list[str] = []

    all_ids = {rule.uc_id for rule in rules}
    exempted_ids = {f"UC-{n:02d}" for n in UNREFERENCED_UC_EXEMPTIONS}

    for rule in rules:
        exempted = rule.uc_id in exempted_ids
        is_referenced = rule.uc_id in referenced
        if not is_referenced and not exempted:
            problems.append(
                f"{rule.dir_path.relative_to(SPECS_ROOT).as_posix()}: invariant 7 (referenced) - "
                f"not cited by any lot fiche or docs/ page, and not in UNREFERENCED_UC_EXEMPTIONS"
            )
        if is_referenced and exempted:
            problems.append(
                f"{rule.dir_path.relative_to(SPECS_ROOT).as_posix()}: invariant 7 (referenced) - "
                f"now referenced; remove {rule.uc_id} from UNREFERENCED_UC_EXEMPTIONS"
            )

    stale_exemptions = exempted_ids - all_ids
    for uc_id in sorted(stale_exemptions):
        problems.append(f"UNREFERENCED_UC_EXEMPTIONS: invariant 7 (referenced) - {uc_id} no longer exists")

    return problems


def check_size_budget() -> list[str]:
    total = sum(p.stat().st_size for p in SPECS_ROOT.rglob("*") if p.is_file())
    if total > SPECS_SIZE_BUDGET_BYTES:
        return [
            f"specs/: invariant 9 (size budget) - {total} bytes exceeds the "
            f"{SPECS_SIZE_BUDGET_BYTES} byte budget"
        ]
    logger.info("specs/ is %d bytes (%.2f MiB), budget is %.0f MiB", total, total / 2**20, SPECS_SIZE_BUDGET_BYTES / 2**20)
    return []


def format_decision_log(rules: list[Rule]) -> str:
    lines = [
        "# Decision log — specification corpus",
        "",
        "> **Generated by `tools/check_specs.py`. Do not hand-edit.** The source of",
        "> truth for any rule is its own `rule.md`; this page is a derived index —",
        "> regenerate it by running the checker again.",
        "",
        "| UC | Rule | Group | Polarity | Decided on | Owner | Revisit if |",
        "|---|---|---|---|---|---|---|",
    ]
    for rule in sorted(rules, key=lambda r: int(r.uc_id.split("-")[1])):
        if rule.decision is None:
            continue
        polarity_mark = "▶" if rule.decision.status == Polarity.ENFORCED.value else "⊘"
        title = rule.title or ""
        group = rule.group or ""
        lines.append(
            f"| {rule.uc_id} | {title} | {group} | {rule.decision.status} {polarity_mark} "
            f"| {rule.decision.decided_on} | {rule.decision.owner} | {rule.decision.revisit_if} |"
        )
    lines.append("")

    enforced = sum(1 for r in rules if r.decision and r.decision.status == Polarity.ENFORCED.value)
    excluded = sum(1 for r in rules if r.decision and r.decision.status == Polarity.ASSUMED_EXCLUSION.value)
    lines.insert(6, f"{len(rules)} rules: {enforced} enforced, {excluded} assumed exclusions.")
    lines.insert(7, "")

    return "\n".join(lines) + "\n"


def run_check() -> int:
    rule_dirs = find_rule_dirs(SPECS_ROOT)
    if not rule_dirs:
        logger.error("no UC-* rule directory found under %s", SPECS_ROOT)
        return 2

    problems: list[str] = []
    rules: list[Rule] = []
    for rule_dir in rule_dirs:
        rule, rule_problems = check_rule(rule_dir)
        rules.append(rule)
        problems.extend(rule_problems)

    problems.extend(check_referenced(rules))
    problems.extend(check_size_budget())

    DECISION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DECISION_LOG_PATH.write_text(format_decision_log(rules), encoding="utf-8")
    logger.info("wrote %s", DECISION_LOG_PATH)

    logger.info(
        "invariant 8 (seed carries no metadata) is enforced separately by "
        "'python tools/strip_exif.py --check specs/_seed/river.jpg'"
    )

    if problems:
        for problem in problems:
            logger.error(problem)
        logger.error("%d problem(s) found across %d rule(s)", len(problems), len(rule_dirs))
        return 1

    logger.info("%d rule(s) checked, no problems found", len(rule_dirs))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)

    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
