Feature: Archives are read one level deep, not recursed

  An archive is dated from the entries it directly contains. An entry that is
  itself an archive is not opened, and nothing inside it counts.

  Background:
    Given the collection of "UC-58-nested-zip-not-recursed"

  Scenario: A nested-archive entry does not lower the outer archive's date
    When the media "backups/2012-full-backup.zip" is inspected
    Then its resolved date is "2012-07-10"
    And the date comes from "embedded-metadata"
    And the date precision is "day"
