Feature: Flatten leaves an undated file where it is

  A flat pile is navigable only by the YYYY-MM-DD name. An undated file has no
  such name, so flatten leaves it in its folder — its last thread of context —
  for a human to date, rather than losing it in the pile.

  Background:
    Given the collection of "UC-47-flatten-leaves-undated-in-place"

  Scenario: The dated file flattens, the undated one stays put
    When the collection is flattened
    Then the media "divers/mystere.jpg" stays at "divers/mystere.jpg"
