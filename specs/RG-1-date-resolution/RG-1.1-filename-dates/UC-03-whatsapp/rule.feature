Feature: WhatsApp media names encode the send date

  WhatsApp removes the original metadata and renames received media to
  IMG-YYYYMMDD-WAnnnn. The calendar date is read from the name; the WAnnnn
  counter is a daily sequence number, not a time.

  Background:
    Given the collection of "UC-03-whatsapp"

  Scenario: The date is read and the WA counter is left out of it
    When the media "WhatsApp/IMG-20161013-WA0001.jpg" is inspected
    Then its resolved date is "2016-10-13"
    And the date comes from "file-name"
    And the date precision is "day"
