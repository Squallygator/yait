Feature: RAW files are not opened to read their capture date

  Reading a date out of a camera-RAW file reliably needs a RAW library — a new
  frozen dependency. YAIT treats RAW as opaque for dating and falls back to the
  name and folder.

  Background:
    Given the collection of "UC-54-raw-not-inspected"

  Scenario: A .CR2 is dated by its folder, not by its embedded Exif
    When the media "2016-05 Iceland/IMG_8801.CR2" is inspected
    Then its resolved date is "2016-05"
    And the date comes from "folder-name"
    And the date does not come from "embedded-metadata"
    And the date precision is "month"
