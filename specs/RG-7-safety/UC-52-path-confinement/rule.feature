Feature: A path from outside cannot escape the collection root

  CSV cells and replayed journal entries can carry ..-traversal, absolute paths
  or escaping symlinks. Every externally supplied path is resolved and confined
  to the collection root before anything acts on it.

  Background:
    Given the collection of "UC-52-path-confinement"

  Scenario: An operation aimed outside the root is rejected
    Given the media "inside/kept.jpg" is in the collection
    When an operation is handed the path "../../secrets/passwords.txt"
    Then the path is rejected as outside the collection
    And nothing outside the collection root is read or written
