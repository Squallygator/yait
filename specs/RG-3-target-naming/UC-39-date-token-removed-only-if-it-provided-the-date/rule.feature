Feature: A date token is dropped from the description only if it supplied the date

  The token the resolver used is removed from the name so it is not written
  twice. A second date-shaped run of digits that carried meaning stays.

  Background:
    Given the collection of "UC-39-date-token-removed-only-if-it-provided-the-date"

  Scenario: The used token goes, a second bare year is kept
    When the media "Scans/2003-07-14 - 1998 reunion rescan.jpg" is inspected
    Then the date comes from "file-name"
    And its target name is "2003-07-14-1998 reunion rescan.jpg"
