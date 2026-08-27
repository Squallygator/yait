Feature: A .THM thumbnail dates its video

  Camcorders wrote a tiny full-Exif JPEG beside every clip. When the video's own
  container has no usable date, that .THM thumbnail supplies it.

  Background:
    Given the collection of "UC-22-video-dated-by-thm-sidecar"

  Scenario: The video takes its date from the sibling .THM
    When the media "CANON/MVI_2468.AVI" is inspected
    Then its resolved date is "2005-12-25"
    And the date comes from "sidecar"
    And the date precision is "day"
