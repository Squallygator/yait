Feature: A French month name in a folder gives month precision

  Envelope-style folder labels name a month, not a day. A number beside the month
  is not read as a day of month.

  Background:
    Given the collection of "UC-15-folder-french-month"

  Scenario: "22 JUILLET 2002" resolves to July 2002 at month precision
    When the media "22 JUILLET 2002/numérisation 08.jpg" is inspected
    Then its resolved date is "2002-07"
    And the date comes from "folder-name"
    And the date precision is "month"
