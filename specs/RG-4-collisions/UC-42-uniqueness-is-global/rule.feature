Feature: Target-name uniqueness is checked across the whole collection

  A normalised collection ends up flat, so two files in different folders that
  resolve to the same name are a collision — caught while the plan can still add
  a suffix, not after the files are moved together.

  Background:
    Given the collection of "UC-42-uniqueness-is-global"

  Scenario: Two identical stems in different folders collide and one is suffixed
    When the media "2006-05 disc 1/plage.jpg" is inspected
    Then its target name is "2006-05-14-plage.jpg"
    When the media "2006-05 disc 2/plage.jpg" is inspected
    Then its target name is "2006-05-14-plage_1.jpg"
