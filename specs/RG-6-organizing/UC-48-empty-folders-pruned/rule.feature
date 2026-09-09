Feature: A source folder left empty by the move is pruned, and only then counted

  Pruning hollow folders is the visible sign a reorg finished. A folder that
  still holds something the organiser did not move stays, and the pruned count
  is real removals, not candidates.

  Background:
    Given the collection of "UC-48-empty-folders-pruned"

  Scenario: Emptied folders go, a folder with a leftover file stays
    When the collection is organized
    Then the folder "alpha/beta" has been pruned
    And the folder "alpha" has been pruned
    And the folder "gamma" is left in place
