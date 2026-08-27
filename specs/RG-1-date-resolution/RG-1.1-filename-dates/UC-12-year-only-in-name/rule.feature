Feature: A year on its own in the filename gives year precision

  Some files are only dated to the year. That is real information and is kept, but
  no month or day is invented from it.

  Background:
    Given the collection of "UC-12-year-only-in-name"

  Scenario: A lone year resolves at year precision, with no fabricated month or day
    When the media "albums/2011 - family reunion.jpg" is inspected
    Then its resolved date is "2011"
    And the date comes from "file-name"
    And the date precision is "year"
