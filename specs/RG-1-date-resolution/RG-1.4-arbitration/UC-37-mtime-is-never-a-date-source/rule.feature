Feature: The filesystem modification time is never a capture date

  On a copied tree — which every recovered archive is — mtime is the copy date.
  A file with no other date stays undated; it does not fall back to mtime.

  Background:
    Given the collection of "UC-37-mtime-is-never-a-date-source"

  Scenario: With only an mtime available, the file is still undated
    When the media "Copie de Photos/IMG_1234.JPG" is inspected
    Then it has no resolved date
    And the date precision is "none"
