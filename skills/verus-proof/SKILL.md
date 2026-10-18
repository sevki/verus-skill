---
name: verus-proof
description: Write, debug, and review Verus proofs while preserving program behavior and specifications. Use when verifying Rust code with Verus or helping complete Verus proof annotations.
---

# Verus Proof Development

Help develop Verus proofs by iterating with the verifier, learning from the project’s existing Verus resources, and preserving the program and its specifications.

## Workflow

1. **Understand the task and scope.** Read the target code, its `requires` and `ensures` clauses, relevant surrounding code, and the project’s verification commands. Identify whether the task is to fill in proof annotations or change something broader.
2. **Find the available resources.** Check for the Verus binary and the project’s `vstd`, Verus guide, and verified tests. Search those resources for syntax, established idioms, and existing lemmas before inventing APIs.
3. **Run Verus before editing.** Verify the target with the project’s usual command. Read the full diagnostics, including source locations; use `--expand-errors` when additional detail would help.
4. **Make a focused proof change.** Add or refine proof annotations to address the reported obligations. Prefer small, understandable steps and relevant library lemmas over guesses or large rewrites. Do not change executable code or existing specifications to make verification easier unless the user explicitly requests that broader change.
5. **Iterate with the verifier.** Re-run Verus after each meaningful change, inspect the new diagnostics, and continue until the target verifies. Do not hide errors by truncating output or report success based only on an exit code or partial log.
6. **Check the final diff and verify again.** Confirm the change is limited to the requested proof work and rerun the relevant verification command on the final version. Report the command and result, along with any remaining unverified cases or limitations.

## Proof integrity

- Do not introduce `assume(...)`, `admit(...)`, `external_body`, or new `axiom` declarations to bypass proof obligations.
- Preserve existing `requires` and `ensures` clauses and executable behavior unless the user has explicitly asked to change them. Never silently weaken a postcondition or strengthen a precondition.
- Run the project’s cheat checker if one is available. Also review the diff against the original code for these shortcuts: search added or modified content for the constructs above, then investigate each match in context; a text match alone is not proof that a change is unsound.
- Do not claim a proof is verified unless Verus completed successfully on the final code.

## Working effectively

- Treat Verus diagnostics as feedback for the next proof step. When a proof is difficult, break it into smaller claims or lemmas and verify incrementally.
- For missing or uncertain APIs, inspect `vstd` and relevant verified tests instead of guessing. Do not assume a plausible-sounding lemma exists.
- Keep proof tasks focused. Large projects, inductive invariants, procedural macros, and opaque abstractions can require substantial exploration; isolate a smaller proof target when possible.
- Generated proofs may be much longer than necessary. Once verification succeeds, simplify only when the result can be verified again.
- Be mindful that coding agents may make many model calls, and difficult proofs may take significant time and compute. Set reasonable verification resource limits, split large tasks, and share intermediate results when a proof cannot be completed.
- Use a secure, appropriately sandboxed environment when allowing an agent to run commands or modify files.

## Useful resources

- [Verus guide: Using LLMs to Help Write Verus Proofs](https://verus-lang.github.io/verus/guide/llmforverusproof.html)
- [Verus standard library (`vstd`)](https://github.com/verus-lang/verus/tree/main/source/vstd)
- [Verus verified tests](https://github.com/verus-lang/verus/tree/main/source/rust_verify_test)
- [Verus guide sources](https://github.com/verus-lang/verus/tree/main/source/docs/guide/src/)
