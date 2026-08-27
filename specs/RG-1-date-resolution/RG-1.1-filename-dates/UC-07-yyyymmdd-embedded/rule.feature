Feature: An isolated YYYYMMDD in the name is a date

  Many files carry a date with no device signature at all: a plain eight-digit
  run. When it stands alone and forms a real calendar date, it is read.

  Background:
    Given the collection of "UC-07-yyyymmdd-embedded"

  Scenario: A leading unprefixed eight-digit date is read
    When the media "scans/20080614_sunset_over_the_bay.jpg" is inspected
    Then its resolved date is "2008-06-14"
    And the date comes from "file-name"
    And the date precision is "day"
