Feature: Embedded date far from the folder date is treated as clock drift

  A camera with an unset clock stamps a fixed wrong date on a whole shoot. When
  the embedded date is more than a year from the folder date, the folder — filed
  by a person who knew the occasion — wins.

  Background:
    Given the collection of "UC-19-clock-drift-guard"

  Scenario: An Exif date nine years off the folder is discarded for the folder date
    When the media "2009-06 Corsica/IMG_0007.JPG" is inspected
    Then its resolved date is "2009-06"
    And the date comes from "folder-name"
    And the date does not come from "embedded-metadata"
    And the date precision is "month"
