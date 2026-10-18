# verus-skill

An agent skill for using LLM coding agents to write and repair [Verus](https://github.com/verus-lang/verus) proofs, based on the Verus Guide chapter [Using LLMs to Help Write Verus Proofs](https://verus-lang.github.io/verus/guide/llmforverusproof.html).

It bundles a cheat checker (`cheat_check.py`) that diffs a modified file against the original and flags `assume`/`admit`/`external_body`/axioms and changed specs.

## Install

```sh
npx skills add sevki/verus-skill
```

## Development

```sh
python3 -I tests/validate_skills.py
python3 -I -m unittest discover -s tests -v
```

CI also checks that the `skills` CLI can discover and install the skill.
