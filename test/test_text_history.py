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

    def test_add_entry(self):
        text = Text(content="Hello World", language="English")
        text.save()

        history = TextHistory(text_id=text.id, content="Initial Content")
        history.save()
        history.add_entry("First Edit")
        self.assertIn("First Edit", history.entries)

    def test_save(self):
        text = Text(content="Hello World", language="English")
        text.save()
        
        history = TextHistory(text_id=text.id, content="Initial Content")
        saved_history = history.save()
        self.assertEqual(saved_history.content, "Initial Content")

    def test_delete(self):
        text = Text(content="Hello World", language="English")
        text.save()
        
        history = TextHistory(text_id=text.id, content="Initial Content")
        history.save()
        history_id = history.id
        history.delete()
        self.assertIsNone(TextHistory.find(history_id))
        
    def test_view_history(self):
        text = Text(content="Hello World", language="English")
        text.save()

        history = TextHistory(text_id=text.id, content="Initial Content")
        history.add_entry("First Edit")
        history.add_entry("Second Edit")
        self.assertEqual(history.view_history(), ["First Edit", "Second Edit"])

    def test_view_versions(self):
        text = Text(content="Hello World", language="English")
        text.save()
        history1 = TextHistory(text_id=text.id, content="Version 1")
        history1.save()
        history2 = TextHistory(text_id=text.id, content="Version 2")
        history2.save()
        
        versions = TextHistory.view_versions(text.id)
        self.assertEqual(len(versions), 2)
        self.assertIn(versions[0].content, "Version 2")
        self.assertIn(versions[1].content, "Version 1")

    def test_change_version(self):
        text = Text(content="Hello World", language="English")
        text.save()

        history1 = TextHistory(content="Initial content", text_id=text.id)
        history1.save()
        history2 = TextHistory(content="Updated content", text_id=text.id)
        history2.save()
        
        history2.change_version(history1.id)
        self.assertEqual(history2.content, "Initial content")

if __name__ == '__main__':
    unittest.main()