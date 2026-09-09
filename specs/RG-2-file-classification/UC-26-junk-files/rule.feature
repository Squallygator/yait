Feature: Photo-manager and operating-system leftovers are junk

  Thumbs.db, Picasa.ini, desktop.ini and their kind are recognised by name and
  set aside, so they stop inflating every count and every screen.

  Background:
    Given the collection of "UC-26-junk-files"

  Scenario: A Picasa.ini is classified as junk by its name alone
    When the media "junk/Picasa.ini" is inspected
    Then it is classified as "junk"
