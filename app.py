import streamlit as st
import random
import pandas as pd

# 1. Exact Remaining Round of 16 Matchups
r16_matches = [
    {"id": "R16_1", "team1": "Canada", "team2": "Morocco"},
    {"id": "R16_2", "team1": "Paraguay", "team2": "France"},
    {"id": "R16_3", "team1": "Brazil", "team2": "Norway"},
    {"id": "R16_4", "team1": "Mexico", "team2": "England"},
    {"id": "R16_5", "team1": "Portugal", "team2": "Spain"},
    {"id": "R16_6", "team1": "United States", "team2": "Belgium"},
    {"id": "R16_7", "team1": "Argentina", "team2": "Egypt"},
    {"id": "R16_8", "team1": "Switzerland", "team2": "Colombia"}
]


def simulate_match(team1, team2):
    """
    Placeholder simulator. Right now it's a coin flip (50/50).
    """
    return random.choice([team1, team2])

def run_single_tournament():
    """Simulates the remaining bracket exactly once and tracks how far teams go."""
    # Dict to keep track of the highest round reached by each team in this run
    results = {}
    
    # --- ROUND OF 16 ---
    r16_winners = []
    for match in r16_matches:
        winner = simulate_match(match["team1"], match["team2"])
        r16_winners.append(winner)
        results[winner] = "Quarterfinals"
        
    # --- QUARTERFINALS ---
    # According to the tournament structure: Winner 1 plays Winner 2, Winner 3 plays Winner 4, etc.
    qf_winners = []
    qf_winners.append(simulate_match(r16_winners[0], r16_winners[1])) # QF 1
    qf_winners.append(simulate_match(r16_winners[2], r16_winners[3])) # QF 2
    qf_winners.append(simulate_match(r16_winners[4], r16_winners[5])) # QF 3
    qf_winners.append(simulate_match(r16_winners[6], r16_winners[7])) # QF 4
    
    for winner in qf_winners:
        results[winner] = "Semifinals"
        
    # --- SEMIFINALS ---
    sf_winners = []
    sf_winners.append(simulate_match(qf_winners[0], qf_winners[1])) # SF 1
    sf_winners.append(simulate_match(qf_winners[2], qf_winners[3])) # SF 2
    
    for winner in sf_winners:
        results[winner] = "Finalist"
        
    # --- THE FINAL ---
    champion = simulate_match(sf_winners[0], sf_winners[1])
    results[champion] = "Champion"
    
    return results


# Baseline Elo ratings for the remaining Round of 16 teams
# Higher score = stronger team
team_elo = {
    "France": 2110,
    "Brazil": 2040,
    "Spain": 2025,
    "Argentina": 2015,
    "England": 1980,
    "Portugal": 1960,
    "Colombia": 1910,
    "Belgium": 1880,
    "Netherlands": 1870,
    "Mexico": 1840,
    "United States": 1815,
    "Morocco": 1810,
    "Switzerland": 1795,
    "Norway": 1780,
    "Paraguay": 1740,
    "Egypt": 1725,
    "Canada": 1720
}


def simulate_match(team1, team2):
    """
    Calculates win probability using the Elo rating difference,
    then simulates a winner based on those weighted probabilities.
    """
    elo1 = team_elo.get(team1, 1500) # Default to 1500 if team not found
    elo2 = team_elo.get(team2, 1500)
    
    # Standard Elo expected score formula
    prob_team1_wins = 1 / (1 + 10 ** ((elo2 - elo1) / 400))
    
    # Use a random float between 0 and 1 to pick the winner based on the weight
    if random.random() < prob_team1_wins:
        return team1
    else:
        return team2



st.title("🏆 2026 World Cup Bracket Simulator")
st.write("This app runs 10,000 Monte Carlo simulations of the remaining World Cup bracket based on live team Elo ratings.")

# Add an interactive button to trigger the simulation
if st.button("Run Simulation Engine"):
    with st.spinner("Simulating 10,000 tournaments..."):
        # Run 10,000 Monte Carlo Simulations
        N_SIMULATIONS = 10000
        championship_counts = {}
        
        for _ in range(N_SIMULATIONS):
            tournament_outcome = run_single_tournament()
            # Find who won this iteration
            for team, round_reached in tournament_outcome.items():
                if round_reached == "Champion":
                    championship_counts[team] = championship_counts.get(team, 0) + 1
        
        # Convert results into a clean percentage DataFrame
        df_probabilities = pd.DataFrame(list(championship_counts.items()), columns=["Team", "Championships Won"])
        df_probabilities["Win Probability (%)"] = (df_probabilities["Championships Won"] / N_SIMULATIONS) * 100
        df_probabilities = df_probabilities.sort_values(by="Win Probability (%)", ascending=False).reset_index(drop=True)
        
        df_probabilities
        
        st.success("Simulation Complete!")
        
        # Display the table beautifully
        st.dataframe(df_probabilities.style.format({"Win Probability (%)": "{:.2f}%"}))
        
        # Display a bar chart instantly
        st.bar_chart(data=df_probabilities, x="Team", y="Win Probability (%)")