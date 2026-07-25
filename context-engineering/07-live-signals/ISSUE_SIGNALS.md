# Genblaze Issue Signals

These open issues are not event rules. They are live engineering evidence from users of the current SDK.

## Most relevant open issues observed

- #195 — export deterministic-provider ffmpeg helpers.
- #194 — Google chat rejects canonical image URL content, reducing provider portability.
- #193 — GMI base URL/payload/entitlement papercuts.
- #176 — local bytes to provider `external_inputs` and durable vs transient URL documentation gaps.
- #172 — business provenance metadata and deterministic transformation providers.
- #168 — cross-provider handoff, model IDs, throttling, Parquet documentation, chat provenance.
- #89 — OpenTelemetry spans may be orphaned.
- #67 — pipeline template auto-discovery initializes providers eagerly.

Issue list: https://github.com/backblaze-labs/genblaze/issues

## Implementation consequences

1. Test exact model slugs with the final provider key before building around them.
2. Store a stable SHA-256 on transient input assets.
3. Keep presigned URLs transient and redacted.
4. Prefer released v0.6 behavior over examples pinned to old 0.3/0.4 combinations.
5. Write integration tests against the actual installed packages.
6. Do not overpromise provider portability for multimodal chat.
7. If filing feedback, avoid duplicating these issues and provide a new, evidenced contribution.
