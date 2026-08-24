# RG-1.1 — Dates written in the filename

Rules that read a date out of the file's own name, whether a human typed it or a
device generated it.

The distinction matters for arbitration: a date a human wrote at the head of a
name is a deliberate act of filing and outranks a camera clock, whereas a
device-generated stamp is merely one more mechanical source.

## Rules

| Rule | Status | Decides |
|---|---|---|
| `UC-01-human-date-in-name` | ▶ | A leading `YYYY-MM-DD` is a filing decision, and outranks metadata |
| `UC-02-dropbox-camera-uploads` | ▶ | `2013-08-15 12.34.56` |
| `UC-03-whatsapp` | ▶ | `IMG-20161013-WA0001` |
| `UC-04-android-generated` | ▶ | `IMG_`/`VID_`/`PANO_`/`BURST_` + `YYYYMMDD` |
| `UC-05-screenshot` | ▶ | `Screenshot_2024-02-15-…` |
| `UC-06-windows-phone` | ▶ | `WP_20140713_…` |
| `UC-07-yyyymmdd-embedded` | ▶ | An isolated `YYYYMMDD` anywhere in the name |
| `UC-10-french-month-in-filename` | ▶ | `suede juin 2004 045.jpg` → month precision |
| `UC-11-numeric-month-in-name` | ▶ | `2011-12 photo` → month precision |
| `UC-12-year-only-in-name` | ▶ | `2011-Elliot` → year precision |

## Boundaries

What must **not** be read as a date — long identifiers, epoch stamps — is stated
in [RG-1.4](../RG-1.4-arbitration/group.md), because those are refusals, and a
refusal is an arbitration decision rather than a reading rule.
