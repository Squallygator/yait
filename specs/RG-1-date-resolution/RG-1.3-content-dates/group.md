# RG-1.3 — Dates read from the file's content

Metadata embedded in the file: Exif for stills, container atoms for video, entry
timestamps for archives — and the thumbnail sidecar that is sometimes a video's
only witness.

Reading is native wherever possible. `ffprobe` is used when present but is never
required: an archive must be processable on a machine with nothing installed.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-17-exif-capture-date` | ▶ | `DateTimeOriginal` and its fallbacks |
| `UC-18-exif-absent` | ▶ | What happens when a still carries no metadata |
| `UC-20-video-riff-idit` | ▶ | AVI `IDIT` chunk |
| `UC-21-video-mp4-mvhd` | ▶ | MP4/MOV `moov/mvhd` atom |
| `UC-22-video-dated-by-thm-sidecar` | ▶ | A `.THM` thumbnail dates its video |
| `UC-23-zip-oldest-exif` | ▶ | An archive takes the oldest date it contains |
| `UC-54-raw-not-inspected` | ⊘ | CR2/NEF/ARW: fall back to name and folder |
| `UC-55-heic-not-inspected` | ⊘ | HEIC would require a new runtime dependency |
| `UC-58-nested-zip-not-recursed` | ⊘ | One level of archive, no deeper |

## Boundaries

That a `.THM` survives the junk filter as long as its video exists is a
classification rule: [RG-2](../../RG-2-file-classification/group.md), `UC-38`.
