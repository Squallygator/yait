# UC-25 — A zero-byte file is a failed copy, not a photograph

| Field | Value |
|---|---|
| Group | `RG-2 File classification` |
| Status | `Enforced` ▶ |
| Stories | `US-03-06` |
| Legacy findings | — |

## Rule

A file of exactly zero bytes is classified as `unreadable`, whatever its
extension. It is reported as such in the inventory and is set aside from
processing — it is never renamed, moved, or counted as a real image with no
date.

## Why

Zero-byte files are almost always the residue of a copy that died: the
directory entry was created, the write never happened. A folder full of them is
how an interrupted `xcopy` or a full disk announces itself. They also turn up
where an antivirus or a sync client quarantined the real content and left the
husk behind.

Treating the husk as a photograph is worse than useless: it would get a target
name, take a slot in the collision check, and — if the tool ever wrote in
place — invite an empty file to be "normalised". Naming it for what it is puts
the operator back on the trail of the failed copy.

## Scope

This rule is the empty case only. A file with a valid header whose body is cut
short is *truncated*, not empty — `UC-24`; the two are separated because they
point at different failures (a truncated file means the source medium is
rotting, an empty one means a copy step failed). A recognised non-media
leftover — `Thumbs.db` and friends — is `UC-26` even when it happens to be
zero bytes, because there the *name* already tells the whole story.

## Counter-examples

- A 1-byte file containing a single newline — not zero bytes; it is `unreadable`
  under `UC-24` instead, same outcome, different rule.
- A zero-byte `Thumbs.db` — recognised by name first, classified `junk`
  (`UC-26`).
- A legitimately tiny but complete 1×1 PNG — has bytes, decodes, classified
  `image`.

## Decision

```
Status:      Enforced
Decided on:  2026-09-09                    Owner: squallygator
Rationale:   A zero-byte image file is the fingerprint of a copy that failed
             halfway. Carrying it through the pipeline as a dateless photo
             hides the failed copy and pollutes the collision check with a
             file that has no content to move.
Fallback:    n/a
Revisit if:  A workflow appears that deliberately uses zero-byte files as
             markers the tool should preserve in place rather than set aside.
Supersedes:  —
```

## Example

`files/damaged/empty-file.jpg` is exactly zero bytes. It must be classified
`unreadable` and kept out of the set of datable media. An implementation that
opens it, gets "no date", and files it with the undated holiday photos fails
the scenario.

Proven by [`rule.feature`](rule.feature).
