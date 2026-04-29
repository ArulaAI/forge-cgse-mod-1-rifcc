---
mode: agent
description: Run the autowork autonomous development loop to process open issues
tools:
  - shell
---

Run the autowork orchestrator to process open issues. First do a dry run to preview, then execute:

```bash
# Preview the execution plan
python .forge/primitives/autowork/shared/orchestrator.py . --dry-run

# Execute against markdown issues
python .forge/primitives/autowork/shared/orchestrator.py . --source markdown

# Execute against GitHub issues with label filter
python .forge/primitives/autowork/shared/orchestrator.py . --source github --label primitives
```

The orchestrator reads `.forge/autowork.yaml` for domain configuration and routes each issue to the appropriate domain based on its labels.
