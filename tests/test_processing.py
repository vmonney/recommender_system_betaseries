import unittest

import pandas as pd

from src.betaseries_recommender.processing import (
    calculate_weighted_average,
    process_data,
)


class TestProcessing(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"title": "Movie A", "total_notes": 1000, "mean_notes": 4.5},
            {"title": "Movie B", "total_notes": 100, "mean_notes": 4.8},
            {"title": "Movie C", "total_notes": 500, "mean_notes": 3.0},
        ]
        self.df = pd.DataFrame(self.data)

    def test_calculate_weighted_average_basic(self):
        # With threshold_count=3, m will be min of top 3 -> 100 (Movie B)
        # C = mean of (4.5, 4.8, 3.0) = 4.1
        # m = 100
        # Movie A: v=1000, R=4.5. WA = (4.5*1000 + 4.1*100)/(1000+100) = (4500+410)/1100 = 4.4636
        df = calculate_weighted_average(self.df.copy(), threshold_count=3)

        movie_a = df[df["title"] == "Movie A"].iloc[0]
        self.assertAlmostEqual(movie_a["weighted_average"], 4.4636, places=3)

    def test_sorting(self):
        # Default sort is weighted_average
        df = process_data(
            self.df.copy(), sort_by="mean_notes", limit=3, threshold_count=3
        )
        assert df.iloc[0]["title"] == "Movie B"  # Highest mean 4.8

        df = process_data(
            self.df.copy(), sort_by="total_notes", limit=3, threshold_count=3
        )
        assert df.iloc[0]["title"] == "Movie A"  # Highest total 1000

    def test_limit(self):
        df = process_data(self.df.copy(), limit=1, threshold_count=3)
        assert len(df) == 1

    def test_threshold_logic(self):
        # If threshold_count is 1, m should be total_notes of the 1st most popular
        # Top 1 is Movie A (1000). So m=1000.
        df = calculate_weighted_average(self.df.copy(), threshold_count=1)
        # Logic for m:
        # v = df["total_notes"]
        # m = df.nlargest(1, "total_notes").iloc[-1]["total_notes"] -> 1000

        # Verify m was effectively 1000 for calculation
        # Movie A: v=1000, m=1000. WA = (4.5*1000 + 4.1*1000)/2000 = (8.6)/2 = 4.3

        movie_a = df[df["title"] == "Movie A"].iloc[0]
        self.assertAlmostEqual(movie_a["weighted_average"], 4.3, places=2)


if __name__ == "__main__":
    unittest.main()
