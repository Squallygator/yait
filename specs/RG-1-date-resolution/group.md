# RG-1 — Date resolution

The heart of the tool. Given a file, decide **when it was taken** — and record
**why** that answer was chosen.

Four sub-groups, in the order the resolver consults them: the filename, the
folder path, the file's own content, and finally the arbitration rules that
decide who wins when several sources disagree.

Every resolved date carries its source. A right date obtained for the wrong
reason is a bug waiting for the next batch of DVDs.

| Sub-group | Answers |
|---|---|
| [RG-1.1](RG-1.1-filename-dates/group.md) | What the filename says |
| [RG-1.2](RG-1.2-folder-dates/group.md) | What the folder path says |
| [RG-1.3](RG-1.3-content-dates/group.md) | What the file itself says |
| [RG-1.4](RG-1.4-arbitration/group.md) | Who wins, and what is refused |

## Boundaries

Turning a resolved date into a filename is [RG-3](../RG-3-target-naming/group.md).
Deciding a file is junk or unreadable is [RG-2](../RG-2-file-classification/group.md).
