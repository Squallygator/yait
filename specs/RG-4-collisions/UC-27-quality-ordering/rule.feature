Feature: The higher-quality file keeps the clean name

  When files collide on one name, the un-suffixed name should point at the best
  copy. Ordering leads on pixel resolution, with the source path only as the
  final, deterministic tie-break.

  Background:
    Given the collection of "UC-27-quality-ordering"

  Scenario: Resolution, not path order, decides which copy is suffixed
    When the media "2010-08 fete/b/photo.jpg" is inspected
    Then its target name is "2010-08-15-photo.jpg"
    When the media "2010-08 fete/a/photo.jpg" is inspected
    Then its target name is "2010-08-15-photo_1.jpg"
