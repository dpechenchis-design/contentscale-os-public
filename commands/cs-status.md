---
description: Показати, на якому етапі ContentSCALE-пайплайну клієнт і що далі
argument-hint: <slug клієнта>
---
Run the `cs-pipeline` skill's status step only for client `$ARGUMENTS`: execute `python3 -I <folder that holds the cs-pipeline skill: the plugin's skills dir, or ~/.claude/skills after a ZIP install>/cs-pipeline/scripts/pipeline_status.py clients/$ARGUMENTS` and summarize for the Content Manager in Ukrainian: stage table, blockers, the single next action, and what (if anything) is needed from them. Do not start work.
