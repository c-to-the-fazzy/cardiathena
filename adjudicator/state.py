import numpy as np
from itertools import product
from random import shuffle

# definitions for the card values and suit values in a 52 card deck
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['C', 'D', 'S', 'H']

# constants
player_hand = [1, 2, 3, 4]
player_won = [11, 12, 13, 14]
player_current = [21, 22, 23, 24]
unknown = 0


class State:

    def __init__(self):
        # Probably want to change values to something else to reflect Adjudicator doc (Card deck?)
        self.values = None
        self.score = [0, 0, 0, 0]


class HeartsState(State):
    """

    """

    def __init__(self):
        """
        inits the state and randomly assigns player

        """

        super().__init__()
        self.shuffle()
        # Game Logic
        self.current_player = 1
        self.trick_number = 0
        self.trick_winner = 0
        self.pass_type = 0
        self.cards_of_trick = []
        self.points = [0, 0, 0, 0] #points for a round rather than a game


        #What we are defining as points for the game. Here we have the indices for all the hearts as well as the
        #queen of spade
        self.points_cond = [ 36,39,40,41,42,43,44,45,46,47,48,49,50,51,52]


    def __repr__(self):
        """
        the human readable representation of the state vector

        :return: string
        """
        out = '|'.join([f'{x:>3}' for x in self.card_position.keys()]) + "\n" + '|'.join(
            [f'{x:3}' for x in self.values])

        return out
    """I will change the name lol just thought i would throw a hunter x hunter reference :p
        This function is aim to only allow players play cards from the lead suit(First card played)
        ;param Domain - The Suit that the players must play e.g Heart,Club,Diamond, and Spade
        Steps to make this function to work 
        1. Define the range given the domain
        2. Keep a counter or a way to see how many legal moves there are 
        3. Zero indicates breaking suit 
        4. Set the encoding in the same fashion as hide encoding 
        5.return the new state"""
    def restriction_and_pledge(self,Domain,player):
        #range of domain
        start_index = Domain * 13
        End_index = start_index + 13
        av_moves=0
        print("Func")
        #focus only on the cards that the player has in their hands
        temp = self.hide_encoding(player)
        card_list=np.where(self.values==player)
        #set the cards that are not in the range to zero
        for x in card_list:
            for card in x:
                print(card)
                if((card>=start_index) & (card<=End_index)):
                    av_moves=av_moves+1
                else:
                    temp[card]=0
        #if the card belong to the suit or not
        if(av_moves==0):
            return self.hide_encoding(player)

        return temp

    """ Call this function when the last turn happens to see who won the trick
        This function will work  in the following  matter 
         1. Scan the Heart State 
         2. Keep track  of the states of played cards
         3. Determine the Winner by Ranking of the Cards or the Highest value Cards
         4. Update encoding to a trick won for the lead player and return the player number who won
         Domain must be a number value from 0-3 and represent Clubs,Diamond,Spades,Hearts """
    def trick_lead(self,Domain):

        #Issue defining the winnin trick player memans specifing the domain(Hearts,Diamond,etc)
        #Min amd Max
        start_index = Domain*13
        End_index = start_index+13

        #Scanning and keeping track of the cards played

        p1  = np.where(self.values==21)
        p2  = np.where(self.values==22)
        p3  = np.where(self.values==23)
        p4  = np.where(self.values==24)

        Players_C = [p1[0],p2[0],p3[0],p4[0]]

        Max=0

        #check to see who had the highest card in the rank
        for cards in Players_C:
            #This player must have broke Suit
            if((cards>End_index) | (cards<start_index)):
                continue
            #Some beat the current player with the highest rank
            if(Max<cards):
                Max=cards
        #set the encoding for the state now
        encoding = self.values[Max]-10

        for won_trick in Players_C:
            self.values[won_trick] =encoding

        # Winning player
        return encoding-10

    """ The State tells us everything that we need to know about the score
         This function will simply scan the database and update the point of the player
         USAGE: Once the trick is done 
         1.scan state for won trick cards for each player
         2.update the scoreboard
         3.return the scores """
    def update_scoreboard(self):

        p1=np.where(self.values==11)
        p2=np.where(self.values==12)
        p3=np.where(self.values==13)
        p4=np.where(self.values==14)

        players = [p1[0],p2[0],p3[0],p4[0]]
        cur =0

        for player  in  players:
            for p in player:
                print(p)
                for points in self.points_cond:
                    if(p==points):
                        self.points[cur]+=1
        cur+=1

        print(self.points)

    def shuffle(self):
        players = [1] * 13 + [2] * 13 + [3] * 13 + [4] * 13
        shuffle(players)
        self.values = np.array(players)

    def set_encoding(self, encoding, card):
        """
        encode a value to the state vector

        :param encoding: value to be encoded on the state vector
        :param card: position in the state vector the be encoded
        :return: None
        """
        print(self.values)
        print(self.card_position)
        element = self.card_position[card]
        self.values[element] = encoding

    def get_encoding(self, card):
        """

        :param card: position in the state vector to get value
        :return: encoded value
        """
        element = self.card_position[card]

        return self.values[element]

    def hide_encoding(self, player):
        """
         Mask state vector values replacing hidden information with zeros.

         :param player: the player number 1-4 to receive a tailored masked encoding state vector
         :return: masked encoding np array
         """

        held_cards = self.values == player
        played_cards = self.values > 10
        temp = np.where(held_cards+played_cards, self.values, np.zeros(52, dtype=int))
        #print(temp)
        #currently not differentiating between valid cards and invalid cards so agents are playing any of the cards in their hands

        return temp

    def store_values(self):

        store_value = list(self.values)
        store_value = store_value + self.score
        store_value.append(self.current_player)
        store_value.append(self.trick_number)
        store_value.append(self.trick_winner)
        store_value.append(self.pass_type)
        store_value = store_value + self.points

        return store_value

    def store_strings(self):

        store_string = []
        for i in range(52): #label indices for storage of values
            store_string.append(i)
        for i in range(4): #label numbers of players for storage of score
            store_string.append("Score of " + str(i))
        game_logic = ["Current Player","Trick Number","Trick Winner","Pass Type"]
        for i in range(4):
            game_logic.append("Points of " + str(i))
        store_string = store_string + game_logic

        return store_string
    @property
    def card_position(self):
        """
        builds a python dictionary that lists the element position for each card on the state vector

        :return:
        """

        return {f'{v[1]}{v[0]}': i for i, v in enumerate(product(suits, cards))}

state_test = HeartsState()
state_test.shuffle()

state_test.set_encoding(21,"3H")
state_test.set_encoding(22,"4H")
state_test.set_encoding(23,"7H")
state_test.set_encoding(24,"2C")
print(state_test.values)
state_test.trick_lead(3)
print("Restrictions")
print(state_test.values)
print(state_test.restriction_and_pledge(0,1))
print(state_test)
state_test.update_scoreboard()