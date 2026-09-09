Feature: Placement follows the precision of the resolved date

  The tree is only as deep as the date is certain: day or month to YYYY/MM,
  year to YYYY, nothing to _undated. A year-only file is never given a month.

  Background:
    Given the collection of "UC-46-organize-by-precision"

  Scenario: Each precision lands at its own depth
    When the media "2011-06-14 rando/a.jpg" is inspected
    Then it is filed under "2011/06/"
    When the media "2009 albums/b.jpg" is inspected
    Then it is filed under "2009/"
    When the media "sans date/c.jpg" is inspected
    Then it is filed under "_undated/"
