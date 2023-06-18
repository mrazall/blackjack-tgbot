from random import randint

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
names = [2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king", "ace"]
deck = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    "jack": 10,
    "queen": 10,
    "king": 10,
    "ace": 11,
}
suit = ["clubs", "diamonds", "hearts", "spades"]


def take_cards(hand, hand_show, num_of_cards):
    for i in range(num_of_cards):
        id = names[randint(0, 12)]
        hand.append(deck[id])
        if deck[id] < 10:
            hand_show.append([str(deck[id]), suit[randint(0, 3)]])
        elif deck[id] == 10:
            hand_show.append([str(names[randint(8, 11)]), suit[randint(0, 3)]])
        else:
            hand_show.append([names[12], suit[randint(0, 3)]])


def make_bet(chip, bet):
    if bet <= chip:
        return bet
    else:
        return None


def make_casino_hand(hand_of_casino, hand_of_casino_show):
    while sum(hand_of_casino) < 17:
        take_cards(hand_of_casino, hand_of_casino_show, 1)


def game_sum(hand):
    if 11 not in hand:
        return sum(hand)
    if sum(hand) > 21:
        hand.remove(11)
        hand.append(1)
        return sum(hand)
    else:
        return sum(hand)


def clean(hand_of_player, hand_of_player_show, hand_of_casino, hand_of_casino_show):
    hand_of_player.clear()
    hand_of_player_show.clear()

    hand_of_casino.clear()
    hand_of_casino_show.clear()


def print_deck(hand, k):
    if k == 1:
        print("Ваши карты: ", *hand)
    else:
        print("Карты казино: ", *hand)


def win_and_lose_start(hand_of_player, hand_of_casino, bet):
    # Мгновенный выигрыш

    if sum(hand_of_player) == 21 and sum(hand_of_casino) != 21:
        return 2.5
    elif sum(hand_of_casino) == sum(hand_of_player) and sum(hand_of_casino) == 21:
        return 1


def win_and_lose(hand_of_player, hand_of_casino, choose):
    if game_sum(hand_of_casino) == game_sum(hand_of_player) or (
        game_sum(hand_of_player) > 21 and game_sum(hand_of_casino) > 21
    ):
        return 1
    elif (
        game_sum(hand_of_casino) > game_sum(hand_of_player)
        and game_sum(hand_of_casino) <= 21
    ):
        if choose == 1:
            return -1
        elif choose == 3:
            return 0
    elif (
        game_sum(hand_of_casino) < game_sum(hand_of_player)
        and game_sum(hand_of_casino) <= 21
        and game_sum(hand_of_player) > 21
    ):
        if choose == 1:
            return -1
        elif choose == 3:
            return 0
    elif (
        game_sum(hand_of_casino) < game_sum(hand_of_player)
        and game_sum(hand_of_player) <= 21
        and game_sum(hand_of_player) <= 21
    ):
        if choose == 1:
            return 3
        elif choose == 3:
            return 2
    elif game_sum(hand_of_casino) > 21 and game_sum(hand_of_player) <= 21:
        if choose == 1:
            return 3
        elif choose == 3:
            return 2


chip = 1000


def main_game(
    chip, bet, hand_of_player, hand_of_player_show, hand_of_casino, hand_of_casino_show
):
    take_cards(hand_of_player, hand_of_player_show, 2)
    take_cards(hand_of_casino, hand_of_casino_show, 1)
    if win_and_lose_start(hand_of_player, hand_of_casino, choose, bet, chip):
        clean(hand_of_player, hand_of_player_show, hand_of_casino, hand_of_casino_show)
    choose = 2
    while choose == 2:
        print("1) Удвоить ставку\n2) Взять еще карту\n3) Достаточно")
        choose = int(input())
        print(choose)
        if choose == 2:
            take_cards(hand_of_player, hand_of_player_show, 1)
            print_deck(hand_of_player_show, 1)
    if choose == 1:
        take_cards(hand_of_player, hand_of_player_show, 1)
        make_casino_hand(hand_of_casino, hand_of_casino_show)
        print_deck(hand_of_casino_show, 2)
        print_deck(hand_of_player_show, 1)
    elif choose == 3:
        make_casino_hand(hand_of_casino, hand_of_casino_show)
        print_deck(hand_of_casino_show, 2)
        print_deck(hand_of_player_show, 1)
    win_and_lose(hand_of_player, hand_of_casino, choose, bet, chip)
    clean(hand_of_player, hand_of_player_show, hand_of_casino, hand_of_casino_show)
