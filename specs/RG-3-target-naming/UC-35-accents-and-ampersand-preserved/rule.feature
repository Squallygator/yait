Feature: Accents, ampersands and parentheses are kept in the target name

  The archive is French. Names are not transliterated, lower-cased or
  punctuation-stripped; only the characters that are actually unsafe go.

  Background:
    Given the collection of "UC-35-accents-and-ampersand-preserved"

  Scenario: An accented, ampersand-and-parenthesis name survives intact
    When the media "2004-07 corse/Étretat & la plage (2).jpg" is inspected
    Then its target name is "2004-07-Étretat & la plage (2).jpg"
