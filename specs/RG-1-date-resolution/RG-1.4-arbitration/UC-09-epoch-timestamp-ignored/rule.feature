Feature: An epoch timestamp in the name dates the transfer, not the photograph

  Facebook and Messenger name saved images with the epoch second at which they
  processed the file. That is the download, not the shot, and for an old photo it
  is years wrong.

  Background:
    Given the collection of "UC-09-epoch-timestamp-ignored"

  Scenario: An FB_IMG epoch stamp is ignored; the folder dates the photo
    When the media "2003 vacances/FB_IMG_1288000000.jpg" is inspected
    Then its resolved date is "2003"
    And the date comes from "folder-name"
    And the date does not come from "file-name"
    And the date precision is "year"
