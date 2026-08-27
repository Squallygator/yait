Feature: An AVI's capture date comes from its IDIT chunk

  AVI carries no Exif. 2000s camcorders wrote the capture time into the RIFF IDIT
  chunk as a C asctime string, and that is where the date is read.

  Background:
    Given the collection of "UC-20-video-riff-idit"

  Scenario: The IDIT asctime string dates the clip
    When the media "holidays/MVI_0031.AVI" is inspected
    Then its resolved date is "2006-08-29"
    And the date comes from "embedded-metadata"
    And the date precision is "day"
