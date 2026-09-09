Feature: Undo restores the file bit for bit, not approximately

  Undo reinstates the kept original bytes; it does not rebuild them from a
  parsed model. An operation and its undo round-trip to the identity.

  Background:
    Given the collection of "UC-51-undo-restores-bit-for-bit"

  Scenario: Undoing a rename puts the file back with identical bytes
    When the operation on "2007-08 corse/IMG_0042.jpg" is undone
    Then the file is back at "2007-08 corse/IMG_0042.jpg" with identical bytes
