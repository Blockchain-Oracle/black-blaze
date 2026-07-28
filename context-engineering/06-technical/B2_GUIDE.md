# Backblaze B2 Technical Guide

## Why B2 must be load-bearing

The scoring criterion rewards meaningful storage and data orchestration. A single `upload(final.mp4)` call is weak. Strong B2 usage stores and manages the full media lifecycle:

```text
inputs/ → intermediate generations/ → accepted outputs/ → thumbnails/
        → manifests/ → indexes/ → logs/ → final deliveries/
```

## Account setup

1. Create/enable a B2 account and MFA.
2. Create a bucket.
3. Create a bucket-scoped application key with only required permissions.
4. Copy key value once into a secrets manager or local `.env`; never commit it.
5. Configure Genblaze's `S3StorageBackend.for_backblaze(...)`.

Typical Genblaze environment variables are `B2_KEY_ID`, `B2_APP_KEY`, optional `B2_BUCKET`, and `B2_REGION`. Sample repositories differ (`B2_APPLICATION_KEY`, `B2_BUCKET_NAME`, `B2_ENDPOINT`), so follow the installed package and chosen app's configuration rather than mixing conventions.

For a later credentialed canary, use a standard application key—not the master key—restricted to one private bucket/prefix with `readFiles`, `writeFiles`, `deleteFiles`, and `listAllBucketNames`; add `listFiles` only if the test lists objects. Both write and delete capabilities are generally needed for S3 `DeleteObject`.

## Recommended product roles

- **Durability:** provider URLs expire; B2 copies remain.
- **Organization:** hierarchical run/tenant/project paths.
- **Deduplication:** content-addressed asset keys.
- **Provenance:** manifests beside assets; optional Object Lock for immutability.
- **Serving:** durable public URLs or controlled private access/presigned delivery.
- **Workflow:** asset arrival can trigger downstream work where Event Notifications access is available. Official documentation says the feature must be enabled by contacting Backblaze Support, so it must not be a critical hackathon dependency until access is confirmed.
- **Lifecycle:** delete rejected/intermediate variants after a policy period.
- **Indexing:** query metadata/Parquet or an app database keyed to B2 objects.

## Security decisions

- Prefer private buckets for user media.
- Public buckets are acceptable only for sanitized demo assets.
- Never expose B2 application keys in a browser bundle.
- Use least privilege and a dedicated hackathon bucket/key.
- Presigned URLs are temporary and can include credential identifiers in query parameters; redact them from logs/manifests.
- Object Lock must be enabled thoughtfully: once enabled at bucket level it cannot be disabled, and compliance-mode retention cannot be shortened or removed. Use it only where immutability materially supports the product.

## Current pricing and limits

The official main pricing page rechecked on 2026-07-27 says:

- first 10 GB always free;
- pay-as-you-go Class A/B/C API calls free;
- storage is $6.95/TB/30-day, approximately $0.00695/GB-month;
- Class D transactions have 2,500 free calls/day, then $0.004/10,000;
- free egress up to 3× average monthly storage, with stated partner exceptions, then $0.01/GB.

The transaction-pricing page still states stale $0.005/GB-month storage. Preserve the conflict and use the current main pricing page for budgeting.

Official documentation rechecked on 2026-07-28 says new accounts default to 500 upload/download requests per second. Native API throttling returns `429`; S3 returns `503 SlowDown`, potentially with `Retry-After`. User-configured caps can independently stop operations, so published throughput is not proof of the entrant's account behavior.

However, a participant reported hitting a 2,500/day B2 access cap, and Genblaze v0.6.0 mentions daily Class B caps/restricted keys causing `HeadObject` 403. Older help pages also describe 2,500 free Class B calls. Treat account-level caps/pricing as an **open operational check**: inspect the actual B2 dashboard and run a load test. Do not architect a polling-heavy system.

## S3 compatibility caveats

Backblaze's S3-compatible API supports common S3 operations and presigned URLs, but not all AWS S3 features. Official documentation names limitations around object-level ACLs, IAM roles, object tagging, website configuration, and browser `POST` uploads to presigned URLs. Design against B2's actual API surface.

- Use short-lived exact-key presigned `PUT` or an API proxy; presigned browser `POST` is unsupported.
- CORS permits browser behavior but is not authorization. Allow only the production origin and required PUT/GET/HEAD methods/headers.
- A single S3 upload may be up to 5 GB. Short media should normally use one PUT; do not infer a multipart requirement for small clips.
- Combined filename and metadata are limited to 7,000 bytes, reduced to 2,048 bytes with SSE or Object Lock. Store full lineage in a JSON manifest.
- Do not use S3 ETag as SHA-256. `HeadObject`, fetch every byte, and recompute the digest.
- B2 buckets are always versioned. Reusing a key creates versions; name-only deletion can leave older bytes. Record and delete exact `VersionId`/native `fileId` values.
- Current `Get`, `Put`, and `Delete Lifecycle Configuration` S3 APIs conflict with an older official page that says lifecycle is Web/Native-only. Use the newer API documentation and one management surface; B2 supports only a subset of AWS lifecycle semantics, and processing is approximately daily rather than an immediate-deletion guarantee.

The web-console upload limit is also inconsistent across official pages (500 MB versus 5 GiB). This is not load-bearing for SDK/S3 uploads; avoid relying on the web console for large media.

## Prepared B2 canary

The smallest real canary remains credential-gated:

```text
put one synthetic artifact
→ head it
→ fetch every byte and compare SHA-256
→ put/read/verify its manifest
→ delete artifact and manifest by exact versions
→ optionally head both to confirm not found
```

Base request classes are A=4 and B=3; post-delete confirmation makes B=5. Do not enable Object Lock on this bucket.

## Judge-visible B2 evidence

- media library or run browser backed by B2;
- inspectable object path and metadata;
- provenance verification screen;
- intermediate/final distinction and retention policy;
- download/playback that remains valid through judging;
- test showing a stored byte changed → verification fails;
- architecture diagram showing B2 between pipeline stages, not outside the product.
