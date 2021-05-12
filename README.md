# Newtons-Room
This is my project for MIT course 11.127. Setting up requires python and pygame to be installed.

# Universal Controls
* esc - ends the game (and also crashes it)
* A - go to previous level
* D - skip to next level
* Space - cycles between setup and movement state
## Normal levels
* click - places an arrow (direction is dependant on arrow buttons, magnitude is capped)
* up/down - allows the player to place vertical arrows
* left/right - allows the player to place horizontal arrows
## Trajectory Prediction Levels
* click - places the target at the mouse's location (as long as it is sufficiently far from the player)

## Setup / Move State

Each level begins in the setup state. In this state, arrows are visible, and the player can place arrows (or the goal).

When space is pressed, the arrows disappear, and the player ball can move. If the level is not complete, the player can reset back to the setup state by using the space button again.
