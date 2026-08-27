Feature: Windows Phone camera names embed the capture date

  Windows Phone named captures WP_YYYYMMDD followed by the time and an optional
  marker. The date is read from the name, which on these devices is often more
  reliable than a camera clock that reset to the epoch.

  Background:
    Given the collection of "UC-06-windows-phone"

  Scenario: The date is read from the WP_ head, past the trailing time and marker
    When the media "Camera Roll/WP_20140713_15_22_30_Pro.jpg" is inspected
    Then its resolved date is "2014-07-13"
    And the date comes from "file-name"
    And the date precision is "day"
