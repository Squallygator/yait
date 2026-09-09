Feature: One deduced label is written to title, subject and comment

  No two programs agree on which field is "the caption". The one deduced label
  goes to all three, identically, so it shows up wherever anyone looks and the
  fields never disagree.

  Background:
    Given the collection of "UC-43-one-label-for-title-subject-comment"

  Scenario: The label reads back from all three caption fields
    When the media "2005-08 Rome/le Forum.jpg" has its metadata written
    Then its title, subject and comment all read "Rome - le Forum"
