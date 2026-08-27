Feature: Dropbox Camera Uploads names carry a full timestamp

  Dropbox renames every imported photo to "YYYY-MM-DD HH.MM.SS", taken from the
  device at upload time, with dots for the time because a colon is not allowed in
  a filename. The calendar date is read from it.

  Background:
    Given the collection of "UC-02-dropbox-camera-uploads"

  Scenario: The dotted time and the collision suffix are both consumed
    When the media "Camera Uploads/2013-08-15 12.34.56-2.jpg" is inspected
    Then its resolved date is "2013-08-15"
    And the date comes from "file-name"
    And the date precision is "day"
