import unittest

from recommender import build_recommendations


class RecommendationPipelineTests(unittest.TestCase):
    def test_build_recommendations_ranks_candidates_without_network_calls(self):
        seed = {
            "id": 1,
            "title": "The Matrix",
            "genres": [{"id": 28, "name": "Action"}, {"id": 878, "name": "Sci-Fi"}],
            "release_date": "1999-03-31",
            "vote_average": 8.7,
            "keywords": [{"id": 10, "name": "computer"}, {"id": 11, "name": "future"}],
            "mood": {
                "valence": 0.2,
                "arousal": 0.6,
                "complexity": 0.1,
                "weight": 0.2,
                "pace": 0.4,
            },
            "mood_bins": {
                "valence": "neutral",
                "arousal": "moderate",
                "complexity": "simple",
                "weight": "light",
                "pace": "moderate",
            },
        }

        candidate = {
            "id": 2,
            "title": "Blade Runner",
            "genres": [{"id": 878, "name": "Sci-Fi"}, {"id": 53, "name": "Thriller"}],
            "release_date": "1982-06-25",
            "vote_average": 8.1,
            "keywords": [{"id": 11, "name": "future"}, {"id": 12, "name": "android"}],
            "mood": {
                "valence": 0.1,
                "arousal": 0.5,
                "complexity": 0.0,
                "weight": 0.3,
                "pace": 0.3,
            },
            "mood_bins": {
                "valence": "neutral",
                "arousal": "moderate",
                "complexity": "simple",
                "weight": "light",
                "pace": "slow",
            },
        }

        credits_by_id = {
            1: {
                "crew": [{"name": "Lana Wachowski", "job": "Director"}],
                "cast": [{"name": "Keanu Reeves"}, {"name": "Laurence Fishburne"}],
            },
            2: {
                "crew": [{"name": "Ridley Scott", "job": "Director"}],
                "cast": [{"name": "Harrison Ford"}, {"name": "Rutger Hauer"}],
            },
        }

        results = build_recommendations(
            seed,
            [candidate],
            credits_by_id=credits_by_id,
            mood_context={"company": "alone"},
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["position"], 0)
        self.assertGreater(results[0]["score"], 0)
        self.assertIn("score", results[0])
        self.assertEqual(results[0]["mood_context"], {"company": "alone"})
        self.assertIn("Strong match", results[0]["reason"])


if __name__ == "__main__":
    unittest.main()
