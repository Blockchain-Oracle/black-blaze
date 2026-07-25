# Verification Report

**Verification date:** 2026-07-25 UTC

## Context integrity

Command:

```bash
python scripts/validate_context.py
```

Result before publication:

```text
VALIDATION PASSED: 34 Markdown files, 2 JSON files, required files present, relative links resolved, no matched secret patterns.
```

The count becomes 35 Markdown files after adding this report.

## External links

Command:

```bash
python scripts/check_external_links.py --output .tmp/link-check.json
```

Result:

```text
Checked 67 URLs: 67 reachable, 0 failed
```

An event-provided GMI Cloud path returned HTTP 404. The resource index documents the broken historical path and points to GMI's current `llms.txt` documentation index instead.

## Genblaze smoke test

The cloned `genblaze-core` package installed in an isolated local virtual environment. `examples/quickstart_local.py` completed with `Verified: True` and a canonical SHA-256 manifest hash. This was offline placeholder data, not a live provider/B2 test.

## Repository-source provenance

Six repositories were shallow-cloned, inspected, and recorded with exact HEAD SHAs. Clones are ignored and not redistributed. See:

- `../06-technical/REPOSITORY_AUDITS.md`
- `repositories.json`

## GitHub publication check

- Remote: `https://github.com/Blockchain-Oracle/black-blaze`
- Visibility: private
- Default branch: `main`
- Initial remote clone contained 39 tracked files at commit `c7b8b7af8bbd2fe2bb507cfaf62c7c203440308f` and passed the context validator.
- This report is part of a subsequent documentation commit; use the latest `main` commit as the final snapshot.

## Limitations

- URL reachability does not prove every page's content will remain unchanged.
- Participant count, project gallery, discussions, updates, rules, model slugs, package versions, pricing, and account limits are live.
- Eligibility and prize receipt remain subject to Sponsor/Administrator verification and applicable law.
- No live B2 account, GMI account, or paid model credentials were used during this research pass.
