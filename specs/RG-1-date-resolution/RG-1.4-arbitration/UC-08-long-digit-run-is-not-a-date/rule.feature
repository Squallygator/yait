Feature: A long run of digits is an identifier, never mined for a date

  Messenger and Facebook ids are long opaque digit runs. Any eight-digit slice
  of them can parse to a plausible date, and all such dates are meaningless, so
  none is read.

  Background:
    Given the collection of "UC-08-long-digit-run-is-not-a-date"

  Scenario: A fifteen-digit id yields no filename date; the folder answers
    When the media "2015-07 Barcelona/received_862666160799536.jpg" is inspected
    Then its resolved date is "2015-07"
    And the date comes from "folder-name"
    And the date does not come from "file-name"
    And the date precision is "month"
