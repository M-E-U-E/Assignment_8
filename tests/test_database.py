import unittest
from trip.db.database import engine, init_db, SessionLocal

class TestDatabase(unittest.TestCase):
    def test_engine_creation(self):
        """Test database engine creation."""
        self.assertIsNotNone(engine)

    def test_init_db(self):
        """Test initializing database (metadata creation)."""
        try:
            init_db()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"init_db failed with exception: {e}")

    def test_session_creation(self):
        """Test creating a database session."""
        try:
            session = SessionLocal()
            session.close()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"SessionLocal failed with exception: {e}")

if __name__ == "__main__":
    unittest.main()
