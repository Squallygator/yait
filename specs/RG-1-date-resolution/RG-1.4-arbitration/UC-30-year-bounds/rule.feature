Feature: A candidate date outside the plausible year range is rejected

  Every source emits an implausible date now and then. A single range gate
  (1970 to the processing date) discards them, and resolution continues.

  Background:
    Given the collection of "UC-30-year-bounds"

  Scenario: A far-future date in the filename is rejected and the folder answers
    When the media "2015-08 wedding/note-20991231.jpg" is inspected
    Then its resolved date is "2015-08"
    And the date comes from "folder-name"
    And the date does not come from "file-name"
    And the date precision is "month"
