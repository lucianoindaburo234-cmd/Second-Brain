# Second Brain — vault instructions

This repository is an Obsidian vault. Open **this folder** as the vault root.

## Structure

| Folder | What belongs there |
|---|---|
| `00-inbox` | Unprocessed capture. Nothing lives here permanently. |
| `10-context` | Stable facts about me: setup, goals, preferences, people. |
| `20-wiki` | Evergreen reference knowledge, one topic per note. |
| `30-projects` | Active work with a goal and an end date, one folder each. |
| `40-skills` | Repeatable procedures written to be executed. |
| `90-meta` | Conventions, templates and upkeep for the vault itself. |

Numbering leaves room for future top-level sections (50–80). Each folder's own
`README.md` states in more detail what belongs there and what doesn't.

## How to work in this vault

- **Filing.** When a note's home is obvious, put it there. When it isn't, put it
  in `00-inbox` rather than guessing — sorting later is cheap, finding a
  misfiled note is not.
- **Naming.** Name notes after the idea, not the date or the source:
  `spaced-repetition.md`, not `notes-from-video-3.md`.
- **Linking.** Use Obsidian wikilinks (`[[note-name]]`) between notes. The links
  are what make this a brain rather than a folder of files.
- **Rewriting.** Prefer sharpening an existing note over appending to it. Notes
  should get shorter and clearer over time, not longer.
- **Front matter.** Optional. When used, keep it to `tags`, `created`, and
  `source`.

## Conventions for Claude

- Ask before moving or deleting existing notes; freely create new ones.
- When a note fits more than one folder, pick one and link from the other —
  never duplicate content across folders.
- When work in `30-projects` produces something reusable, offer to distill it
  into `20-wiki` (knowledge) or `40-skills` (procedure) before archiving.
- Match the voice of the surrounding notes: plain, direct, no filler.
