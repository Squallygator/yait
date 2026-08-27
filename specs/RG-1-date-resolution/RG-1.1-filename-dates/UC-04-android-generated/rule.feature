Feature: Android camera names embed the capture date

  Stock Android and Google Photos name captures IMG_/VID_/PANO_/BURST_ followed
  by YYYYMMDD and then the time. The date is read from the name and the trailing
  time is discarded.

  Background:
    Given the collection of "UC-04-android-generated"

  Scenario: The date is read and the trailing capture time is discarded
    When the media "DCIM/Camera/IMG_20150704_193000.jpg" is inspected
    Then its resolved date is "2015-07-04"
    And the date comes from "file-name"
    And the date precision is "day"
