Feature: A caption field a human already filled is never overwritten

  A non-empty caption field was typed by someone who knew something the folder
  path does not say. YAIT fills empty metadata; it does not revise a value that
  is already there.

  Background:
    Given the collection of "UC-33-existing-fields-never-overwritten"

  Scenario: An existing human title survives a metadata write
    Given "2004-09 Bretagne/vieux scan.jpg" already has the title "Family house, summer 1974"
    When the media "2004-09 Bretagne/vieux scan.jpg" has its metadata written
    Then its title still reads "Family house, summer 1974"
    And the deduced label was not written to the title
