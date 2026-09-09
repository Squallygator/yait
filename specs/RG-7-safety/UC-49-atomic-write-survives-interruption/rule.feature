Feature: An interrupted write never truncates the original

  Every write goes to a temp file in the same directory, then a single atomic
  replace. A crash at any point during the write leaves the original complete.

  Background:
    Given the collection of "UC-49-atomic-write-survives-interruption"

  Scenario: A metadata write killed partway leaves the original whole
    When the operation on "originals/portrait.jpg" is interrupted before it completes
    Then the original file is intact, byte for byte
    And no partial or temporary file is left beside it
