Feature: An archive takes the oldest date it contains

  A zipped bag of photos has no single capture time. The oldest date among its
  entries is chosen, so a late addition cannot drag the archive's date forward.

  Background:
    Given the collection of "UC-23-zip-oldest-exif"

  Scenario: The oldest entry dates the archive, wherever it sits in the listing
    When the media "backups/holiday-photos.zip" is inspected
    Then its resolved date is "2009-12-24"
    And the date comes from "embedded-metadata"
    And the date precision is "day"
