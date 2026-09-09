Feature: A zero-byte file is a failed copy, not a photograph

  An empty image file is the residue of a copy that died mid-write. It surfaces
  as unreadable and is kept out of the datable set.

  Background:
    Given the collection of "UC-25-zero-byte-file"

  Scenario: An empty .jpg is classified as unreadable
    When the media "damaged/empty-file.jpg" is inspected
    Then it is classified as "unreadable"
