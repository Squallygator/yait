Feature: Screenshot names carry the capture date

  Android screenshots carry no metadata, so the name is the only witness. It
  reads Screenshot_YYYY-MM-DD followed by the time and the foreground app. The
  date is taken; the time and the app name are not.

  Background:
    Given the collection of "UC-05-screenshot"

  Scenario: The leading date is read past the time and the app package name
    When the media "Pictures/Screenshots/Screenshot_2024-02-15-08-13-22-123_com.example.app.png" is inspected
    Then its resolved date is "2024-02-15"
    And the date comes from "file-name"
    And the date precision is "day"
