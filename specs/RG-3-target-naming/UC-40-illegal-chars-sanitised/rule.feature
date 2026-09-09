Feature: Characters Windows refuses are removed from the target name

  A proposed name that Windows would reject or silently rewrite breaks the
  journal and undo. The name is sanitised so the plan matches the disk.

  Background:
    Given the collection of "UC-40-illegal-chars-sanitised"

  Scenario: A trailing dot and space on the description are stripped
    When the media "scans/holiday day 1. .jpg" is inspected
    Then its target name is "2005-08-01-holiday day 1.jpg"
