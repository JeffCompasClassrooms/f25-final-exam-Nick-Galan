Feature: Christmas list management

  Scenario: Add item
    Given I have a fresh christmas list file
    When I add "bb gun" to the christmas list
    Then the list should contain an item "bb gun" marked as "not purchased"