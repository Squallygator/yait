Feature: An unrecognised filename prefix is kept, not stripped

  Only prefixes on a known camera list are removed when building the label
  context. An unknown leading token is often the only thing the filename says
  about the photo, so it stays.

  Background:
    Given the collection of "UC-31-unknown-camera-prefix"

  Scenario: An unknown SANY prefix is retained in the label
    When the media "2012-06 Ouessant/SANY0032.jpg" is inspected
    Then its deduced label is "Ouessant - SANY0032"
