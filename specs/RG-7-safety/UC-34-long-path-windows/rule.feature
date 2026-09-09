Feature: Paths beyond 260 characters still work

  Deep archives cross Windows' legacy 260-character limit, past which naive file
  APIs fail — often silently. A file there is inventoried, named and organised
  like any other, never skipped for its path length.

  Background:
    Given the collection of "UC-34-long-path-windows"

  Scenario: A long, deep path is handled like a short one
    When the media "deeply nested archive folder from an old backup disc/one more level down the tree/family gathered on the beach at sunset.jpg" is inspected
    Then it is classified as "image"
    And a file whose full path exceeds 260 characters is not skipped for its length
