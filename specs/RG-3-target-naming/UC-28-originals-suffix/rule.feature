Feature: A camera master in an "Originals" folder takes an -original suffix

  The out-of-camera JPEG in an Originals sub-folder and its edited twin one
  level up collide once the tree is flattened. The master is marked -original
  so the pair stays readable, instead of one getting a bare _1.

  Background:
    Given the collection of "UC-28-originals-suffix"

  Scenario: The master is suffixed, the edited twin keeps the plain name
    When the media "Bretagne 2011/Originals/coastal path.jpg" is inspected
    Then its target name is "2011-07-02-coastal path-original.jpg"
    When the media "Bretagne 2011/coastal path.jpg" is inspected
    Then its target name is "2011-07-02-coastal path.jpg"
