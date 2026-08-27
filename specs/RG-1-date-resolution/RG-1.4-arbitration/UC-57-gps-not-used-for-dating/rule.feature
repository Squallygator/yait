Feature: GPS metadata is never used to resolve a capture date

  GPSDateStamp is the UTC satellite-fix time, not the shutter time. When the
  capture-date tags are absent, the GPS timestamp is not used as a substitute;
  resolution falls to the name and folder.

  Background:
    Given the collection of "UC-57-gps-not-used-for-dating"

  Scenario: With no capture-date tag, the folder answers, not GPS
    When the media "2013-07 Sicily/DSCN2043.JPG" is inspected
    Then its resolved date is "2013-07"
    And the date comes from "folder-name"
    And the date does not come from "embedded-metadata"
    And the date precision is "month"
