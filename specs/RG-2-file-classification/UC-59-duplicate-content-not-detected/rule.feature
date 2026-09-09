Feature: Identical content in two files is not detected or merged

  YAIT does not hash file contents to find duplicates. Two byte-identical files
  with different names are each processed on their own; only a clash on the
  target name is reconciled, and even then both files are kept.

  Background:
    Given the collection of "UC-59-duplicate-content-not-detected"

  Scenario: Two identical files each keep a target name from their own stem
    When the media "2007-08 corse/sunset.jpg" is inspected
    Then its target name is "2007-08-sunset.jpg"
    When the media "2007-08 corse/sunset (copy).jpg" is inspected
    Then its target name is "2007-08-sunset (copy).jpg"
