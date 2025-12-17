def best_hand_value(hand):
    """
    Return (best_total, is_soft)
    best_total = the highest total <= 21 if possible, otherwise the smallest total > 21.
    is_soft = True if the returned best_total counts an Ace as 11.
    """
    total = sum(hand)
    aces = hand.count(1)
    # try to convert 0 or 1 ace to 11 (or more, but only one 11 is useful usually)
    best = total
    is_soft = False
    for use_aces_as_11 in range(aces + 1):
        t = total + use_aces_as_11 * 10  # each ace promoted adds +10 (1 -> 11)
        # we only consider promotions that don't make more than aces
        if use_aces_as_11 <= aces:
            # pick highest <=21 if possible
            if t <= 21 and t > best:
                best = t
                is_soft = (use_aces_as_11 > 0)
            elif best > 21 and t < best:
                # if everything busts, pick smallest bust total
                best = t
                is_soft = (use_aces_as_11 > 0)
    return best, is_soft

def simulate_dealer(dealer_hand, deck, hit_on_soft17=True):
    total, soft = best_hand_value(dealer_hand)

    if total > 17 or (total == 17 and (not soft or not hit_on_soft17)):
        # base case: dealer stands here. Return distribution mass 1 on this total.
        return {total: 1.0}
    
    outcomes = {}
    n = len(deck)
    if n == 0:
        # no cards left — should not happen in practice on a single deck if inputs valid,
        # but handle gracefully: treat current total as final.
        return {total: 1.0}
    else:
        for i in range(n):
            new_card = deck[i]
            new_hand = dealer_hand.copy() + [new_card]
            new_deck = deck[:i] + deck[(i+1):]
            sub = simulate_dealer(new_hand, new_deck, hit_on_soft17=hit_on_soft17)
            for t, p in sub.items():
                outcomes[t] = outcomes.get(t, 0) + p / n
        return outcomes

def main():
    remaining = []
    for i in range(10):
        count = 16 if i + 1 == 10 else 4
        remaining.extend([i + 1] * count)

    my_hand = []
    dealers_hand = [int(input("What is the dealer's card? "))]

    print('Input card numbers, type "x" to end')
    while True:
        card = input(f'Card {len(my_hand)+1}: ')
        if card.lower() == "x":
            break
        else:
            my_hand.append(int(card))

    for card in my_hand + dealers_hand:
        remaining.remove(card)

    my_total, _ = best_hand_value(my_hand)

    if my_total > 21:
        print("You busted! Loss probability: 100%")
        return
    lose = 0
    tie = 0
    win = 0

    for i in range(len(remaining)):
        new_card = remaining[i]
        new_hand = dealers_hand.copy() + [new_card]
        new_deck = remaining[:i] + remaining[(i+1):]

        outcomes = simulate_dealer(new_hand, new_deck)

        for total, prob in outcomes.items():
            if total > 21:
                win += prob
            elif total > my_total:
                lose += prob
            elif total == my_total:
                tie += prob
            else:
                win += prob

    print(win, tie, lose)
    print("win:", win/(win + tie + lose) * 100)
    print("tie:", tie/(win + tie + lose) * 100)
    print("lose:", lose/(win + tie + lose) * 100)

if __name__ == "__main__":
    main()