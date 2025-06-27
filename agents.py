from blackjack import current_count, decks_remaining, play

def counting_agent(state):
    """
    Decide a bet based on true count.
    Requires:
      state["min_bet"]
    Returns:
      {"bet": int}
    """
    decks_left = max(decks_remaining(), 1)
    tc = current_count() / decks_left
    level = max(1, int(tc))
    bet = state["min_bet"] * level
    return {"bet": bet}

def play_agent(state):
    """
    Play one hand and return the P/L.
    Requires:
      state["bet"]
    Returns:
      {"result": int}
    """
    result = play(chips=state["bet"], stake=state["bet"]) - state["bet"]
    return {"result": result}

def describer_agent(state):
    """
    Log the hand and accumulate stats.
    Expects:
      state["bet"], state["result"]
    Updates/inits:
      state["hands_played"], state["net_return"], state["by_count"]
    """
    state.setdefault("hands_played", 0)
    state.setdefault("net_return", 0)
    state.setdefault("by_count", {})

    state["hands_played"] += 1
    state["net_return"] += state["result"]

    decks_left = max(decks_remaining(), 1)
    tc_value = current_count() / decks_left
    tc_bucket = f"true_count_of_{int(round(tc_value))}"

    bucket = state["by_count"].setdefault(tc_bucket, {"sum": 0, "n": 0})
    bucket["sum"] += state["result"]
    bucket["n"] += 1

    print(
        f"[{state['hands_played']:4d}] "
        f"TC={int(round(tc_value)):>2} | "
        f"Bet={state['bet']:3d} | "
        f"P/L={state['result']:+4d}"
    )

    return {}
