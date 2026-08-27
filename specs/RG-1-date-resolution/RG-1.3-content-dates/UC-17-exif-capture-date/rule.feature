Feature: A still's capture date comes from Exif, DateTimeOriginal first

  The Exif date tags are consulted in a fixed order of preference:
  DateTimeOriginal, then DateTimeDigitized, then DateTime. A later tag fills in
  only when an earlier one is missing.

  Background:
    Given the collection of "UC-17-exif-capture-date"

  Scenario: DateTimeOriginal is used even when DateTimeDigitized disagrees
    When the media "holidays/IMG_0042.JPG" is inspected
    Then its resolved date is "2006-08-29"
    And the date comes from "embedded-metadata"
    And the date precision is "day"
