Feature: The label is deduced from the folder and the filename together

  The path already says what a photo is about. The proposed caption joins the
  folder's meaning to the filename's: <folder label> - <filename context>.

  Background:
    Given the collection of "UC-32-label-from-folder-and-context"

  Scenario: Folder and filename combine into one label
    When the media "2004-09 Bretagne/menhir debout.jpg" is inspected
    Then its deduced label is "Bretagne - menhir debout"
