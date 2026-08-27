Feature: A French month name in the filename gives month precision

  Pre-phone files were named like a shoebox label: a place, a month in letters, a
  year, a running number. There is no day, and the trailing number is a batch
  counter.

  Background:
    Given the collection of "UC-10-french-month-in-filename"

  Scenario: "suède juin 2004 045" resolves to June 2004 at month precision
    When the media "numérisations/suède juin 2004 045.jpg" is inspected
    Then its resolved date is "2004-06"
    And the date comes from "file-name"
    And the date precision is "month"
