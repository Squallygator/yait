Feature: An unpadded digit after the year is a disc number, not a month

  A year burned across CDs gets folders named 2006-1, 2006-2, 2006-3. "2006-2" is
  not February; it is disc two. The folder keeps the year and nothing more.

  Background:
    Given the collection of "UC-16-batch-suffix-is-not-a-month"

  Scenario: "2006-2" resolves to the year only, not to February
    When the media "2006-2/family new year 025.jpg" is inspected
    Then its resolved date is "2006"
    And the date comes from "folder-name"
    And the date precision is "year"
