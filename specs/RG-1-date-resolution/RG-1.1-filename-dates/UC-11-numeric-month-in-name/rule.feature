Feature: A numeric YYYY-MM in the filename gives month precision

  A filename with YYYY-MM and a trailing number is a month of pictures with a
  running count. The number is not a day, and no day is invented.

  Background:
    Given the collection of "UC-11-numeric-month-in-name"

  Scenario: "2011-12 christmas market 08" resolves to December 2011, month precision
    When the media "divers/2011-12 christmas market 08.jpg" is inspected
    Then its resolved date is "2011-12"
    And the date comes from "file-name"
    And the date precision is "month"
