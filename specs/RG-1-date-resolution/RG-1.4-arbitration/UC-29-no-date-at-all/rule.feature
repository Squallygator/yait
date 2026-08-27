Feature: When nothing answers, the file is undated, and that is a real state

  Some files cannot be dated from what is on disk. "Undated" is an explicit,
  visible outcome, not an error and not a guess.

  Background:
    Given the collection of "UC-29-no-date-at-all"

  Scenario: No name, folder, or content date leaves the file undated
    When the media "Originals/scan.jpg" is inspected
    Then it has no resolved date
    And the date precision is "none"
