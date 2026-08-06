# Project AEGIS-INSURE — Integrated Insurance Challenge Case

## 1. Organisation


**Aurelia Mutual & Re Group (AMR)** is a fictional composite insurer and reinsurer operating in India, Germany, the United Kingdom, the United States, Singapore and the UAE. It writes retail motor and home, health, term life, disability, commercial property, marine cargo, cyber, parametric agriculture and specialty liability business, and also accepts and cedes reinsurance.


AMR serves approximately 18 million policyholders through direct channels, brokers, banks, employers, managing general agents and affinity partners. Its estate contains multiple policy-administration platforms, claims systems, pricing engines, actuarial workbenches, document stores, telematics platforms, provider networks, catastrophe tools, reinsurance systems, data lakes and vendor portals.

## 2. The converging crisis

Cyclone **Nila** produces wind, storm-surge, river-flood, motor, health, business-interruption and parametric claims across India, the Gulf and European supply chains. At the same time, AMR experiences a ransomware containment event, a model-package integrity failure, a telematics firmware change, allegations of discriminatory pricing, a bancassurance mis-selling review, a reinsurance event-definition dispute and a 72-hour multi-regulator evidence request.

The operational facts are fragmented and contradictory. Policy, party, claim, coverage, peril, location, repairer, provider, broker, treaty, currency and model identifiers do not reconcile reliably. Some records are stale, duplicated, altered, untrusted, outside purpose, in the wrong jurisdiction or temporally inapplicable.

## 3. Participant mandate

Design and demonstrate a defensible AI Forward Deployed Engineering intervention that improves evidence reconciliation and operational decision support without assuming regulated accountability. Participants may conclude that an AI component, agent, semantic layer or knowledge graph is unjustified, but must prove the decision.

## 4. Mandatory workflows

### Workflow A — Coverage, claim and fraud evidence reconciliation

Reconcile policy version, endorsement timing, insured interest, loss event, peril, cause, coverage, exclusion, deductible, claimant identity, repair/provider evidence, fraud indicators, legal hold and provenance. The workflow may expose contradictions, missing evidence and candidate next actions. It must never bind coverage, repudiate, settle, reserve, pay, cancel or litigate a claim.

### Workflow B — Underwriting, pricing and customer-outcome evidence support

Reconcile application facts, external data rights, rating factors, actuarial model version, underwriting rules, protected-proxy risk, overrides, renewal treatment, consent and explanation evidence. It may provide bounded recommendations and alternatives. It must never bind, decline, price, renew, cancel or modify a policy.

### Workflow C — Bounded catastrophe, liquidity and reinsurance recovery planner

Generate traceable response options using catastrophe events, exposure accumulation, claim severity, emergency hardship, operational capacity, reserve uncertainty, reinsurance terms, hours clauses, currencies, collateral, sanctions, vendor availability and customer vulnerability. It must never create a payment, change a reserve, aggregate a treaty event, submit a recovery, allocate capital or instruct a vendor without authorized human approval.

## 5. Required operating properties

Every workflow must demonstrate purpose limitation, least privilege, current authorization, temporal and jurisdictional applicability, source authority, provenance, structured outputs, abstention, human review, contestability, idempotency, bounded steps, token and cost budgets, checkpointing, rollback, kill switch, degraded mode, auditability and AI-disabled continuity.

## 6. Embedded-inject rule

All challenge conditions are disclosed below. There are no later instructor injects. Participants must discover connections, contradictions, common-cause failures and cascading consequences from the supplied repository.

## 7. Inject catalogue

### D01 — Strategy, value and operating-model conflict
**INJ-001 — Board catastrophe target.** The board demands a 20% reduction in catastrophe claim cycle time and a 12% expense-ratio improvement without weakening claims independence, reserving governance or consumer protections. Evidence is distributed across `board_requests.csv; kpi_conflicts.csv`.
**INJ-002 — No-AI challenge.** Process Excellence argues that policy-wording rationalisation, identity repair and workflow redesign can deliver most benefits without generative AI. Evidence is distributed across `no_ai_baselines.csv; process_bottlenecks.csv`.
**INJ-003 — Mutual versus shareholder tension.** The mutual parent prioritises member fairness while a listed subsidiary prioritises growth and combined-ratio targets. Evidence is distributed across `legal_entities.csv; strategy_conflicts.csv`.
**INJ-004 — Acquisition integration.** A recently acquired digital insurer uses different product identifiers, pricing factors, cloud tenancy and claims authority matrices. Evidence is distributed across `legal_entities.csv; system_inventory.csv`.
**INJ-005 — Prohibited autonomy.** The board prohibits autonomous binding, declinature, pricing, reserve changes, settlement, payment, policy cancellation, claim repudiation or treaty placement. Evidence is distributed across `ai_use_boundaries.csv; decision_rights.csv`.
**INJ-006 — Value leakage.** The business case excludes complaints, appeals, human review, litigation, regulatory remediation and model-change costs. Evidence is distributed across `cost_model.csv; staff_rates.csv`.

### D02 — Product, policy and coverage lifecycle
**INJ-007 — Policy version collision.** Three policy wordings with the same marketing name have different exclusions, endorsements and territorial limits. Evidence is distributed across `policy_products.csv; policy_wording_versions.csv`.
**INJ-008 — Endorsement timing conflict.** A flood endorsement was requested before loss but issued after loss; payment and effective dates disagree. Evidence is distributed across `policies.csv; endorsements.csv`.
**INJ-009 — Binder authority ambiguity.** A managing general agent bound a commercial risk above delegated authority during a portal outage. Evidence is distributed across `binder_events.csv; delegated_authorities.csv`.
**INJ-010 — Cancellation and reinstatement race.** Cancellation, premium receipt and reinstatement events arrived out of order across billing and policy administration. Evidence is distributed across `policies.csv; billing_events.csv`.
**INJ-011 — Master-policy certificate mismatch.** A group health certificate promises benefits not present in the master policy schedule. Evidence is distributed across `group_policies.csv; member_certificates.csv`.
**INJ-012 — Parametric trigger wording conflict.** The customer brochure describes rainfall at farm location, while the contract uses a named weather-station index. Evidence is distributed across `parametric_contracts.csv; marketing_materials.csv`.

### D03 — Underwriting, pricing and actuarial model risk
**INJ-013 — Protected-proxy pricing.** Motor pricing uses postcode, occupation and device variables that strongly proxy protected characteristics. Evidence is distributed across `pricing_factors.csv; fairness_metrics.csv`.
**INJ-014 — Telematics firmware drift.** A firmware update changes harsh-braking counts and mileage aggregation without a pricing-model recalibration. Evidence is distributed across `telematics_events.csv; device_firmware.csv`.
**INJ-015 — Catastrophe model version split.** Property accumulation reports use two catastrophe-model versions with materially different flood loss estimates. Evidence is distributed across `cat_models.csv; exposure_aggregates.csv`.
**INJ-016 — Clinical underwriting conflict.** Life underwriting receives contradictory smoking, medication and laboratory evidence from different sources. Evidence is distributed across `life_applications.csv; medical_evidence.csv`.
**INJ-017 — Unapproved external data.** A vendor supplies social and purchasing attributes without clear provenance or approved underwriting purpose. Evidence is distributed across `external_data_sources.csv; data_licenses.csv`.
**INJ-018 — Renewal price walking risk.** Home and motor renewal premiums diverge from equivalent new-business offers through channel-specific factors. Evidence is distributed across `quotes.csv; renewals.csv`.
**INJ-019 — Sparse specialty portfolio.** A cyber model extrapolates from a small, non-representative loss history and ignores silent-cyber exposure. Evidence is distributed across `cyber_risks.csv; model_performance.csv`.
**INJ-020 — Underwriter override opacity.** High-value commercial risks show unexplained overrides concentrated by office and broker. Evidence is distributed across `underwriting_decisions.csv; override_events.csv`.

### D04 — Claims, coverage, litigation and reserving evidence
**INJ-021 — Duplicate catastrophe claims.** The same property loss appears under household, landlord and small-business policies with different addresses. Evidence is distributed across `claims.csv; claimant_identities.csv`.
**INJ-022 — Coverage temporal ambiguity.** Loss time is uncertain across local time, UTC, daylight-saving transition and sensor timestamps. Evidence is distributed across `loss_events.csv; timezone_rules.csv`.
**INJ-023 — Repair estimate manipulation.** A repair network submits near-identical images and inflated line items across unrelated motor claims. Evidence is distributed across `repair_estimates.csv; image_forensics.csv`.
**INJ-024 — Medical necessity conflict.** Health pre-authorisation, provider invoice and clinical note disagree on procedure code and medical necessity. Evidence is distributed across `health_claims.csv; provider_records.csv`.
**INJ-025 — Life contestability boundary.** A death claim falls near the contestability boundary and the application has a disputed disclosure. Evidence is distributed across `life_claims.csv; policy_applications.csv`.
**INJ-026 — Litigation hold versus deletion.** A customer requests deletion while the claim, complaint and related class action are under legal hold. Evidence is distributed across `deletion_requests.csv; legal_holds.csv`.
**INJ-027 — Reserve leakage.** A batch job overwrote case reserves with model suggestions in one subsidiary despite advisory-only policy. Evidence is distributed across `claim_reserves.csv; audit_events.csv`.
**INJ-028 — Subrogation ownership conflict.** Two insurers and a recovery vendor assert rights over the same commercial loss recovery. Evidence is distributed across `subrogation_cases.csv; recovery_contracts.csv`.

### D05 — Catastrophe, property, motor and parametric operations
**INJ-029 — Cyclone-flood compound event.** Cyclone Nila creates wind, storm-surge, river-flood and business-interruption losses across shared locations. Evidence is distributed across `cat_events.csv; exposure_locations.csv`.
**INJ-030 — Geospatial address collision.** One apartment complex has six address forms and two geocodes, fragmenting accumulation and duplicate detection. Evidence is distributed across `addresses.csv; geocodes.csv`.
**INJ-031 — Drone evidence authenticity.** Post-loss drone imagery has missing signatures and one flight path conflicts with claimed capture time. Evidence is distributed across `drone_images.csv; drone_flights.csv`.
**INJ-032 — Business-interruption dependency.** A manufacturer has little physical damage but depends on a failed sole-source supplier outside the insured zone. Evidence is distributed across `commercial_claims.csv; supply_dependencies.csv`.
**INJ-033 — EV battery escalation.** A minor collision becomes a thermal event after towing, creating causation and salvage disputes. Evidence is distributed across `motor_claims.csv; vehicle_telemetry.csv`.
**INJ-034 — Parametric sensor spoofing.** Rainfall sensor data exceeds the trigger, but neighbouring stations and satellite estimates disagree. Evidence is distributed across `weather_observations.csv; parametric_contracts.csv`.
**INJ-035 — Catastrophe vendor outage.** The primary imagery and hazard vendor is unavailable during peak triage. Evidence is distributed across `vendor_status.csv; downtime_events.csv`.
**INJ-036 — Emergency payment pressure.** Executives request rapid hardship advances before coverage, sanctions and duplicate checks are complete. Evidence is distributed across `emergency_payment_requests.csv; claims.csv`.

### D06 — Life, health, disability and sensitive-risk operations
**INJ-037 — Provider identity collision.** A hospital group uses reused provider identifiers after an acquisition, corrupting network and fraud analytics. Evidence is distributed across `providers.csv; provider_aliases.csv`.
**INJ-038 — Health-code version mismatch.** ICD, CPT and local procedure codes use different effective versions across claim, pre-auth and policy rules. Evidence is distributed across `health_claims.csv; terminology_versions.csv`.
**INJ-039 — Mental-health privacy boundary.** Behavioural-health notes are exposed to a general claims summarisation workflow beyond minimum necessary use. Evidence is distributed across `clinical_notes.csv; access_policies.csv`.
**INJ-040 — Disability functional conflict.** Employer, physician, wearable and claimant evidence disagree on functional limitation and return-to-work dates. Evidence is distributed across `disability_claims.csv; functional_evidence.csv`.
**INJ-041 — Genetic-information exclusion.** A life-risk feature store contains family-history and genetic indicators prohibited or restricted in some jurisdictions. Evidence is distributed across `feature_store.csv; jurisdiction_rules.csv`.
**INJ-042 — Dependent eligibility mismatch.** A newborn is covered under a grace rule in one system but absent from the membership file. Evidence is distributed across `member_eligibility.csv; health_claims.csv`.
**INJ-043 — Wellness consent withdrawal.** A member withdraws consent for wearable use, but the data remains in pricing and engagement features. Evidence is distributed across `consents.csv; feature_store.csv`.
**INJ-044 — Provider outage and continuity.** A claims clearinghouse outage forces manual submissions with incomplete coding and duplicate risk. Evidence is distributed across `downtime_events.csv; manual_claim_intake.csv`.

### D07 — Fraud, financial crime and adversarial behaviour
**INJ-045 — Fraud-ring graph ambiguity.** Shared devices, addresses and repairers suggest a ring, but some links are legitimate household or fleet relationships. Evidence is distributed across `fraud_links.csv; claimant_identities.csv`.
**INJ-046 — Synthetic identity.** A life applicant combines valid government, credit and employer attributes belonging to different people. Evidence is distributed across `identity_checks.csv; life_applications.csv`.
**INJ-047 — Sanctions-name collision.** A claimant name matches a sanctions record but date of birth and nationality are incomplete. Evidence is distributed across `sanctions_screening.csv; claimant_identities.csv`.
**INJ-048 — Insider claim manipulation.** A claims handler repeatedly changes payee details shortly before payment approval. Evidence is distributed across `payment_changes.csv; audit_events.csv`.
**INJ-049 — Document deepfake.** A commercial fire claim includes an AI-generated invoice and altered certificate. Evidence is distributed across `claim_documents.csv; document_forensics.csv`.
**INJ-050 — Fraud-model feedback loop.** Investigations focus on model-selected groups, creating biased labels and apparent performance improvement. Evidence is distributed across `fraud_referrals.csv; model_training_labels.csv`.

### D08 — Reinsurance, capital, reserving and finance
**INJ-051 — Treaty wording ambiguity.** A catastrophe treaty differs between slip, signed wording and bordereaux mapping for hours clause and flood aggregation. Evidence is distributed across `reinsurance_treaties.csv; treaty_documents.csv`.
**INJ-052 — Event-definition conflict.** Claims teams use one catastrophe event ID while reinsurers apply different hours and geographic aggregation. Evidence is distributed across `cat_events.csv; reinsurance_events.csv`.
**INJ-053 — Bordereaux currency error.** Paid and outstanding amounts mix USD, EUR, INR and GBP using inconsistent valuation dates. Evidence is distributed across `bordereaux.csv; fx_rates.csv`.
**INJ-054 — Facultative placement gap.** A high-value location appears bound in broker email but absent from the reinsurance administration system. Evidence is distributed across `facultative_placements.csv; broker_correspondence.csv`.
**INJ-055 — Reserve model drift.** Inflation, repair duration and litigation severity move outside the reserving model training range. Evidence is distributed across `claim_reserves.csv; reserving_assumptions.csv`.
**INJ-056 — IFRS 17 grouping conflict.** Acquired portfolios map inconsistently to cohorts, profitability groups and contract boundaries. Evidence is distributed across `ifrs17_groups.csv; policy_products.csv`.
**INJ-057 — Capital-model concentration.** Cloud, cyber and catastrophe dependencies create correlated exposures not represented in the internal model. Evidence is distributed across `capital_scenarios.csv; vendor_dependencies.csv`.
**INJ-058 — Collateral dispute.** A reinsurer collateral balance is stale during a ratings downgrade and large-loss notification. Evidence is distributed across `reinsurance_collateral.csv; counterparty_ratings.csv`.

### D09 — Distribution, conduct, complaints and customer outcomes
**INJ-059 — Bancassurance mis-selling.** Recorded calls, sales script and suitability declaration conflict for a savings-linked protection product. Evidence is distributed across `sales_interactions.csv; suitability_records.csv`.
**INJ-060 — Broker remuneration conflict.** A broker receives higher commission for a product with narrower coverage and more exclusions. Evidence is distributed across `broker_commissions.csv; product_comparisons.csv`.
**INJ-061 — Dark-pattern renewal.** The mobile journey makes cancellation difficult and preselects optional covers. Evidence is distributed across `digital_journeys.csv; usability_findings.csv`.
**INJ-062 — Complaint clock mismatch.** Complaint receipt dates differ across email, branch, ombudsman and CRM systems. Evidence is distributed across `complaints.csv; communication_events.csv`.
**INJ-063 — Vulnerable customer handling.** A hardship claimant repeatedly discloses disability and bereavement but is routed through generic automation. Evidence is distributed across `customer_vulnerability.csv; contact_history.csv`.
**INJ-064 — Multilingual wording inequity.** Translated policy summaries omit material limitations present in the authoritative wording. Evidence is distributed across `translations.csv; policy_wording_versions.csv`.

### D10 — Data, interoperability, ontology and evidence authority
**INJ-065 — Party-role confusion.** The same person may be policyholder, insured, claimant, beneficiary, driver, employee and broker contact. Evidence is distributed across `parties.csv; party_roles.csv`.
**INJ-066 — Policy-claim identifier collision.** Legacy policy numbers are reused across countries and product lines. Evidence is distributed across `policies.csv; identifier_crosswalk.csv`.
**INJ-067 — ACORD mapping loss.** An integration drops endorsement effective time, reserve currency and catastrophe event identifier. Evidence is distributed across `acord_messages.csv; integration_errors.csv`.
**INJ-068 — Source-authority conflict.** Data lake snapshots, core systems, adjuster notes and signed documents disagree on material facts. Evidence is distributed across `source_authority.csv; evidence_conflicts.csv`.
**INJ-069 — Ontology scope dispute.** Teams disagree whether peril, cause, damage, coverage, exclusion and event should be distinct entities. Evidence is distributed across `glossary_conflicts.csv; ontology_seed.csv`.
**INJ-070 — Graph overreach.** Architects propose a knowledge graph for questions that reliable SQL and document retrieval may already solve. Evidence is distributed across `graph_candidate_questions.csv; no_ai_baselines.csv`.

### D11 — Privacy, cross-border, retention and secondary use
**INJ-071 — Purpose expansion.** Claims images and health data are proposed for enterprise model training beyond original processing purpose. Evidence is distributed across `consents.csv; data_use_requests.csv`.
**INJ-072 — Cross-border replica.** EU and Indian policyholder data is replicated into an unapproved analytics region. Evidence is distributed across `data_residency.csv; backup_inventory.csv`.
**INJ-073 — Household inference.** Connected-home data reveals occupancy, religion-related routines and health conditions not required for cover. Evidence is distributed across `iot_events.csv; privacy_risk.csv`.
**INJ-074 — Telematics family surveillance.** A policyholder receives scores inferred from journeys made by other household drivers. Evidence is distributed across `telematics_events.csv; driver_assignments.csv`.
**INJ-075 — Retention conflict.** Fraud, tax, litigation, actuarial and customer-deletion rules specify different retention periods. Evidence is distributed across `retention_rules.csv; deletion_requests.csv`.
**INJ-076 — Free-text oversharing.** Claims notes contain health, financial, family and immigration information unrelated to claim handling. Evidence is distributed across `claim_notes.csv; privacy_risk.csv`.

### D12 — Cybersecurity, agentic security and Zero Trust
**INJ-077 — Prompt injection in adjuster report.** A repairer report contains hidden instructions telling the AI to approve coverage and ignore fraud alerts. Evidence is distributed across `knowledge_catalog.csv; MALICIOUS_ADJUSTER_REPORT.md`.
**INJ-078 — Tool-manifest poisoning.** A new payment-status tool requests write privileges and changes payee information during a read operation. Evidence is distributed across `tool_catalog.csv; tool_manifest_poisoned.json`.
**INJ-079 — Revocation cache lag.** A terminated third-party adjuster remains authorized in the AI gateway cache. Evidence is distributed across `users_entitlements.csv; access_cache.csv`.
**INJ-080 — Ransomware containment.** Policy administration is read-only, claims images are offline and payment systems operate in degraded mode. Evidence is distributed across `downtime_events.csv; network_zones.csv`.
**INJ-081 — Model artefact mismatch.** A model package hash differs from the approved registry after an emergency vendor patch. Evidence is distributed across `model_registry.csv; model_artifacts.csv`.
**INJ-082 — Cross-tenant leakage.** A crafted broker query retrieves claim narratives from another legal entity. Evidence is distributed across `security_events.csv; tenant_boundaries.csv`.

### D13 — Responsible AI, fairness, explainability and human factors
**INJ-083 — Claims automation bias.** Handlers accept an AI summary that omits an endorsement favourable to the claimant. Evidence is distributed across `candidate_outputs.csv; reviewer_feedback.csv`.
**INJ-084 — Subgroup false positives.** Fraud referral rates and false positives are materially higher for specific regions, languages and low-income proxies. Evidence is distributed across `fairness_metrics.csv; fraud_referrals.csv`.
**INJ-085 — Unexplainable adverse outcome.** A life underwriting recommendation cannot identify the controlling evidence or policy rule. Evidence is distributed across `underwriting_decisions.csv; explanation_tests.csv`.
**INJ-086 — Language performance gap.** Arabic, Hindi and German claims show lower extraction and citation accuracy than English. Evidence is distributed across `model_performance.csv; multilingual_claims.csv`.
**INJ-087 — Accessibility failure.** The proposed portal uses colour-only severity, inaccessible PDFs and mouse-only approval controls. Evidence is distributed across `usability_findings.csv`.
**INJ-088 — Accountability conflict.** Global AI owners seek standard automation while local claims officers, actuaries and compliance leaders retain legal accountability. Evidence is distributed across `decision_rights.csv; stakeholders.csv`.

### D14 — Token economics, FinOps and vendor concentration
**INJ-089 — Model price shock.** The preferred provider raises input-token prices by 65% and removes cached-input discounts. Evidence is distributed across `model_costs.csv; vendor_contracts.csv`.
**INJ-090 — Denial-of-wallet.** Repeated oversized claim bundles and image reprocessing cause abnormal inference, OCR and embedding cost. Evidence is distributed across `model_usage.csv; security_events.csv`.
**INJ-091 — Hidden unit economics.** Cost per successful claim excludes human review, appeals, false-positive investigations and observability. Evidence is distributed across `cost_model.csv; staff_rates.csv`.
**INJ-092 — Stack concentration.** One vendor hosts model, vector store, OCR, evaluation, observability and key management. Evidence is distributed across `vendor_dependencies.csv; vendor_contracts.csv`.

### D15 — Reliability, continuity, change and retirement
**INJ-093 — Regional outage.** The primary AI region fails during catastrophe triage and statutory reporting deadlines. Evidence is distributed across `downtime_events.csv; model_endpoints.csv`.
**INJ-094 — Checkpoint replay.** A recovery agent resumes stale state and creates duplicate draft payments and reinsurer notices. Evidence is distributed across `agent_runs.csv; idempotency_records.csv`.
**INJ-095 — Fallback regression.** A smaller fallback model preserves JSON schema but loses coverage fidelity and multilingual accuracy. Evidence is distributed across `model_performance.csv; model_endpoints.csv`.
**INJ-096 — AI-disabled continuity and exit.** The insurer must operate for 21 days without model inference while a strategic vendor exits in 120 days and historical evidence remains inspectable. Evidence is distributed across `continuity_requirements.csv; vendor_exit_assets.csv`.

## 8. Required strategic decisions

Participants must explicitly decide and defend:

- Whether AI is justified against process redesign, rules, analytics, master-data repair and conventional workflow automation.
- Which policy wording, endorsement, record, timestamp, model and jurisdiction is authoritative for each decision context.
- Whether a knowledge graph is justified and which questions genuinely require relationship or multi-hop reasoning.
- How policy, party, claim, coverage, peril, location, treaty and evidence concepts are separated in the domain model.
- Which workflows trigger high-risk or regulated-use analysis and which remain advisory.
- How fairness, explainability, human review, contestability and adverse-action obligations are evidenced.
- How model, prompt, retrieval, tool, rule and configuration changes are controlled and evaluated.
- How AMR continues safely during ransomware containment, model unavailability, vendor exit and final retirement.

## 9. Definition of done

The capstone is complete only when another qualified team can reproduce the environment, execute the public tests, inspect evidence lineage, understand residual risks, run manual fallback, measure value and defend a go, conditional-go, pivot, pause or stop recommendation without oral knowledge from the builders.
