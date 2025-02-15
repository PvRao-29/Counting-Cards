from blackjack import set_counting_method, reset, play, count, decks_remaining, calculate_advantage, set_max_adv

sim_iters = 500
sim_num_trials = 10
more_trials = 10
sim_chips = 1000
sim_bet_size = 5

hl_count = {
    'A': -1,
    'K': -1,
    'Q': -1,
    'J': -1,
    '10': -1,
    '9': 0,
    '8': 0,
    '7': 0,
    '6': 1,
    '5': 1,
    '4': 1,
    '3': 1,
    '2': 1
}

set_counting_method(hl_count)
set_max_adv(2)

def basic_test(iterations=sim_iters, initial_chips=sim_chips, base_bet=sim_bet_size):
    history = []
    chips = initial_chips
    for i in range(iterations):
        new_chips = play(chips, base_bet)
        history.append(new_chips)
        chips = new_chips
    return chips

def hl_test(iterations=sim_iters, initial_chips=sim_chips, base_bet=sim_bet_size):
    hl_history = []
    hl_chips = initial_chips
    for _ in range(iterations):
        decks_left = decks_remaining()
        true_count = count / max(decks_left, 0.1)

        if true_count <= 0:
            bet = base_bet
        elif 1 <= true_count < 2:
            bet = base_bet * 2
        elif 2 <= true_count < 3:
            bet = base_bet * 4
        else:
            bet = base_bet * 8
        
        bet = min(bet, hl_chips)
        hl_chips_new = play(hl_chips, bet)
        hl_history.append(hl_chips_new)
        hl_chips = hl_chips_new
    return hl_chips

def compute_overall_edge(num_trials=sim_num_trials, iterations=sim_iters):
    total_edge = 0
    for i in range(num_trials):
        reset()
        basic_out = basic_test(iterations)
        
        reset()
        hl_out = hl_test(iterations)
        
        reset()
        trial_edge = (hl_out - basic_out) / iterations
        total_edge += trial_edge
    average_edge = total_edge / num_trials
    return average_edge * 100

if __name__ == "__main__":
    overarching_edge = 0
    for j in range(1, more_trials + 1):
        overall_edge = 0
        for i in range(1, sim_num_trials + 1):
            reset()
            edge = compute_overall_edge()
            overall_edge += edge
        overall_edge = overall_edge / sim_num_trials
        print(f"Overall edge in Trial {j} was {edge} %")
        overarching_edge += overall_edge
    overarching_edge = overarching_edge / more_trials

    print(f"The average edge across all {more_trials * sim_num_trials} trials ({sim_iters} hands per trial) was {overall_edge} %")
    reset()