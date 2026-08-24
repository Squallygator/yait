# Business language only. No file formats, no function names, no "the parser".
# One scenario is the target. If you need several, say why in rule.md.

Feature: <the rule stated as an outcome>

  <One or two sentences of context, the same intent as rule.md's Rule section,
  so the scenario reads standalone in a test report.>

  Background:
    Given the collection of "UC-nn-slug"

  Scenario: <what this specific example proves>
    When the media "<relative/path.jpg>" is inspected
    Then its resolved date is "YYYY-MM-DD"
    And the date comes from "<file-name|folder-name|embedded-metadata|sidecar|none>"
    And the date precision is "<day|month|year|none>"

  # For an assumed exclusion, assert the FALLBACK, never the absence:
  #
  #   Scenario: an epoch timestamp in the name is not read as a capture date
  #     When the media "FB_IMG_1288000000.jpg" is inspected
  #     Then the date does not come from "file-name"
  #     And its resolved date is "2010-05-08"
  #     And the date comes from "folder-name"
