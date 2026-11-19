---
name: session-postmortem
description: At a tracked implementation task handoff, or when asked to run a session postmortem, use the active Copilot conversation to draft one reusable project improvement if actual friction was observed.
---

# Session postmortem

1. Use only evidence already visible in the active conversation or obtained
   during this task. Do not read session files, export a transcript, or copy
   prompts, secrets, or full tool output. Use the actual work issue number. If
   it is unknown, do not invent one.
2. Look for an observed failure, contradiction, or avoidable rework. Choose a
   change that helps future tasks. A bug fixed within this task is not enough.
   If there is no evidence for a reusable improvement, report no candidate
   and do not write a draft.
3. If `.feedback/task-<number>.json` already exists, report its path and leave
   it alone. Otherwise write one JSON object with these fields:

   ```json
   {
     "work_item": 12,
     "candidate": {
       "category": "docs",
       "title": "Explain the supported environment values",
       "finding": "A sample change was rejected before the accepted value could be determined from the command output.",
       "suggestion": "List the accepted values next to the profile creation instructions."
     }
   }
   ```

   Choose one category: `docs`, `instructions`, `standard`, or `lint-ci`.
   Keep each field plain text and on one line. The finding must describe what
   actually happened and the suggestion must be a concrete testable change.
   Write for a public reader; cite neither logs nor private paths. Do not
   copy the example as a finding.
4. Report the draft path. Do not commit the draft or run publication commands
   on your own. The operator can review and publish it using the
   [experiment procedure](../../../docs/experiment.md#publish-a-local-candidate).
