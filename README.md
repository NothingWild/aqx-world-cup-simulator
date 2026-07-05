# 🏆 2026 World Cup Monte Carlo Bracket Simulator

An open-source sports analytics web application built for the **AQX Sports Analytics Data Bowl #2**. This tool simulates the remainder of the 2026 World Cup tournament from the Round of 16 onward using dynamic Elo rating differentials.

## 🚀 Features
* **Monte Carlo Engine:** Simulates the entire single-elimination tournament bracket 10,000 times to capture the inherent randomness of knockout football.
* **Mathematical Weighting:** Replaces arbitrary predictions with standard Elo probability formulas to calculate a team's true probability of advancing based on current form and historical strength.
* **Interactive Dashboard:** Built with Streamlit to provide an instantaneous, user-friendly breakdown of championship win probabilities and data visualizations.

## 📊 How it Works
The match outcome probability is calculated using the Elo rating difference:
$$P(\text{Team A}) = \frac{1}{1 + 10^{\frac{\text{Elo B} - \text{Elo A}}{400}}}$$
A random weighted sample then determines the advancing team for each bracket branch, repeating across 10,000 tournament iterations to aggregate final championship probabilities.

## 🛠️ How to Run Locally
1. Clone the repo: `git clone <your-repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
