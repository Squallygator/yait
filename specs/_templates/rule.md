# UC-nn — <one line, the rule stated as an outcome>

| Field | Value |
|---|---|
| Group | `RG-x.y <group name>` |
| Status | `Enforced` ▶ *or* `Assumed exclusion` ⊘ |
| Stories | `US-nn-mm` |
| Legacy findings | `#n` *(dvd-tools audit, if any)* |

## Rule

<One paragraph, in business language. State what happens, not how it is coded.
A reader who has never opened the source must be able to tell whether this is
the behaviour they want.>

## Why

<The reasoning, and the observation that produced it. This is the section that
survives: in five years nobody will remember why folder dates beat camera
clocks, and the code will not say. Quote the real-world case that forced the
decision — an archive where the camera clock was never set, a filename whose
digits decoded to yesterday for a fifteen-year-old photograph.>

## Scope

<What this rule does NOT decide, and which sibling rule does. Rules that quietly
overlap are how a specification rots.>

## Counter-examples

<Inputs that look like they should trigger this rule and must not. One line
each. These are as important as the positive case: they are what stops a
regex from getting greedy in six months.>

## Decision

```
Status:      Enforced | Assumed exclusion
Decided on:  YYYY-MM-DD                    Owner: <name>
Rationale:   <why this way, in one or two sentences>
Fallback:    <for an exclusion: what happens instead. For an enforced rule: "n/a">
Revisit if:  <the concrete signal that should reopen this decision>
Supersedes:  <UC-nn of a deleted rule this replaces, or "—">
```

## Example

`files/<the sample>` — <one line on what makes it the right example>

Proven by [`rule.feature`](rule.feature).
