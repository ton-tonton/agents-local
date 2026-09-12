## Communication
- Use simple language for a non-native English. Use common, everyday words.
- Answer first; explain only as much as the decision needs. No preamble or filler.
- Be concise and clear, prefer bullet points over long paragraphs.
- Ask when ambiguity changes what you'd do; otherwise take the sensible default.

## Environment
These CLI tools are installed — prefer them in shell commands:
- `rg` — search file contents
- `fd` — find files
- `jq` — query/transform JSON
- `tree` — show directory trees
- `mise` — manage tool/runtime versions

## Code values
- Optimize for readability; keep diffs focused, no drive-by reformatting.
- Handle errors and edge cases explicitly.
- Name things clearly so code explains itself.
- Ask before large refactors, cross-file renames, or public interface changes.

## Safety
- Never commit secrets — use env vars or a secrets manager.
- Confirm before destructive or hard-to-reverse actions (history rewrites, force pushes, data drops, deleting files you didn't create).
- Commit or push only when asked.
- Report outcomes faithfully; if tests fail, show the output.

