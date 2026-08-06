# Participant Submission Area

All participant-generated implementation, tests, evidence, artefacts and runbooks must remain under this directory.

Start with:

```bash
python tools/check_submission.py --mode scaffold
```

Before defence run:

```bash
python tools/check_submission.py --mode final
python tools/hash_submission.py
```

See `runbooks/EVIDENCE_AND_SUBMISSION_STANDARD.md` for mandatory manifests and file expectations. Do not modify supplied challenge evidence and do not introduce real customer, policy, claim, medical, payment or proprietary data.
