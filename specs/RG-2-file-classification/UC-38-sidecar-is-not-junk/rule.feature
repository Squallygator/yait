Feature: A .THM sidecar survives as long as its video does

  A camcorder wrote a tiny thumbnail beside every clip. It looks like a stray
  file, but it carries the video's only date on old AVIs, so the cleanup must
  not bin it while its video is still there.

  Background:
    Given the collection of "UC-38-sidecar-is-not-junk"

  Scenario: A .THM whose video is present is classified as a sidecar, not junk
    When the media "CANON/MVI_3312.THM" is inspected
    Then it is classified as "sidecar"
