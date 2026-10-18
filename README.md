# Verus Proof Skill

A reusable agent skill for writing, debugging, and reviewing Verus proofs, based on the [Verus guide to using LLMs for proofs](https://verus-lang.github.io/verus/guide/llmforverusproof.html).

## Skill

The skill is in [`skills/verus-proof/SKILL.md`](skills/verus-proof/SKILL.md), following the top-level layout recognized by `npx skills add`. Use it when an agent needs to develop or debug Verus proofs. It guides the agent to iterate with Verus, consult `vstd` and verified tests, preserve specifications and executable behavior, and check for proof shortcuts.
