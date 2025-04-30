"""
League-finishing-position simulator – annotated heat-map version
----------------------------------------------------------------
Run this file or import the functions in a notebook.

Author: ChatGPT · April 2025
"""

from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------- #
# 1  Monte-Carlo engine                                                       #
# --------------------------------------------------------------------------- #
def simulate_league(
    teams: list[str],
    ratings: list[float],
    current_points: list[float],
    tournaments: list[dict],
    *,
    sigma: float = 200.0,
    n_sims: int = 50_000,
    random_seed: int | None = None,
) -> pd.DataFrame:
    if random_seed is not None:
        rng = np.random.default_rng(random_seed)
    else:
        rng = np.random.default_rng()

    n = len(teams)
    ratings = np.asarray(ratings,  dtype=float)
    base    = np.asarray(current_points, dtype=float)

    counts = np.zeros((n, n), dtype=np.int32)
    total  = np.empty(n, dtype=float)
    perf   = np.empty(n, dtype=float)
    eps    = 1e-6

    for _ in range(n_sims):
        total[:] = base

        for t in tournaments:
            perf[:]  = ratings + rng.normal(0, sigma, n)
            order    = np.argsort(-perf)                 # best → worst
            pts_dist = t["points"]

            for pos, idx in enumerate(order):
                if pos < len(pts_dist):
                    total[idx] += pts_dist[pos]

        total += rng.uniform(0, eps, n)                  # break ties
        rank = np.argsort(-total)
        for pos, idx in enumerate(rank):
            counts[idx, pos] += 1

    probs = counts / n_sims
    return pd.DataFrame(
        probs,
        index=teams,
        columns=[str(i + 1) for i in range(n)]
    )


# --------------------------------------------------------------------------- #
# 2  Annotated heat-map                                                       #
# --------------------------------------------------------------------------- #
def plot_finish_probs(df: pd.DataFrame, title: str | None = None) -> None:
    n_rows, n_cols = df.shape
    fig, ax = plt.subplots(figsize=(0.65 * n_cols, 0.45 * n_rows))
    im = ax.imshow(df.values, aspect="auto")

    # axis layout
    ax.set_xticks(range(n_cols), df.columns)
    ax.set_yticks(range(n_rows), df.index)
    if title:
        ax.set_title(title)
    ax.set_xlabel("Final position")
    ax.set_ylabel("Team")

    # write probabilities inside every square
    for i in range(n_rows):
        for j in range(n_cols):
            ax.text(
                j,
                i,
                f"{df.iat[i, j] * 100:.1f}",     # e.g. 98.2
                ha="center",
                va="center",
                fontsize=8,
            )

    fig.colorbar(im, label="Probability")
    fig.tight_layout()
    plt.show()


# --------------------------------------------------------------------------- #
# 3  Example usage                                                            #
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # toy data – replace with the real thing
    teams   = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Gogo", "Henry", "Italy", "Jones", "Klondike", "London", "Money", "Never", "Ovni", "Paris"]
    ratings = [1600, 1550, 1500, 1450, 1400, 1350, 1200, 1110, 1100, 1090, 1040, 1020, 1000, 990, 980, 960]        # Elo style
    today = [71, 35, 28, 28, 20, 16, 9,8,5,5,3,2,2,2,1,1]               # current standings

    # three events left in the season
    pts_scheme = [18, 12, 8, 8, 6, 6, 4, 4, 2, 2, 2, 2, 1, 1, 1, 1]                    # customise as needed
    events = [
        {"name": "open4", "points": pts_scheme},
        {"name": "open5", "points": pts_scheme},
        {"name": "open6", "points": pts_scheme},
    ]

    df_probs = simulate_league(
        teams, ratings, today, events,
        sigma=200, n_sims=50_000, random_seed=2025
    )

    print("\nFinishing-position probabilities (fractional form):")
    print(df_probs.round(4))
    print()

    plot_finish_probs(df_probs, "Probability of finishing positions")
