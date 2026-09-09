Feature: A file that changed since the audit is not written blind

  The audit fingerprints every file. If a file's bytes change before the plan is
  applied, its write is refused and it is left alone — the operator may have
  edited it in the meantime.

  Background:
    Given the collection of "UC-45-drift-detected"

  Scenario: A file edited between audit and apply is refused, not overwritten
    Given the metadata audit has recorded "2010-05 corse/IMG_0042.jpg"
    When the file's bytes change and the write is applied
    Then the write is refused because the file changed since it was audited
    And the file is left untouched
