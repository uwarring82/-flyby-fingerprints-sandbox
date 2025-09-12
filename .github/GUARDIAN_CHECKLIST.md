# Guardian Safety Checklist

## Physics Completeness
- [ ] ≥3 citations (module docs)
- [ ] Uncertainty bounds documented & implemented
- [ ] Validity ranges stated

## Code Integrity
- [ ] Unit tests incl. seeded randomness
- [ ] Air-gapped formatting gate passes
- [ ] Performance note (if applicable)

## Validation Status
- [ ] Residuals artifact generated
- [ ] Residual medians < 10% (placeholder acceptable until real data)
- [ ] Cross-validation if `risk: H` (`requires_cross_validation: true`)

## Documentation
- [ ] Failure Modes & Mitigations documented
- [ ] `/docs/` updated (model, benchmarks, policy)
- [ ] Known limitations listed

## Phase Gate
- [ ] Foundation gate sign-offs requested in PR body
