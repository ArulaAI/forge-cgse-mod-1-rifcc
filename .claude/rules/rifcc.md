---
applyTo: "**/*.md"
---

# RIFCC rules

1. Never modify `exercises/*/reference/`.
2. Every prompt sent to an LLM must walk R-I-F-C-C explicitly.
3. **R**ole — who is the agent? (reviewer / author / explainer / etc.)
4. **I**ntent — what's the goal? (find bugs / verify spec / generate code / etc.)
5. **F**rame — which files / scope / context window?
6. **C**onstraints — what must NOT happen? (no rewrites / no new deps / etc.)
7. **C**onfidence — what would change "yes" to "no"?
