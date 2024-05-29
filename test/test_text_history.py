import unittest
from flask import current_app
from app import create_app, db
from app.models import TextHistory, Text

class TextHistoryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_text_history_creation(self):
        text = Text(content="Hello World", language="English")
        text.save()

        text_history = TextHistory(content="Initial content", text_id=text.id)
        text_history.save()

        self.assertEqual(text_history.content, "Initial content")
        self.assertEqual(text_history.text_id, text.id)

    def test_text_history_add_entry(self):
        text = Text(content="Hello World", language="English")
        text.save()

        text_history = TextHistory(content="Initial content", text_id=text.id)
        text_history.save()

        text_history.add_entry("Updated content")
        self.assertEqual(len(text_history.entries), 1)
        self.assertEqual(text_history.entries[0], "Updated content")

    def test_text_history_view_history(self):
        text = Text(content="Hello World", language="English")
        text.save()

        text_history = TextHistory(content="Initial content", text_id=text.id)
        text_history.save()

        text_history.add_entry("Updated content")
        history = text_history.view_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0], "Updated content")

    def test_text_history_view_versions(self):
        text = Text(content="Hello World", language="English")
        text.save()

        text_history1 = TextHistory(content="Initial content", text_id=text.id)
        text_history1.save()

        text_history2 = TextHistory(content="Updated content", text_id=text.id)
        text_history2.save()

        versions = text_history2.view_versions()
        self.assertEqual(len(versions), 2)
        self.assertIn(text_history1.id, versions)
        self.assertIn(text_history2.id, versions)

    def test_text_history_change_version(self):
        text = Text(content="Hello World", language="English")
        text.save()

        text_history1 = TextHistory(content="Initial content", text_id=text.id)
        text_history1.save()

        text_history2 = TextHistory(content="Updated content", text_id=text.id)
        text_history2.save()

        text_history2.change_version(text_history1.id)
        self.assertEqual(text_history2.content, "Initial content")

if __name__ == '__main__':
    unittest.main()
