from blackjack import reset, decks_remaining, set_counting_method
from agents import counting_agent, play_agent, describer_agent
from langgraph.graph import StateGraph, START, END
import csv

def wrap(agent_fn):
    def wrapped(state):
        out = agent_fn(state)
        state.update(out)
        return state
    return wrapped

def init_agent(state):
    state['decks_remaining'] = decks_remaining()
    return state

basic = {}

hl = {
    '2': +1, '3': +1, '4': +1, '5': +1, '6': +1,
    '7':  0, '8':  0, '9':  0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1,
}

zen = {
    'A': -1,
    'K': -2, 'Q': -2, 'J': -2, '10': -2,
    '9': 0, '8': 0, '7': 0,
    '6': 2, '5': 2, '4': 2,
    '3': 1, '2': 1
}

set_counting_method(zen)

def build_graph():
    g = StateGraph(state_schema=dict)

    g.add_node("init", init_agent)
    g.add_edge(START, "init")

    g.add_node("counting", wrap(counting_agent))
    g.add_edge("init", "counting")

    g.add_node("play", wrap(play_agent))
    g.add_edge("counting", "play")

    g.add_node("update_decks", init_agent)
    g.add_edge("play", "update_decks")

    g.add_node("describe", wrap(describer_agent))
    g.add_edge("update_decks", "describe")

    g.add_edge("describe", END)

    return g.compile()

if __name__ == "__main__":
    NUM_SHOES = 20000
    OUTFILE = 'zen_results_by_shoe.csv'

    #txt:
    # with open(OUTFILE, "w") as f:
    #     f.write("")
    #csv:
    with open(OUTFILE, "w") as f:
        f.write("shoe,hands_played,net_return,avg_return_per_hand\n")

    graph = build_graph()

    for shoe_idx in range(1, NUM_SHOES + 1):
        reset()
        state = {"min_bet": 1}

        while decks_remaining() > 0.5:
            state = graph.invoke(input=state)

        hands = state['hands_played']
        net   = state['net_return']
        avg   = net / hands

        #this is for txt:
        # with open(OUTFILE, "a") as f:
        #     f.write(f"=== TRIAL {trial} ===\n")
        #     f.write(f"Hands played:   {hands}\n")
        #     f.write(f"Net return:     {net:+}\n")
        #     f.write(f"Avg return/h:   {avg:+.4f}\n")
        #     f.write("EV by True Count bucket:\n")
        #     for bucket, data in state["by_count"].items():
        #         avg_bc = data["sum"] / data["n"]
        #         f.write(f"  {bucket}: {avg_bc:+.4f} over {data['n']} hands\n")
        #     f.write("\n")
        
        #if appending to csv use this:
        with open(OUTFILE, "a") as f:
            f.write(f"{shoe_idx},{hands},{net:+},{avg:+.4f}\n")
            
print('sim complete!')