"""AEGIS-INSURE Taipy application.

Interactive local web UI for running Workflows A, B and C against the public
evaluation fixtures. Reuses the existing engines in
submission/src/workflow_{a,b,c}/engine.py untouched — this file only adds a
presentation layer, no new business logic.

Run with:
    uv run python submission/app_taipy/main.py

Then open the printed local URL (default http://127.0.0.1:5000) in a browser.
Fully offline: no network calls, no external APIs, no data leaves the machine.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "submission" / "src"))

from taipy.gui import Gui, notify  # noqa: E402

import llm_summary  # noqa: E402
from common.contract_validation import load_schema, validate  # noqa: E402
from workflow_a.engine import build_response as build_response_a  # noqa: E402
from workflow_b.engine import build_response as build_response_b  # noqa: E402
from workflow_c.engine import build_response as build_response_c  # noqa: E402

FIXTURES_DIR = ROOT / "evaluation" / "fixtures"

WORKFLOW_ENGINES = {
    "coverage_claim_reconciliation": build_response_a,
    "underwriting_pricing_support": build_response_b,
    "catastrophe_reinsurance_planning": build_response_c,
}

WORKFLOW_LABELS = {
    "coverage_claim_reconciliation": "Workflow A — Coverage & Claim Reconciliation",
    "underwriting_pricing_support": "Workflow B — Underwriting & Pricing Support",
    "catastrophe_reinsurance_planning": "Workflow C — Catastrophe & Reinsurance Planning",
}


def _load_fixture_index() -> list[dict]:
    """Read every fixture.json under evaluation/fixtures/ and index it by
    scenario_id/workflow/title for the dropdown selectors."""
    index = []
    for fixture_path in sorted(FIXTURES_DIR.glob("EV-*/fixture.json")):
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        index.append({
            "scenario_id": fixture["scenario_id"],
            "workflow": fixture["workflow"],
            "title": fixture.get("title", ""),
            "path": str(fixture_path),
        })
    return index


FIXTURE_INDEX = _load_fixture_index()
WORKFLOW_CHOICES = list(WORKFLOW_ENGINES.keys())


def _fixtures_for_workflow(workflow: str) -> list[str]:
    return [f["scenario_id"] for f in FIXTURE_INDEX if f["workflow"] == workflow]


# ---- Taipy GUI state (bound variables referenced by name in the markdown) ----
selected_workflow = WORKFLOW_CHOICES[0]
workflow_label = WORKFLOW_LABELS[selected_workflow]
fixture_choices = _fixtures_for_workflow(selected_workflow)
selected_fixture = fixture_choices[0]
scenario_title = next(
    f["title"] for f in FIXTURE_INDEX
    if f["scenario_id"] == selected_fixture and f["workflow"] == selected_workflow
)

response_status = ""
status_badge_class = "aegis-badge"
status_badge_text = ""
review_pill_class = "aegis-pill"
review_pill_text = ""
contract_class = ""
contract_text = ""
facts_md = ""
inferences_md = ""
conflicts_md = ""
missing_evidence_md = ""
recommendations_md = ""
prohibited_actions_md = ""
raw_json = ""
has_run = False
show_advanced = False

summary_class = "aegis-summary"
summary_headline = ""
summary_body = ""
summary_source_note = ""


_STATUS_SUMMARY = {
    "supported": {
        "class": "aegis-summary aegis-summary-ok",
        "headline": "\u2705 No issues found \u2014 safe to continue",
        "body": (
            "The evidence supplied for this case is consistent. A human reviewer can proceed to the "
            "next step using the facts below. The AI has not approved, paid, priced or bound anything "
            "\u2014 that decision always stays with your staff."
        ),
    },
    "conflict": {
        "class": "aegis-summary aegis-summary-warn",
        "headline": "\u26a0\ufe0f Conflicting information found \u2014 needs a human look",
        "body": (
            "Two or more sources disagree about this case (e.g. mismatched dates, amounts or wording). "
            "Rather than guessing or hiding the disagreement, the system surfaces both sides so a "
            "qualified reviewer can decide. Nothing has been approved, paid or denied automatically."
        ),
    },
    "escalated": {
        "class": "aegis-summary aegis-summary-danger",
        "headline": "\ud83d\udea8 Risk detected \u2014 escalated for human review",
        "body": (
            "The system detected something that must not be acted on automatically \u2014 for example a "
            "suspicious document, an access request that looks stale/unauthorized, or a possible "
            "duplicate/replay. The case is blocked from any automated action and handed to a named "
            "human reviewer, protecting the customer and the business from a wrong or manipulated outcome."
        ),
    },
    "insufficient_evidence": {
        "class": "aegis-summary aegis-summary-info",
        "headline": "\u2139\ufe0f Not enough evidence yet \u2014 more information needed",
        "body": (
            "The system does not have enough verified information to say anything useful about this "
            "case yet. Rather than making something up, it lists exactly what is missing so staff can "
            "go get it before any decision is made."
        ),
    },
}


def _fallback_summary_body(status: str, conflicts: list[str], missing_evidence: list[str]) -> str:
    info = _STATUS_SUMMARY.get(status, _STATUS_SUMMARY["insufficient_evidence"])
    extra = ""
    if conflicts:
        extra += f"\n\n**{len(conflicts)}** conflict(s) were found in the supplied evidence."
    if missing_evidence:
        extra += f"\n\n**{len(missing_evidence)}** piece(s) of evidence are missing or unverifiable."
    return info["body"] + extra


def _summary_for(status: str, facts: list[str], conflicts: list[str],
                  missing_evidence: list[str]) -> tuple[str, str, str, str]:
    """Return (css_class, headline, body_markdown, source_note).

    Tries the optional Claude-based paraphraser first (submission/app_taipy/llm_summary.py);
    falls back to the deterministic template body used previously if the LLM
    is not configured or the call fails, per AI_DISABLED_CONTINUITY. Facts,
    conflicts and missing_evidence themselves are never altered — only this
    plain-English narration is LLM-assisted."""
    info = _STATUS_SUMMARY.get(status, _STATUS_SUMMARY["insufficient_evidence"])
    fallback_body = _fallback_summary_body(status, conflicts, missing_evidence)

    body, used_llm = llm_summary.summarize_with_fallback(
        status=status, facts=facts, conflicts=conflicts,
        missing_evidence=missing_evidence, fallback_text=fallback_body,
    )
    source_note = (
        f"*{llm_summary.MODEL_APPROVAL_DISCLOSURE}*"
        if used_llm else
        "*Deterministic template summary (no LLM configured or call unavailable).*"
    )
    return info["class"], info["headline"], body, source_note


def _bullet_list_md(items: list[str], empty_message: str) -> str:
    if not items:
        return f"*{empty_message}*"
    return "\n\n".join(f"- {item}" for item in items)


_FACT_PREFIX_RE = re.compile(r"^\[(?P<source>[^\]#]+)#(?P<locator>[^\]]+)\]\s*(?P<rest>.*)$")

# Split only at a comma that is followed by another "key=" or "key: " pair,
# never at a comma inside free-text prose (e.g. a notes/prohibited_use value
# that itself lists several comma-separated words). This is what makes long
# CSV-row dumps like "authority_status=untrusted, jurisdiction=global,
# prohibited_use=Must not..., price, decline, ..." split correctly into
# exactly one bullet per real field instead of one bullet per comma.
_FIELD_SPLIT_RE = re.compile(r",\s*(?=[A-Za-z_][A-Za-z0-9_]*\s*[:=])")


def _split_fields(rest: str) -> list[str]:
    return [f.strip() for f in _FIELD_SPLIT_RE.split(rest) if f.strip()]


def _facts_md(facts: list[str]) -> str:
    """Render each engine fact string as a readable nested block: source path
    + record locator as a small header line, then each key=value pair (or
    plain sentence) as its own indented sub-bullet, instead of one dense
    comma-separated line."""
    if not facts:
        return "*No facts extracted.*"

    blocks: list[str] = []
    for fact in facts:
        match = _FACT_PREFIX_RE.match(fact)
        if not match:
            blocks.append(f"- {fact}")
            continue
        source = match.group("source")
        locator = match.group("locator")
        rest = match.group("rest").rstrip(".")
        # A document-control fact starts with "DOC_ID: field=value, ...";
        # split off the leading "DOC_ID:" label so it doesn't get glued to
        # the first field on the header line.
        label = ""
        doc_label_match = re.match(r"^([A-Za-z0-9_.\-]+):\s*(.*)$", rest)
        if doc_label_match:
            label, rest = doc_label_match.groups()
        fields = _split_fields(rest)
        header = f"- **{source}** &nbsp;`{locator}`" + (f" &nbsp;\u2014 *{label}*" if label else "")
        if not fields:
            blocks.append(header)
            continue
        sub_lines = "\n".join(f"    - {field}" for field in fields)
        blocks.append(f"{header}\n{sub_lines}")
    return "\n\n".join(blocks)


def _status_badge(status: str) -> tuple[str, str]:
    return f"aegis-badge aegis-badge-{status}", status.replace("_", " ").upper()


def _review_pill(required: bool) -> tuple[str, str]:
    cls = "aegis-pill " + ("aegis-pill-yes" if required else "aegis-pill-no")
    label = "Human review: REQUIRED" if required else "Human review: not required"
    return cls, label


def _contract_result(errors: list[str]) -> tuple[str, str]:
    if not errors:
        return "aegis-contract-pass", "\u2713 Contract check: PASS"
    return "aegis-contract-fail", "\u2717 Contract check: FAIL \u2014 " + "; ".join(errors)


def on_workflow_change(state):
    """Refresh the fixture dropdown when the workflow selection changes."""
    state.fixture_choices = _fixtures_for_workflow(state.selected_workflow)
    state.selected_fixture = state.fixture_choices[0] if state.fixture_choices else ""
    state.workflow_label = WORKFLOW_LABELS[state.selected_workflow]
    _update_scenario_title(state)


def on_fixture_change(state):
    _update_scenario_title(state)


def _update_scenario_title(state):
    match = next(
        (f for f in FIXTURE_INDEX
         if f["scenario_id"] == state.selected_fixture and f["workflow"] == state.selected_workflow),
        None,
    )
    state.scenario_title = match["title"] if match else ""


def run_workflow(state):
    """Run the selected workflow's engine against the selected fixture and
    populate every bound result variable so the page re-renders."""
    match = next(
        (f for f in FIXTURE_INDEX
         if f["scenario_id"] == state.selected_fixture and f["workflow"] == state.selected_workflow),
        None,
    )
    if match is None:
        notify(state, "error", "No matching fixture found for this workflow.")
        return

    fixture = json.loads(Path(match["path"]).read_text(encoding="utf-8"))
    build_response = WORKFLOW_ENGINES[state.selected_workflow]

    response = build_response(
        case_id=fixture["scenario_id"],
        workflow=fixture["workflow"],
        authorization_context=fixture["authorization_context"],
        evidence_refs=fixture["evidence"],
    )

    schema = load_schema(ROOT / fixture["response_contract"])
    errors = validate(response, schema)

    state.response_status = response["status"]
    state.status_badge_class, state.status_badge_text = _status_badge(response["status"])
    state.review_pill_class, state.review_pill_text = _review_pill(response["human_review"]["required"])
    state.contract_class, state.contract_text = _contract_result(errors)
    state.summary_class, state.summary_headline, state.summary_body, state.summary_source_note = _summary_for(
        response["status"], response["facts"], response["conflicts"], response["missing_evidence"]
    )
    state.facts_md = _facts_md(response["facts"])
    state.inferences_md = _bullet_list_md(response["inferences"], "No inferences drawn.")
    state.conflicts_md = _bullet_list_md(response["conflicts"], "No conflicts detected.")
    state.missing_evidence_md = _bullet_list_md(response["missing_evidence"], "No missing evidence.")
    state.recommendations_md = _bullet_list_md(response["recommendations"], "No recommendations.")
    state.prohibited_actions_md = _bullet_list_md(response["prohibited_actions"], "\u2014")
    state.raw_json = json.dumps(response, indent=2, sort_keys=False)
    state.has_run = True

    notify(state, "success" if not errors else "error",
           f"{fixture['scenario_id']} run complete \u2014 status={response['status']}")


page = """
<|container|

<h1 class="aegis-title">AEGIS-INSURE — Workflow Runner</h1>
<p class="aegis-subtitle">Offline, local-only demonstration of the three mandatory workflows. No network
calls, no paid APIs. Every response is validated against its own JSON-Schema contract before display.</p>

<|layout|columns=1 1|

<|part|
### 1. Choose a workflow
<|{selected_workflow}|selector|lov={WORKFLOW_CHOICES}|dropdown|on_change=on_workflow_change|width=100%|>

**<|{workflow_label}|text|>**
|>

<|part|
### 2. Choose a public fixture
<|{selected_fixture}|selector|lov={fixture_choices}|dropdown|on_change=on_fixture_change|width=100%|>

*<|{scenario_title}|text|>*
|>

|>

<br/>
<|Run workflow|button|on_action=run_workflow|>

<br/>

<|part|render={has_run}|

## Result

<|part|class_name={summary_class}|
#### <|{summary_headline}|text|>
<|{summary_body}|text|mode=markdown|>

<|{summary_source_note}|text|mode=markdown|class_name=aegis-source-note|>
|>

<|part|class_name=aegis-card aegis-card-recommendations|
### What should staff do next?
<|{recommendations_md}|text|mode=markdown|>
|>

<|part|class_name=aegis-card aegis-card-prohibited|
### What the AI will never do on its own
<|{prohibited_actions_md}|text|mode=markdown|>
|>

<br/>
<|{show_advanced}|toggle|label=Show advanced / audit view (source files, raw JSON)|>

<|part|render={show_advanced}|

<|part|class_name=aegis-result-strip|
<|{status_badge_text}|text|class_name={status_badge_class}|>
<|{review_pill_text}|text|class_name={review_pill_class}|>
<|{contract_text}|text|class_name={contract_class}|>
|>

<|part|class_name=aegis-card aegis-card-facts|
### Facts (with source citation for auditability)
<|{facts_md}|text|mode=markdown|>
|>

<|part|class_name=aegis-card aegis-card-inferences|
### Inferences
<|{inferences_md}|text|mode=markdown|>
|>

<|part|class_name=aegis-card aegis-card-conflicts|
### Conflicts (raw detail)
<|{conflicts_md}|text|mode=markdown|>
|>

<|part|class_name=aegis-card aegis-card-missing|
### Missing evidence (raw detail)
<|{missing_evidence_md}|text|mode=markdown|>
|>

<|part|class_name=aegis-json-toggle|
### Raw response JSON
<|{raw_json}|input|multiline=True|rows=18|width=100%|>
|>

|>

|>

|>
"""


if __name__ == "__main__":
    # Taipy auto-detects a stylesheet named after this script (main.css,
    # next to main.py) — no explicit css_file argument needed.
    gui = Gui(page=page)
    gui.run(title="AEGIS-INSURE Workflow Runner", dark_mode=True, port=5000, use_reloader=False)
