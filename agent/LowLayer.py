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


class LowLayer(Agent):
    """
    An random agent who selects from available legal moves.
    """

    def __init__(self):
        self.own_adj = HeartsAdjudicator()
        self.cards_in_hand = []

    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """
        # Given the masked state, only cards in hand of agent is available
        # for i in range(len(partial_state.values)):
        #     if 0 < partial_state.values[i] < 5:
        #         self.cards_in_hand.append(i)

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            # c1 = random.choice(self.cards_in_hand)
            # self.cards_in_hand.remove(c1)
            # c2 = random.choice(self.cards_in_hand)
            # self.cards_in_hand.remove(c2)
            # c3 = random.choice(self.cards_in_hand)
            # self.cards_in_hand.remove(c3)
            # three_cards = [c1, c2, c3]
            three_cards = self.passing_smart_sequence(partial_state)
            # for remove in three_cards:
            #     self.cards_in_hand.remove(remove)
            return HeartsAction(three_cards)

        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                self.cards_in_hand.append(i)

        # Agent picks a card to play
        # elif partial_state.trick_number > 0 and len(cards_in_hand) > 0:
        else:
            choice = self.select_card(partial_state)
            # print("minimizing agent is leading: " + str(self.is_lead(partial_state)))
            # print("minimizing agent is not void: " + str(self.not_void(partial_state)))
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
                choice = self.sloughing(partial_state)
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

    def sort_suits(self,
                   partial_state: HeartsState):
        cards = []
        clubs = []
        Diamond = []
        spades = []
        hearts = []
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                cards.append(i)

            """ Sort out the Cards by Suit """
            # Clubs - Diamond - Spades - Hearts
        for i in range(4):
            start = i * 13
            end = start + 13
            for card in cards:
                # print("I : "+str(i)+"  Card "+str(card))
                if i == 0:
                    # print("Club Enter")
                    if start <= card < end:
                        clubs.append(card)
                        #   print("Club Added")
                elif i == 1:
                    # print("Diamond Enter")
                    if start <= card < end:
                        Diamond.append(card)
                    #  print("Diamond Added")
                elif i == 2:
                    # print("Spade Enter")
                    if start <= card < end:
                        spades.append(card)
                        #    print("Spade Added")
                elif i == 3:
                    #  print("Hearts Enter")
                    if start <= card < end:
                        hearts.append(card)
                        #   print("Hearts Added")

        suits = [clubs, Diamond, spades, hearts]
        return suits

    def passing_smart_sequence(self, partial_state: HeartsState):
        cards_to_pass = []  # List of the cards that the agent will pass
        passing_amount = 3  # Amount of Cards that will be pass

        suits = self.sort_suits(partial_state)
        num_cards = -1
        counter = 0

        for card in range(3):
            choose_one, suits = self.pick_trouble_card(suits);
            for c in choose_one:
                cards_to_pass.append(c)
            if (len(cards_to_pass) > 3):
                break;

        return cards_to_pass[0:3]

    def pick_trouble_card(self, sorted_hands):

        """Choose the suit with the least amount of cards
            and pass those starting with the highest card unimplemented so far """
        trouble = []
        index = -1
        store_pos = 0
        num_cards = -1
        cards_to_pass = []
        for suit in sorted_hands:
            index += 1
            if len(suit) > num_cards:
                num_cards = len(suit)
                trouble = suit
                store_pos = index

        for i in range(len(trouble)):
            cards_to_pass.append(trouble[i * -1])

        lost_card = sorted_hands
        lost_card[store_pos] = trouble

        return cards_to_pass, lost_card

    def average_suit_weight(self, Suit_list):
        sum = 0
        for cards in Suit_list:
            sum += (cards % 13) + 1
        if sum == 0:
            return 0
        return sum / len(Suit_list)

    def sloughing(self,
                  partial_state: HeartsState):
        suit_to_slough = self.bad_suit()
        begin = 13 * suit_to_slough
        end = 13 * (suit_to_slough + 1)
        max_card = -1
        for cards in self.cards_in_hand:
            if begin <= cards < end and cards > max_card:
                max_card = cards
        if max_card == -1:
            max_card = self.cards_in_hand[0]
        return max_card

    def bad_suit(self):
        suit_avg = [0, 0, 0, 0]
        counter = 0
        # count up the number of problem cards per suit
        # whichever suit has more problem cards is the one we're going to slough from
        for x in range(4):
            begin = 13 * x
            end = 13 * (x + 1)
            for cards in range(begin, end):
                if cards in self.cards_in_hand:
                    suit_avg[x] += cards % 13
                    counter += 1
            if counter != 0:
                suit_avg[x] = suit_avg[x] / counter
            counter = 0

        bad_suit_index = 0
        for suit_index in range(len(suit_avg)):
            if suit_avg[suit_index] > suit_avg[bad_suit_index]:
                bad_suit_index = suit_index

        return bad_suit_index

    # def get_highest_card_from_played_cards(self,
    #                                        partial_state: HeartsState):
    #     currently_played_cards = np.where(partial_state.values > 20)
    #     lead_suit = self.own_adj.lead_suit(partial_state)
    #     begin = 13 * lead_suit  # beginning of range of valid cards
    #     end = 13 * (lead_suit + 1)  # end of range of valid cards
    #     for x in currently_played_cards:
