# todo

# integration testing would probably help squash these bugs

# implement game loop with win condition
    # Ensure players have a min of 3 cards when possible
    # Ensure there is a cli interface for this game loop

## Current issues:
- inputs not in index range crashes the game instead of prompting it to continue (or non numbers)
- Playing cards when not allowed causes you to play the card and pickup losing it from your hand
- Doesn't show the opponents board and hand state
- win condition actually pops up for the opponent

# implement special card functionality
# implement swap face cards and hand functionality
# implement reasonable ai behaviour
# implement ability pregame selecition of amount of players
# implement pygame gui