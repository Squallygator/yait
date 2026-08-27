Feature: Which written forms count as a folder date

  Hand-labelled folders spell the same date many ways. This is the registry of
  the accepted numeric forms; the example takes the least obvious separator.

  Background:
    Given the collection of "UC-13-folder-date-formats"

  Scenario: An underscore-separated date in a descriptive folder name is read
    When the media "2002_07_20 Wedding at Arras/img_0042.jpg" is inspected
    Then its resolved date is "2002-07-20"
    And the date comes from "folder-name"
    And the date precision is "day"
