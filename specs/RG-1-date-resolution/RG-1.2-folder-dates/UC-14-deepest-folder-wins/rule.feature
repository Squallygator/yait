Feature: The deepest dated folder wins over its ancestors

  Archives are filed in layers: a folder for the event, subdivided by day as the
  photographs arrive. The inner folder is the more specific statement about when
  these files belong, and it prevails.

  Background:
    Given the collection of "UC-14-deepest-folder-wins"

  Scenario: A day folder inside an event folder dates the photograph
    When the media "2002-07-20 Wedding at Arras/18-07-2002/026-the-couple-and-the-mother.jpg" is inspected
    Then its resolved date is "2002-07-18"
    And the date comes from "folder-name"
    And the date precision is "day"
