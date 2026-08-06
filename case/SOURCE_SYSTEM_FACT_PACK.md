# Source-System Fact Pack

| System | Function | Known issue | Authority caveat |
|---|---|---|---|
| PolicyCore-IN | Retail policy administration | Read-only during containment | Authoritative for issued schedule, not scanned endorsements |
| ClaimSphere | Claims and reserves | Duplicate party and event IDs | Reserve write defect under investigation |
| PriceForge | Pricing and renewals | Channel factors and proxy risk | Model version differs by country |
| UnderwritePro | Commercial and life underwriting | Override reasons incomplete | Delegated authority is external |
| MedClaim Hub | Health claims | Provider IDs reused | Clinical notes require segmentation |
| DrivePulse | Telematics | Firmware changed semantics | Driver attribution is probabilistic |
| CatVision | Hazard and imagery | Vendor outage | Model release independently unvalidated |
| ReSure | Reinsurance administration | Signed wording attachment missing | Broker and legal repositories may control |
| DataLake-X | Analytics snapshot | Stale and cross-tenant rows | Never authoritative by itself |
| AI Gateway | Model and tool access | Revocation cache lag | Current IAM must be checked per action |
| PayFlow | Claims payments | Degraded mode | No AI write permission is allowed |
| DocVault | Signed documents | Metadata quality varies | Signature and effective date must be validated |

## Evidence-authority rules to discover and defend

Authority is contextual. A system may be authoritative for issuance but not effective-time interpretation, for paid amount but not coverage, or for identity but not party role. Participants must create an explicit temporal and jurisdictional authority model rather than a single global source-of-truth ranking.
