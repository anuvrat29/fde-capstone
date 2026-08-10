# AEGIS-INSURE Taipy UI

Python-only interactive runner for Workflows A, B and C. Calls the engines in
`submission/src/workflow_{a,b,c}/` in-process — no Node.js, npm, Vite, React or
separate HTTP API.

## Run

```bash
python submission/scripts/run_taipy.py
# or
python submission/app_taipy/main.py
```

Open `http://127.0.0.1:5000`.

## Dependencies

| Package | Required? | Purpose |
|---|---|---|
| `taipy` | Yes | GUI |
| `anthropic` | Optional | GEN-SUM-3 plain-English paraphrase when `CLAUDE_KEY` is set in repo-root `.env` |

Without an API key the UI keeps working with deterministic template summaries
(`AI_DISABLED_CONTINUITY`).

## Stack boundary

- Decision logic: `submission/src/` (rule engines only)
- Presentation: this folder
- CLI: `submission/scripts/run_workflow_{a,b,c}.py`
- Supplied evidence explorer (not this app): package-root `app/`
