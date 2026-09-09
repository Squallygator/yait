Feature: A file that cannot be read is reported, never silently skipped

  A truncated JPEG is the signature of a failing disc. It must surface in the
  inventory as unreadable, not disappear into the pile of files with no date.

  Background:
    Given the collection of "UC-24-unreadable-is-detected"

  Scenario: A JPEG whose scan is cut short is classified as unreadable
    When the media "damaged/corrupt-scan.jpg" is inspected
    Then it is classified as "unreadable"
