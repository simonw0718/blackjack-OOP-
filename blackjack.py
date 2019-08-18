import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}     
playing = True

#先將所有元素分析出來, 有玩家/莊家, 有卡片, 有牌堆deck, 有手牌 hand, 有籌碼

#定義出Card object
class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
      
    def __str__(self):
        return f'{self.rank} of {self.suit}'
#開始定義牌堆
class Deck: 
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank)) #在這裡給(rank,suit) Card的object
                 
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__() #這裡利用Card的method來print內容
        return 'desk have' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        deal_card = self.deck.pop()
        return deal_card    
#開始定義手牌的樣子 (可以加牌,算數字, 根據value修改ace)
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces: #self.aces存在 = True
            self.value -= 10
            self.aces -= 1
#定義籌碼的樣子
class Chips: 
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet 
    
    def lose_bet(self):
        self.total -= self.bet
#下注
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('plz input integer value for your bet: '))
        except:
            print('plz inpur inreger value')
            continue
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break
#加牌
def hit(deck,hand):   
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
#決定是否繼續
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break
#顯示牌面
# player and dealer should be hand
def show_some(player,dealer):
    # print(*objects, sep=' ', end='\n', file=sys.stdout) 這是print語法, 可以修改默認的sep 跟end 
    print("<dealer's hand>:")
    print(' <<card hidden>>')
    print(' ', dealer.cards[1]) 
    print("<player's hand>:", *player.cards, sep = '\n ')#sep='\n '可以拿來分割
    #*可以用來show全部items


def show_all(player,dealer):
    
    print("\n<dealer's hand>:", *dealer.cards, sep = '\n')
    print("\ndealer's total value:", dealer.value, sep = '\n')
    print("\n<player's hand>:", *player.cards, sep = '\n')
    print("\nplayer's total value:", player.value, sep = '\n')
#終盤狀況
def player_busts(player,dealer,chips):
    print('player bust!')
    chips.lose_bet()
def player_wins(player,dealer,chips):
    print('player win!')
    chips.win_bet()
def dealer_busts(player,dealer,chips):
    print('dealer bust!')
    chips.win_bet()
def dealer_wins(player,dealer,chips):
    print('dealer win!')
    chips.lose_bet()   
def push():
    print("it's a tied, push!")

while True:
    # Print an opening statement
    print('welcome to blackjack!')
    
    # Create & shuffle the deck, deal two cards to each player
    play_deck = Deck()
    play_deck.shuffle()

    player = Hand() #建立手牌
    player.add_card(play_deck.deal())
    player.add_card(play_deck.deal())
    dealer = Hand() #建立手牌
    dealer.add_card(play_deck.deal())
    dealer.add_card(play_deck.deal())
    
        
    # Set up the Player's chips
    try:
        print(f'you know have {chips.total}')
    except:
        chips = Chips()

    
    # Prompt the Player for their bet
    take_bet(chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)
    
    while playing:  # recall this variable from our hit_or_stand function
    
        # Prompt for Player to Hit or Stand
        bust_check = False
        hit_or_stand(play_deck, player)
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player, dealer, chips)
            playing = True
            bust_check = True #確認是否player已經炸掉
            break
        continue

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    while bust_check == False:
        hit(play_deck, dealer)
        if dealer.value >17:
            break
         
    
        # Run different winning scenarios
    if bust_check == False:
        show_all(player, dealer) # Show all cards
        if dealer.value > 21:
            dealer_busts(player,dealer,chips)
        elif dealer.value > player.value:
            print('dealer win!')
            dealer_wins(player,dealer,chips)

        elif dealer.value < player.value:
            player_wins(player,dealer,chips)
        elif dealer.value == player.value:
            push()  

    
    # Inform Player of their chips total 
    print(f'you remain {chips.total} chips')
    
    # Ask to play again
    play_check = input('you wanna play again or not? (y/n) ?')
    if play_check.lower() == 'y':
        playing = True
        continue
    else:
        print('bye!')
        break


