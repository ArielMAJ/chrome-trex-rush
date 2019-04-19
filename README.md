# T-Rex Rush 

![trex game screenshot](https://github.com/shivamshekhar/Chrome-T-Rex-Rush/raw/master/screenshot.png)

![trex game gif](https://github.com/shivamshekhar/Chrome-T-Rex-Rush/raw/master/screenshot.gif)

## Description

A recreated version of the famous Chrome T-Rex in Python.

## Technology

Built using pygame library

## Version and Release

First Release, version 1.0

## Target Platforms

Windows/Linux

## Instructions and Prerequisites

To run this game:  

* Make sure you have Python installed alongwith pygame (<http://www.pygame.org/>) library
* Install the `chrome_trex` package:

    ```bash
    git clone https://github.com/fernandokm/chrome-trex-rush
    cd chrome-trex-rush
    pip install .
    ```

* Use the package:

    ```python
    from chrome_trex import DinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN

    # Create a new game that runs with at most 'fps' frames per second.
    # Use fps=0 for unlimited fps.
    game = DinoGame(fps)

    # Go to the next frame and take the action 'action'
    # (ACTION_UP, ACTION_FORWARD or ACTION_DOWN).
    game.step(action)

    # Get a list of floats representing the game state
    # (positions of the obstacles and game speed).
    game.get_state()

    # Get the game score.
    game.get_score()

    # Reset the game.
    game.reset()

    # Close the game.
    game.close()
    ```

## Developers

Initially developed by: Shivam Shekhar (shivam.shekhar.ece14@itbhu.ac.in)

Adapted by:

* Badr Youbi Idrissi (badryoubiidrissi@gmail.com)
* Fernando Matsumoto (ferkmatsumoto@gmail.com)

## Credits

* Sprites : <https://chromedino.com/assets/offline-sprite-2x-black.png>
* Logo : <https://textcraft.net/>
* Speech Bubble : <http://pixelspeechbubble.com/>
* Sounds : <https://github.com/vicboma1/T-Rex-Game/tree/master/Unity/Sounds>
