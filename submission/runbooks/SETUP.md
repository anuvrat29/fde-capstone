# Setup Runbook

## Purpose

One-command environment setup for the AEGIS-INSURE participant submission. This runbook covers the offline, dependency-light setup path only; no cloud keys, paid APIs or external datasets are required or permitted.

## Prerequisites

- Python 3.10 or later (standard library only; see PACKAGE_SCOPE_AND_ASSUMPTIONS.md).
- Repository cloned or extracted with `FILE_HASHES.csv` intact and unmodified outside `submission/`.

## Steps

1. From the repository root, verify the package is intact and unmodified:
   ```bash
   python run_capstone.py
   ```
   This rebuilds `app/data.js`, verifies all package hashes, validates inject mappings and confirms the submission workspace is writable. Do not proceed if this fails — restore the original archive rather than repairing challenge evidence manually.

2. Confirm the submission scaffold exists and is writable:
   ```bash
   python tools/check_submission.py --mode scaffold
   ```

3. No additional package installation is required. If participant-authored code under `submission/src` introduces third-party dependencies, they must be vendored or documented here with an offline-installable wheel/path; no network access may be assumed at run time.

## Current submission state

As of this pass, `submission/src`, `submission/app`, `submission/tests` and `submission/scripts` contain no substantive implementation files beyond `.gitkeep` placeholders. This setup runbook will be updated with any additional dependency or environment-variable requirements as soon as implementation code is added. There are currently no environment variables, config files or secrets required.

## Verification

Setup is complete when both commands in step 1 and step 2 print `PASS` with no errors.
