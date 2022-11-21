'''
Blackjack game
'''


import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
        'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
        'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

PLAYING = True


class Card:
    '''
    Card object
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    '''
    Here we might store 52 card objects in a list that can later be shuffled.
    '''

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                new_card = Card(suit, rank)
                self.deck.append(new_card)

    def __str__(self):
        print("Start of the deck:")
        for card in self.deck:
            print(card)
        return "End of the deck."

    def shuffle(self):
        """Shuffle the cards in the deck
        """
        random.shuffle(self.deck)

    def deal(self):
        '''
        Deal out cards
        '''
        return self.deck.pop()


class Hand:
    """The Hand class may be used to calculate the value of those cards using the values dictionary
    defined above. It may also need to adjust for the value of Aces when appropriate.
    """

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        """Adding cards to the Hand and calculating the value.
        """
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        """Adjusting Ace values
        """
        if self.value > 21 and self.aces > 0:
            self.value -= 10 * self.aces
            self.aces = 0


class Chips:
    """Player's starting chips, bets, and ongoing winnings.
    """

    def __init__(self, total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        """Total chips after winning.
        """
        self.total += self.bet * 2

    def lose_bet(self):
        """Total chips after losing.
        """
        self.total -= self.bet


class InputNegative(Exception):
    """Raised when the input value is negativve"""


def take_bet(player_chip):
    """Taking the bets from the player by asking.
    """

    while True:
        try:
            player_chip.bet = int(input("Place your bet: "))
            if player_chip.bet <= player_chip.total and player_chip.bet >= 0:
                break
            elif player_chip.bet < 0:
                raise InputNegative
            else:
                raise Exception
        except ValueError:
            print("Please bet with integer numbers!")
        except InputNegative:
            print("Please bet with non negative numbers!")
        except Exception:
            print("Please bet less than or equal to your total chips.")


def hit(deck, hand):
    """This function will be called during gameplay anytime a Player requests a hit, or a
    Dealer's hand is less than 17. It should take in Deck and Hand objects as arguments,
    and deal one card off the deck and add it to the Hand.

    Args:
        deck (Deck)
        hand (Hand)
    """
    new_card = deck.deal()
    hand.add_card(new_card)


class InputNotBoolean(Exception):
    """Raised when the input value is not True or False"""


def hit_or_stand(deck, hand):
    """This function should accept the deck and the player's hand as arguments, and assign
    playing as a global variable. If the Player Hits, employ the hit() function above.
    If the Player Stands, set the playing variable to False.
    """
    global PLAYING  # to control an upcoming while loop

    while True:
        try:
            hit_or_not = input(
                "To hit please type 'True', to stand please type 'False':\n")
            if hit_or_not in ["True", "False"]:
                break
            raise InputNotBoolean
        except InputNotBoolean:
            print("Please type 'True' for hit or 'False' to stand")

    if hit_or_not == "True":
        hit(deck, hand)
    else:
        PLAYING = False


def show_some(player, dealer):
    """hen the game starts, and after each time Player takes a card, the dealer's first card is
    hidden and all of Player's cards are visible.

    Args:
        player (Hand)
        dealer (Hand)
    """
    print("Player's cards: ")
    print(" | ", end='')
    for card in player.cards:
        print(card, end=' | ')
    print("")
    print("Dealer's cards: ")
    print(" | ", end='')
    first_card = True
    for card in dealer.cards:
        if first_card:
            print("HIDDEN CARD", end=' | ')
            first_card = False
        else:
            print(card, end=' | ')
    print("")


def show_all(player, dealer):
    """At the end of the hand all cards are shown, and you may want to show each hand's total value.

    Args:
        player (Hand)
        dealer (Hand)
    """
    print("Player's cards: ")
    print(" | ", end='')
    for card in player.cards:
        print(card, end=' | ')
    print("Player's total value is: " + str(player.value))
    print("Dealer's cards: ")
    print(" | ", end='')
    for card in dealer.cards:
        print(card, end=' | ')
    print("Dealer's total value is: " + str(dealer.value))


def player_busts(player):
    """Player busts if value is over 21.

    Args:
        player (Hand)

    Returns:
        boolean
    """
    return player.value > 21


def dealer_wins(dealer):
    """Dealer wins if value is under 21.

    Args:
        dealer (Hand)

    Returns:
        boolean
    """
    return dealer.value < 21


def replay():
    """Asking for replay.

    Raises:
        InputNotBoolean

    Returns:
        string 'Yes' or 'No'
    """
    while True:
        try:
            play_again = input(
                "Do you want to play again? Please type 'Yes' or 'No':\n")
            play_again.capitalize()
            if play_again in ["Yes", "No"]:
                break
            raise Exception
        except Exception:
            print("Please type 'Yes' or 'No'")
    return play_again


print("Welcome to the Serhat's casino!")
print("You are going to play blackjack!")
GAME_PLAY = 1
while True:
    # Print an opening statement
    print("Enjoy!!!")
    # Create & shuffle the deck, deal two cards to each player
    new_deck = Deck()
    new_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(new_deck.deal())
    player_hand.add_card(new_deck.deal())
    dealer_hand.add_card(new_deck.deal())
    dealer_hand.add_card(new_deck.deal())
    # Set up the Player's chips
    if GAME_PLAY == 1:
        player_chip = Chips()
    # Prompt the Player for their bet
    print(f"Your total chips: {player_chip.total}")
    take_bet(player_chip)
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while PLAYING:  # recall this variable from our hit_or_stand function
        # Prompt for Player to Hit or Stand
        hit_or_stand(new_deck, player_hand)
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_busts(player_hand):
            player_hand.adjust_for_ace()
            if player_busts(player_hand):
                print("Player is busted. The bet is lost.")
                print("All cards:")
                show_all(player_hand, dealer_hand)
                player_chip.lose_bet()
                break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if not player_busts(player_hand):
        DEALER_HIT = 0
        while dealer_hand.value < 17:
            hit(new_deck, dealer_hand)
            DEALER_HIT += 1
        if DEALER_HIT > 0:
            print(
                f"Dealer finished hitting. In total, the dealer hit {DEALER_HIT} times.")
            print("All cards:")
        else:
            print("Dealer cannot hit because its cards already reach the value limit 17.")
            print("All cards:")
        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if (dealer_hand.value > player_hand.value) and dealer_wins(dealer_hand):
            print("Dealer won the game. You lost the bet.")
            player_chip.lose_bet()
        else:
            print(
                f"You won the game!\nIn total, you won {player_chip.bet * 2}")
            player_chip.win_bet()

    # Inform Player of their chips total
    print(f"Your total chips: {player_chip.total}")

    # Ask to play again
    if replay() == 'No':
        print("Thank you for playing, see you!")
        break
    if player_chip.total == 0:
        GAME_PLAY = 1
    else:
        GAME_PLAY += 1
    PLAYING = True
