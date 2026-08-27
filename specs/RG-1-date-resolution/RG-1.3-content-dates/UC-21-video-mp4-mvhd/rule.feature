Feature: An MP4/MOV's capture date comes from the moov/mvhd atom

  MP4 and MOV videos keep the capture instant in moov/mvhd creation_time, counted
  from the 1904 QuickTime epoch. The calendar date is read from it.

  Background:
    Given the collection of "UC-21-video-mp4-mvhd"

  Scenario: The mvhd creation_time dates the clip
    When the media "holidays/MVI_0032.MOV" is inspected
    Then its resolved date is "2011-06-04"
    And the date comes from "embedded-metadata"
    And the date precision is "day"
