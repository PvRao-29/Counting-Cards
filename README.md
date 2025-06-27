# Blackjack Simulation

I updated this recently just as a way to practice making agentic frameworks. I used langgraph and made a playing, a counting, and a describing agent to compartmentalize the work I was previously doing. It was quite fun and in the process I also updated my logic to be more sound.

## A quick update on my findings:

 - This will be brief as I have notebooks pushed to the main branch with all the cool graphs and meaningful numbers
 - HiLo actually has been beating zen
    - I have no idea why, but its cool to see
 - I will work on reducing variance (maybe run some pseudorandom testing?)

As always thanks for reading! For any inquiries reach me at pranshu_rao@berkeley.edu


# Original Version:

A Python simulation comparing the Zen Count card counting strategy to basic strategy in Blackjack. This project demonstrates the effectiveness of the Zen Count system in gaining an edge over the casino.

I have now also added the HiLo counting strategy. Will sophisticate the simulations over time... for now the hl_v_zen simulation is not where I want it to be.

## A quick rundown on what the data has shown me so far:

 - Zen beats basic by around 2.3% on average when doing 1000 trials with 5000 iterations (hands) played each

 - HiLo does aroud 1.9 - 2.1%

 - However my data shows heads up, HiLo outperforms Zen. I am not sure why this is, but I will try and find out!
