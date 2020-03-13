# Shooter Agent
`get_action(partial_state : State) : Action` creates an action with the mindset of trying to shoot for the moon every round.

## Passing
This agent aims to pass along its lower cards to other players so it can more efficiently take tricks.
It especially aims to get rid of the low hearts cards so it does not give points to other players.

## Leading
Early in the game, the agent will attempt to avoid taking tricks because points are less likely to appear.
It uses the low cards so it does not lose points later in the game.
Later in the game, the agent leads with high cards since it is hoping that the other players will give it points.

## Following
Early in the game, the agent will follow with low cards because it wants to get rid of them before points start showing up.
Later in the game, the agent will want to try and take tricks so it will use its higher cards.

## Unique Functions
`select_card(partial_state : HeartsState) : Int` The agent must play a card so it determines if it is leading or following.
When leading, the player plays low cards if it is early in the game and high cards if it is later in the game.
When following, the player plays low cards if it is early in the game and high cards if it is later in the game.

`is_lead(partial_state : HeartsState) : Boolean` Check if the agent is leading or following this trick.
This function will return true when the agent should lead and will return false when the agent is following another player's lead.
To accomplish this, the function will count the cards > 20 in the partial state and determine that this played is leading when the
length is four.
This is because the last state has finished when all four players have played and now the player needs to start the next trick.

`is_early(partial_state : HeartsState) : Boolean` Check if it is early in the game or late in the game. This function determines
that it is early in the game when less than half the deck has been played and it is late in the game when more than half the deck
has been played.

`get_lowest(cards : List) : List` Take a list of cards and find the cards with the lowest value.
In order to find the value, you use mod thirteen because there are thirteen cards in a suit.
If there is more than one card that shares the lowest value, they all get to remain in the list so the player can choose
based on additional information if they want to.

`get_highest(cards : List) : List` Similar to get_lowest(cards) except it finds the cards with the highest value.
It is also capable of returning a list with multiple cards with the same value.

`lowest_high(partial_state : HeartsState, cards: List) : List` Take a list of cards and find the lowest card that is higher than
anything currently played.
If any cards that match that criteria were found, return a list of them.
If no cards were found that match that criteria, return the lowest cards.
This function is useful for when the player is playing at the end of the trick because they know if they can take it and they want
to save their high cards for future tricks.
