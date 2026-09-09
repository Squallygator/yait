Feature: Running the namer twice changes nothing the second time

  The one safe recovery from an interrupted batch is to run it again. A file
  already in target form must be a fixed point, or the re-run corrupts names it
  had already fixed.

  Background:
    Given the collection of "UC-41-idempotent-on-rerun"

  Scenario: A file already in target form keeps its exact name
    When the media "2007-08-25 retour/2007-08-25-arrivee ferry.jpg" is inspected
    Then its target name is "2007-08-25-arrivee ferry.jpg"
