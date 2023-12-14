from enum import Enum
import random
from tqdm import tqdm

suit = ['spade', 'heart', 'diamond', 'club']

class SwapFirstCard(Enum):
    NEVER = 1
    ALWAYS = 2
    OPTIMAL = 3


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank  # Apparently the value of the card is called rank...

    def show(self):
        if self.rank == 1:
            print(f'Ace of {self.suit}')
        elif self.rank == 11:
            print(f'Jack of {self.suit}')
        elif self.rank == 12:
            print(f'Queen of {self.suit}')
        elif self.rank == 13:
            print(f'King of {self.suit}')
        else:
            print(f'{self.rank} of {self.suit}')

    def compare(self, other):
        if self.rank > other.rank:
            return 1
        elif self.rank < other.rank:
            return -1
        else:
            return 0

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in suit:
            for r in range(1, 14):
                self.cards.append(Card(s, r))

    def draw(self):
        return self.cards.pop()

    def shuffle(self):
        # Fisher-Yates shuffle
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def shouldGoHigher(self, card):
        higherCardsInDeck = sum(1 for c in self.cards if c.rank > card.rank)
        lowerCardsInDeck = sum(1 for c in self.cards if c.rank < card.rank)
        return higherCardsInDeck > lowerCardsInDeck

    def pickCardWithRank(self, rank):
        for i in range(len(self.cards)):
            if self.cards[i].rank == rank:
                return self.cards.pop(i)
        return None

class Game:
    def __init__(self, deck, rounds = 12, verbose = False, swapFirstCard = SwapFirstCard.NEVER, forceFirstRank = None):
        self.deck = deck
        self.deck.shuffle()
        self.rounds = rounds
        self.verbose = verbose
        self.swapFirstCard = swapFirstCard
        self.forceFirstRank = forceFirstRank

    def play(self):
        card = None
        if self.forceFirstRank is None:
            card = self.deck.draw()
        else:
            card = self.deck.pickCardWithRank(self.forceFirstRank)

        if self.verbose:
            card.show()

        shouldSwap = card.rank > 3 and card.rank < 11
        if self.swapFirstCard == SwapFirstCard.ALWAYS or (self.swapFirstCard == SwapFirstCard.OPTIMAL and shouldSwap):
            card = self.deck.draw()
            if self.verbose:
                print("Discarded first card")
                card.show()


        for i in range(self.rounds):
            guess = self.deck.shouldGoHigher(card)
            nextCard = self.deck.draw()
            if self.verbose:
                print(f'Round {i + 1} of {self.rounds}')
                print('Will the next card be higher or lower?')
                print("Higher" if guess else "Lower")
                nextCard.show()

            if guess == True and nextCard.rank > card.rank:
                if self.verbose:
                    print('Correct!')
            elif guess == False and nextCard.rank < card.rank:
                if self.verbose:
                    print('Correct!')
            else:
                if self.verbose:
                    print('Incorrect!')
                return False

            card = nextCard
            if self.verbose:
                print("--------------------")

        if self.verbose:
            print("Winner winner chicken dinner!")
        return True

def testFirstCardSwap(tries=10**6):
    for rank in tqdm(range(1, 14)):
        for j in range(2):
            wins = 0
            for i in tqdm(range(tries)):
                deck = Deck()
                deck.shuffle()
                game = Game(deck, verbose=False, swapFirstCard=SwapFirstCard.ALWAYS if j==1 else SwapFirstCard.NEVER, forceFirstRank=rank)
                win = game.play()
                if win:
                    wins += 1

            print(f"Configuration {rank}, {j}: Won {wins} out of {tries} games")



if __name__ == '__main__':
    tries = 10**9
    swapFirstCard = SwapFirstCard.OPTIMAL
    # testFirstCardSwap()

    wins = 0
    for i in tqdm(range(tries)):
        deck = Deck()
        deck.shuffle()
        game = Game(deck, verbose=False, swapFirstCard=swapFirstCard)
        win = game.play()
        if win:
            wins += 1
        if i % 10**5 == 0:
            print(f"Won {wins} out of {i} games")

    print(f"Won {wins} out of {tries} games")
