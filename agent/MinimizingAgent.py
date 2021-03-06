import random

import numpy as np

from adjudicator.hearts_adjudicator import HeartsAdjudicator
from adjudicator.state import HeartsState
from base import Action, Agent


class HeartsAction(Action):
    """
    A Hearts action is the card index chosen by the agent
    """
    def __init__(self,
                 card_index):
        self.card_index = card_index

    def __str__(self):
        return str(self.card_index)


class MinimizingAgent(Agent):
    """
    An random agent who selects from available legal moves.
    """
    def __init__(self):
        self.own_adj = HeartsAdjudicator()
        self.cards_in_hand = []

    def __str__(self):
        return "The Low Layer"

    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """
        # Given the masked state, only cards in hand of agent is available
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                self.cards_in_hand.append(i)

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            c1 = random.choice(self.cards_in_hand)
            self.cards_in_hand.remove(c1)
            c2 = random.choice(self.cards_in_hand)
            self.cards_in_hand.remove(c2)
            c3 = random.choice(self.cards_in_hand)
            self.cards_in_hand.remove(c3)
            three_cards = [c1, c2, c3]
            return HeartsAction(three_cards)


        # Agent picks a card to play
        # elif partial_state.trick_number > 0 and len(cards_in_hand) > 0:
        else:
            choice = self.select_card(partial_state)
            self.cards_in_hand = []
            return HeartsAction(choice)

    def select_card(self,
                    partial_state: HeartsState):
        # our player is leading, choosing a random card for now
        if self.is_lead(partial_state):
            choice = random.choice(self.cards_in_hand)
        else:
            # we're following, not leading
            if self.not_void(partial_state):
                # Not void in the leading suit
                # pick the lowest card compared to the highest currently played
                choice = self.get_highest_low_card(partial_state)
            else:
                # Void in the leading suit
                # just randomly play for now
                choice = random.choice(self.cards_in_hand)
        return choice

    def is_lead(self,
             partial_state: HeartsState):
        """Returns true if agent is leading currently"""
        played = partial_state.values[partial_state.values > 20]

        if len(played) >= 4:
            return True
        return False

    def not_void(self,
                 partial_state: HeartsState):
        """Returns true if agent is not void in the leading suit"""
        lead_suit = self.own_adj.lead_suit(partial_state)
        begin = 13 * lead_suit  # beginning of range of valid cards
        end = 13 * (lead_suit + 1)  # end of range of valid cards
        for x in self.cards_in_hand:
            if begin <= x < end:
                return True
        return False

    def get_highest_low_card(self,
                             partial_state: HeartsState):
        """Find the cards that are lowest than the card currently set to win and
        choose the highest one"""
        max_card_played = self.own_adj.find_max_card(partial_state)
        max_card_player = -1
        lead_suit = self.own_adj.lead_suit(partial_state)
        begin = 13 * lead_suit  # beginning of range of valid cards
        end = 13 * (lead_suit + 1)  # end of range of valid cards
        for x in self.cards_in_hand:
            if begin <= x < end:
                if max_card_played > x > max_card_player:
                    max_card_player = x

        # TODO might need to do something other than "just play whatever and hope for the best"
        # TODO if we end up with a hand where none of the cards are less than the current max
        if max_card_player == -1:
            max_card_player = self.cards_in_hand[0]
        return max_card_player

    # def get_highest_card_from_played_cards(self,
    #                                        partial_state: HeartsState):
    #     currently_played_cards = np.where(partial_state.values > 20)
    #     lead_suit = self.own_adj.lead_suit(partial_state)
    #     begin = 13 * lead_suit  # beginning of range of valid cards
    #     end = 13 * (lead_suit + 1)  # end of range of valid cards
    #     for x in currently_played_cards:

