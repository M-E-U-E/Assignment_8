import unittest
from trip import settings

class TestSettings(unittest.TestCase):
    def test_settings_values(self):
        """Test that settings values are correctly set."""
        self.assertEqual(settings.BOT_NAME, "trip")
        self.assertEqual(settings.IMAGES_STORE, "city_data/images_of_hotels")
        self.assertIn("trip.pipelines.PostgresPipeline", settings.ITEM_PIPELINES)

if __name__ == "__main__":
    unittest.main()
