Feature: The journal entry is written and flushed before the operation runs

  One JSONL line per operation, on disk before the change it describes. After a
  crash the journal is a precise record of everything that had started — a
  recovery mechanism, not a log written at the end.

  Background:
    Given the collection of "UC-50-journal-written-ahead"

  Scenario: The rename is journalled and flushed before the file moves
    When the operation on "originals/portrait.jpg" is about to run
    Then the journal already records the operation, flushed, before the file changes
