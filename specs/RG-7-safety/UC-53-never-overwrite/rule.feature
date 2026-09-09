Feature: An occupied destination is an error, never a silent suffix

  Planned collisions are resolved in the plan (RG-4). If a destination is
  occupied at execution time by something the plan did not foresee, the
  operation fails loudly — it does not append ~2 and carry on.

  Background:
    Given the collection of "UC-53-never-overwrite"

  Scenario: A move onto an occupied destination fails and touches nothing
    When the operation on "src/photo.jpg" finds its destination already occupied
    Then the operation fails rather than overwrite the file that is already there
    And no partial or temporary file is left beside it
