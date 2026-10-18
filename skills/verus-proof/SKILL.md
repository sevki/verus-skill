---
name: verus-proof
description: Workflow and guardrails for using an LLM coding agent to write or repair Verus proofs (Rust verification). Make sure to use this skill whenever the user mentions Verus, vstd, proof annotations, proof fns/lemmas, requires/ensures, assert-by, "verus file.rs", rlimit, or asks to make a .rs file verify, fix Verus errors, fill in a proof skeleton, or clean up an existing Verus proof, even if they don't say "skill" or "LLM".
---

# Writing Verus proofs with an agent

Source: the Verus Guide, "Using LLMs to Help Write Verus Proofs"
(https://verus-lang.github.io/verus/guide/llmforverusproof.html). Re-read it if
something here seems stale; Verus and model behavior change quickly.

Proof writing goes best as an observe-adjust loop: edit annotations, run Verus,
read the full errors, repeat. A model guessing without verifier feedback is
relying on luck, so every step below exists to keep that loop tight and honest.

## Setup checklist (do before editing)

1. **Find Verus.** Check `which verus`; ask the user for the path if absent. You need a one-line command, e.g. `verus file.rs`. Do not truncate output to just pass/fail; read the whole error report. `--expand-errors` gives more detail on failing assertions.
2. **Find vstd and examples.** Locate the vstd source, the Verus test suite (`rust_verify_test`), and the Verus Guide in the repo or a local Verus checkout. Grep them for lemma names and syntax. Never invent a lemma name: guessing `len_mono`, `subset_len`, `len_le_of_subset` in turn (and failing each time) is the classic hallucination pattern when vstd isn't consulted. `rust_verify_test` is also the best source for newest features.
3. **Snapshot the original file** (e.g. `cp file.rs /tmp/file.orig.rs`) so the cheat checker can diff against it.

## Rules for the task

- Do not change existing specifications (`requires`/`ensures`, spec fns, invariants) or executable code. Weakening a postcondition, strengthening a precondition, or "optimizing" the Rust changes what is being proven. If a spec truly seems wrong or too weak, stop and tell the user rather than editing it.
- No `assume(...)`, `admit(...)`, `#[verifier::external_body]`, or `axiom`-tagged lemmas to make errors go away. Those make the proof vacuous.
- Keep editing until Verus reports no errors, then run the cheat checker (below) before declaring success.

## The loop

1. Run Verus; read all errors.
2. Search vstd / tests for relevant lemmas; fix imports (`use vstd::prelude::*;` etc.) first since import errors cascade.
3. Add the smallest annotation that addresses the first error: an `assert`, a `reveal`, a lemma call, an `assert forall ... by`, loop invariants, or a decreases clause.
4. Re-run. Prefer decomposing the proof into smaller helper lemmas over pushing hard at one big one.
5. Keep `--rlimit` modest (e.g. 50 to 150). Some models crank it to 2000 and then hang for hours; if a proof needs that, it needs to be split, not given more budget.
6. After verification succeeds, try deleting annotations one at a time (see "Trim verbosity").

## Cheat checker

Run after every claimed success:

```
python3 <skill-dir>/scripts/cheat_check.py ORIGINAL.rs MODIFIED.rs
```

It flags added lines containing `assume`, `admit`, `external_body`, `external`, `axiom`, `verifier::` attributes, and heuristically warns when `requires`/`ensures`/`decreases`/`invariant` lines or non-proof code lines were removed or changed. Exit code 1 means findings; fix them, don't argue with them. It is text-based, so spec and executable-code changes still deserve a manual look at `diff -u`.

## Trim verbosity

LLM proofs tend to be 2-3x longer than human ones: needless "safety" asserts, case splits Z3 handles unaided. Example: for
`forall|s: Seq<A>, v: A, x: A| !s.contains(x) && v != x ==> !s.push(v).contains(x)`
an empty proof body already verifies, yet models write a 25-line contradiction proof. Once green, remove assertions and sub-blocks one by one, re-running Verus, and keep only what's needed. This cuts maintenance and verification time.

## Where models struggle (set expectations, escalate early)

- Inductive invariants for state machines (finding the stronger invariant).
- Procedural-macro-generated code.
- Heavy abstraction: closed/opaque spec fns where the right lemma must be chosen to `reveal` properties.
- Very large tasks; success falls as line count grows. Extract the target function/lemma into a small file when possible, since exploring a whole project costs more tokens.

When stuck, leave a useful partial result: state what is proven, what remains, which assert fails, and why. Humans can take over from a clear intermediate state. Some proofs cost real money even on a single function, so split big goals and avoid open-ended retries.

## Working with a human

Good split of labor: the human writes the proof skeleton and the lemma statements; you fill in routine detail. You can also propose adjusted lemma specs when decomposition is hard, and point to relevant vstd or project lemmas. Design, specification, and proof architecture stay with the human.

## Example prompt (for the user to reuse or for sub-agents)

```
The file X.rs cannot be verified by Verus yet.
Please add proof annotations so that it can be successfully verified by Verus.
The vstd folder contains Verus standard library definitions and helper lemmas.
Keep editing your proof until Verus shows no errors.
Do NOT change existing specifications (requires/ensures) or executable code.
Do NOT use assume(...) or admit(...).
Before you finish, run the cheat checker to make sure you haven't cheated.
```

Run the agent in a sandbox/container so it can call Verus freely without constant approvals.
