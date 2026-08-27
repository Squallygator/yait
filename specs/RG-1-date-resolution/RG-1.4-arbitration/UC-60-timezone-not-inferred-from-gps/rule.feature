Feature: Timestamps are kept as written; no timezone is applied

  Exif local time is the answer people want. No conversion to UTC and no
  GPS-derived timezone shift is applied, so a near-midnight shot keeps its day.

  Background:
    Given the collection of "UC-60-timezone-not-inferred-from-gps"

  Scenario: A 23:30 capture keeps its calendar day
    When the media "2006-08 birthday/IMG_0512.JPG" is inspected
    Then its resolved date is "2006-08-29"
    And the date comes from "embedded-metadata"
    And the date precision is "day"
