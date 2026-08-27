Feature: A leading human-typed date outranks the camera clock

  A filename that begins with YYYY-MM-DD was named by a person who decided when
  the file belongs. That decision is trusted over the date stored in the file's
  own metadata, which is often an unset or wrong camera clock.

  Background:
    Given the collection of "UC-01-human-date-in-name"

  Scenario: The leading date wins over a much later digitisation date in metadata
    When the media "Scans/1974-08-11 grandparents house 03.jpg" is inspected
    Then its resolved date is "1974-08-11"
    And the date comes from "file-name"
    And the date does not come from "embedded-metadata"
    And the date precision is "day"
