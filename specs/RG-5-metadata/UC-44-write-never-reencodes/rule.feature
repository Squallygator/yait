Feature: Writing metadata never re-encodes the image

  JPEG re-saves lose detail every time. A metadata write rebuilds only the
  header; the compressed scan is spliced back byte for byte.

  Background:
    Given the collection of "UC-44-write-never-reencodes"

  Scenario: The compressed scan is untouched by a metadata write
    When the media "2003-07 corse/plage.jpg" has its metadata written
    Then the compressed image is byte-for-byte unchanged
    And its title, subject and comment all read "corse - plage"
