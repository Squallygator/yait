Feature: A caption in place is compared to its proposal ignoring case, accents and spacing

  Whether a caption already matches the label YAIT would write decides its
  status, and the "divergent" status is the one a person reads closely. Capital
  letters, missing accents and stray spaces are not a difference worth that
  attention; a different word or a different punctuation mark is.

  Background:
    Given the collection of "UC-61-status-comparison-is-normalised"

  Scenario: Capital letters do not make a caption divergent
    Given "2005-08 Rome/le Forum.jpg" already has the title "ROME - LE FORUM"
    When the media "2005-08 Rome/le Forum.jpg" is audited for metadata
    Then its deduced label is "Rome - le Forum"
    And its title status is "compliant"

  Scenario: Missing accents do not make a caption divergent
    Given "2004-07 corse/Étretat & la plage (2).jpg" already has the title "Corse - Etretat & la plage (2)"
    When the media "2004-07 corse/Étretat & la plage (2).jpg" is audited for metadata
    Then its deduced label is "corse - Étretat & la plage (2)"
    And its title status is "compliant"

  Scenario: Extra spaces do not make a caption divergent
    Given "2003-07 corse/plage.jpg" already has the title "  corse   -   plage  "
    When the media "2003-07 corse/plage.jpg" is audited for metadata
    Then its deduced label is "corse - plage"
    And its title status is "compliant"

  Scenario: A different caption is divergent
    Given "2004-09 Bretagne/menhir debout.jpg" already has the title "Menhir de Carnac"
    When the media "2004-09 Bretagne/menhir debout.jpg" is audited for metadata
    Then its deduced label is "Bretagne - menhir debout"
    And its title status is "divergent"

  Scenario: A different punctuation mark is a difference
    Given "2006-05 disc 1/plage.jpg" already has the title "disc 1 – plage"
    When the media "2006-05 disc 1/plage.jpg" is audited for metadata
    Then its deduced label is "disc 1 - plage"
    And its title status is "divergent"
