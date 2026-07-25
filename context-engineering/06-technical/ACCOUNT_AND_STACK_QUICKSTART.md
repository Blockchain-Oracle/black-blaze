# Account and Stack Quickstart

## 1. Join and create accounts

- Join the Devpost event.
- Create a Backblaze B2 account and enable MFA.
- Create a dedicated bucket.
- Create a least-privileged app key scoped to that bucket.
- Choose at least one confirmed media provider. GMI Cloud is optional.

## 2. Verify local prerequisites

```bash
python --version   # must be 3.11+
ffmpeg -version    # needed for composition/transforms
```

## 3. Prove Genblaze locally without keys

```bash
git clone --depth 1 https://github.com/backblaze-labs/genblaze.git
python -m venv .venv
source .venv/bin/activate
pip install -e genblaze/libs/core
python genblaze/examples/quickstart_local.py
```

Expected evidence: `Verified: True`. This is only a local manifest smoke test.

## 4. Prove B2 independently

Using the final app's storage package:

- upload a small generated test asset;
- read it back;
- compare SHA-256 bytes;
- list only the expected prefix;
- delete it if the key is intended to have delete permission;
- record account cap/transaction behavior.

Do not paste credentials or signed URLs into issue trackers, chat, screenshots, or committed logs.

## 5. Prove one live model call

Before product code, invoke each planned model with minimum cost settings. Record:

- provider and exact model slug;
- SDK/package versions;
- latency and cost if available;
- output media type;
- entitlement/rate-limit behavior;
- whether an input URL must be public/presigned;
- content-policy behavior.

## 6. Build one end-to-end slice

Use a real user input to produce one useful output with:

- at least one real Genblaze pipeline step;
- B2 persistence;
- a manifest and byte hash;
- UI progress and explicit failure status;
- a clean test/demo path.

Only add fan-out, more providers, or extra modalities after this is stable.
