# Copilot compatibility

The local feedback path is the same development chat, a repository skill,
and optionally `gh` after an operator approves publication. It does not depend
on access to the IDE's transcript files.

| Primitive | Visual Studio | Copilot CLI |
|---|---|---|
| Agent runs terminal commands | [Agent mode](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-agent-mode?view=visualstudio) starts at Visual Studio 2022 17.14. Terminal commands can require confirmation. `gh` needs its own sign-in. | A developer can grant specific terminal tools for a CLI session. |
| Project skill | [Visual Studio 2026 18.5+](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-agent-skills?view=visualstudio) discovers `.github/skills/` in Agent mode. The agent chooses whether to activate it. | Discovers the same project skills. An explicit request in the same session is the fallback. |
| Completion instruction | [Repository instructions](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-chat-context?view=visualstudio) must be enabled. An instruction is not an event handler. | Uses the same `.github/copilot-instructions.md`. |
| Reusable prompt | Prompt files under `.github/prompts/` can be selected in chat. | Use the equivalent text in chat; prompt files are not on the [CLI support matrix](https://docs.github.com/en/copilot/reference/customization-cheat-sheet#ide-and-surface-support). |
| Stop or session-end hook | [GitHub lists hooks as unsupported](https://docs.github.com/en/copilot/reference/customization-cheat-sheet#ide-and-surface-support). Do not rely on quitting or closing chat as a trigger. | [Hooks](https://docs.github.com/en/copilot/reference/hooks-reference) exist but are not part of this shared path. |

Visual Studio compatibility here is based on documentation. Verify the actual
Visual Studio version, Agent mode, skill discovery, and the terminal approval
flow on the target workstation before rollout.

The PR workflow uses [GitHub Models from Actions](https://github.blog/ai-and-ml/llms/solving-the-inference-problem-for-open-source-ai-projects-with-github-models/)
for inference, not Copilot CLI or a Copilot session export. This avoids
installing a personal Copilot token into a public lab. A Copilot-driven
[agentic workflow](https://docs.github.com/en/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows)
can use the same evidence and issue format, but its Copilot access and billing
need separate validation.
