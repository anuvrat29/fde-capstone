# Declared Data Exceptions

These conditions are intentional challenge evidence and must be surfaced rather than silently repaired:

- `OM-Small` appears in performance evidence but not the internal model registry because it is an external fallback candidate.
- `UW-LIFE-4` appears in fairness metrics without a complete registry record, representing a governance gap.
- Only the Home Protect policy-wording family has a complete local wording table; other products require escalation for controlling wording.
- `party_roles.csv` legitimately repeats `party_id` because one party may hold multiple roles in different contexts.
- `model_performance.csv` legitimately repeats `model_id` by language or segment.
- Blank catastrophe-event identifiers are valid for non-catastrophe claims.
- Compact evidence-envelope tables are deliberately sparse and mixed-authority; they are not master data.
- Knowledge documents marked untrusted, obsolete, marketing, draft, vendor or counterparty must not control decisions.
