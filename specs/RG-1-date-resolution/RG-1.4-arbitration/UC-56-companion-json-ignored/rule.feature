Feature: Google Takeout companion JSON is not read for a date

  A Takeout .json sidecar carries a photoTakenTime that is frequently wrong. The
  media is dated from its own Exif, name and folder, as if the JSON were absent.

  Background:
    Given the collection of "UC-56-companion-json-ignored"

  Scenario: The .json photoTakenTime is ignored; the folder dates the photo
    When the media "2018-09 Rome/IMG_1234.JPG" is inspected
    Then its resolved date is "2018-09"
    And the date comes from "folder-name"
    And the date does not come from "sidecar"
    And the date precision is "month"
