Feature: HEIC/HEIF files are not opened to read their capture date

  Opening HEIC needs a new library. YAIT treats HEIC as opaque for dating and
  falls back to the name and folder, which an iPhone export always provides.

  Background:
    Given the collection of "UC-55-heic-not-inspected"

  Scenario: A .HEIC is dated by its folder, not by its embedded Exif
    When the media "2019-08 Algarve/IMG_2233.HEIC" is inspected
    Then its resolved date is "2019-08"
    And the date comes from "folder-name"
    And the date does not come from "embedded-metadata"
    And the date precision is "month"
