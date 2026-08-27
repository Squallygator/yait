Feature: The full source priority order

  When several sources yield different dates for one file, an ordered list
  decides: a human filing decision, then the camera's shutter record, then a
  named folder, then a coarse filename guess, then nothing.

  Background:
    Given the collection of "UC-36-source-priority-order"

  Scenario: Exif beats a bare filename date and a deeper folder date
    When the media "2007-08-25 retour/20070815 arrivee ferry.JPG" is inspected
    Then its resolved date is "2007-08-20"
    And the date comes from "embedded-metadata"
    And the date precision is "day"
