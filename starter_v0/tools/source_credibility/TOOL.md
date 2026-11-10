---
name: source_credibility
track: bonus
kind: local_knowledge
provider: local_evaluator
requires_env: []
inputs: [url, source_type]
outputs: [tier, requires_corroboration, domain, reason]
side_effect: false
---
# source_credibility

Evaluates the credibility tier (Tier 1, Tier 2, or Tier 3) of a source URL or source type
according to the internal Company Source Citation Policy.
