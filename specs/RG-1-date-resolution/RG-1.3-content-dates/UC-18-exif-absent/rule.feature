Feature: A still with no Exif date is normal, not a dead end

  Most of an old archive has no Exif. A missing capture-date tag is not a
  failure: resolution carries on to the filename and the folder.

  Background:
    Given the collection of "UC-18-exif-absent"

  Scenario: With no Exif, the folder still supplies the date
    When the media "vacances corse 2004/DSC_0009.JPG" is inspected
    Then its resolved date is "2004"
    And the date comes from "folder-name"
    And the date does not come from "embedded-metadata"
    And the date precision is "year"
