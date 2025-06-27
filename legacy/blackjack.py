import random
import math

deck_of_cards = []
options_list = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
for option in options_list:
    deck_of_cards += [option] * 4

six_decks = deck_of_cards * 6
count = 0

counting_method = {}

def set_counting_method(new_counting_method):
    global counting_method
    counting_method = new_counting_method

def reset():
    global six_decks, count
    six_decks = deck_of_cards * 6
    count = 0

def deal():
    global six_decks, count
    if len(six_decks) < (52 * 0.5):
        six_decks = deck_of_cards * 6
        count = 0
    card = random.choice(six_decks)
    six_decks.remove(card)
    count += counting_method.get(card, 0)
    return card

def decks_remaining():
    return len(six_decks) / 52

def card_value(card):
    if card in ['K', 'Q', 'J', '10']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)
    
def is_soft(hand):
    return 'A' in hand and total(hand) <= 21

def total(cards):
    total_val = 0
    aces = 0
    for card in cards:
        if card == 'A':
            aces += 1
            total_val += 11
        else:
            total_val += card_value(card)
    while total_val > 21 and aces > 0:
        total_val -= 10
        aces -= 1
    return total_val
    
def can_split(hand):
    return len(hand) == 2 and (card_value(hand[0]) == card_value(hand[1]))

def basic_strategy(player_hand, dealer_showing):
    player_total = total(player_hand)
    dealer_val = card_value(dealer_showing)
    soft = is_soft(player_hand)
    pair = can_split(player_hand)

    if pair:
        pair_card = player_hand[0]
        if pair_card == 'A':
            return "Split"
        elif pair_card == '8':
            return "Split"
        elif pair_card in ['9'] and dealer_val not in [7, 10, 11]:
            return "Split"
        elif pair_card in ['7', '2', '3'] and dealer_val < 8:
            return "Split"
        elif pair_card == '6' and dealer_val < 7:
            return "Split"
        elif pair_card == '4' and dealer_val in [5, 6]:
            return "Split"
        elif pair_card in ['5'] and dealer_val < 10:
            return "Double Down"

    if soft:
        if player_total >= 19:
            return "Stand"
        elif player_total == 18:
            if dealer_val >= 9:
                return "Hit"
            else:
                return "Stand"
        else:
            return "Hit"

    else:
        if player_total >= 17:
            return "Stand"
        elif player_total >= 13:
            if dealer_val <= 6:
                return "Stand"
            else:
                return "Hit"
        elif player_total == 12:
            if dealer_val <= 3 or dealer_val >= 7:
                return "Hit"
            else:
                return "Stand"
        elif player_total == 11:
            return "Double Down"
        elif player_total == 10:
            if dealer_val <= 9:
                return "Double Down"
            else:
                return "Hit"
        elif player_total == 9:
            if dealer_val in [3, 4, 5, 6]:
                return "Double Down"
            else:
                return "Hit"
        else:
            return "Hit"

def play(chips, stake):
    if chips <= 0:
        return chips
    
    player_hand = [deal(), deal()]
    dealer_showing = deal()
    dealer_hidden = deal()
    dealer_hand = [dealer_showing, dealer_hidden]
    
    def basic_play(hand, current_stake):
        action = basic_strategy(hand, dealer_showing)
        if action == "Split" and can_split(hand) and len(hand) == 2:
            hand1 = [hand[0], deal()]
            hand2 = [hand[1], deal()]
            return basic_play(hand1, current_stake) + basic_play(hand2, current_stake)
        elif action == "Hit":
            hand.append(deal())
            if total(hand) > 21:
                return [(total(hand), current_stake)]
            return basic_play(hand, current_stake)
        elif action == "Double Down":
            new_stake = current_stake * 2
            hand.append(deal())
            return [(total(hand), new_stake)]
        else:
            return [(total(hand), current_stake)]
    
    player_final_totals = basic_play(player_hand.copy(), stake)
    
    dealer_total_val = total(dealer_hand)
    while dealer_total_val < 17:
        dealer_hand.append(deal())
        dealer_total_val = total(dealer_hand)
        if dealer_total_val > 21:
            break
    
    dealer_final_total = dealer_total_val if dealer_total_val <=21 else -1
    
    def eval_total(result):
        hand_total, hand_stake = result
        if hand_total > 21:
            return -hand_stake
        if dealer_final_total == -1:
            return hand_stake
        if hand_total > dealer_final_total:
            return hand_stake
        elif hand_total < dealer_final_total:
            return -hand_stake
        else:
            return 0
    
    chips += sum(eval_total(result) for result in player_final_totals)
    return max(0, chips)

max_adv = 0.1
def set_max_adv(new_max_adv):
    global max_adv
    max_adv = new_max_adv / 100
    
def calculate_advantage(true_count, max_advantage=max_adv, base_house_edge=-0.005):
    if true_count <= 0:
        advantage = base_house_edge
    else:
        advantage = base_house_edge + (0.005 * true_count)
        advantage = min(advantage, max_advantage)
    
    return advantage