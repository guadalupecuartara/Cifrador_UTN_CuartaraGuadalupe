import unittest
from flask import current_app
from app import create_app, db
from app.models import TextHistory, Text
from sqlalchemy import text 

class TextHistoryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
         # Crea un texto de prueba
        self.text = Text(content="Initial Content",language="English")
        self.text.save()
        db.session.add(self.text)
        db.session.commit()

    def test_add_entry(self):
         # Crear una instancia de TextHistory
        history = TextHistory(text_id=self.text.id, content="Initial Content")
        
        # Agregar la entrada
        history.add_entry("First Edit")
        
        # Guardar los cambios
        history.save()
        
        # Volver a consultar el historial desde la base de datos
        reloaded_history = TextHistory.query.get(history.id)
        
        # Verificar que la entrada está en el historial
        self.assertIn("First Edit", reloaded_history.view_history())
       
    def test_save(self):
        history = TextHistory(text_id=self.text.id, content="Initial Content")
        saved_history = history.save()
        self.assertEqual(saved_history.content, "Initial Content")

    def test_delete(self):
        history = TextHistory(text_id=self.text.id, content="Initial Content")
        history.save()
        history_id = history.id
        history.delete()
        self.assertIsNone(TextHistory.find(history_id))
        
    def test_view_history(self):
        history = TextHistory(text_id=self.text.id, content="Initial Content")
        history.add_entry("First Edit")
        history.add_entry("Second Edit")
        self.assertEqual(history.view_history(), ["First Edit", "Second Edit"])

    def test_view_versions(self):
        history1 = TextHistory(text_id=self.text.id, content="Version 1")
        history1.save()
        history2 = TextHistory(text_id=self.text.id, content="Version 2")
        history2.save()
        
        versions = TextHistory.view_versions(self.text.id)
        self.assertEqual(len(versions), 2)
        self.assertIn("Version 2", [v.content for v in versions])
        self.assertIn("Version 1", [v.content for v in versions])

    def test_change_version(self):
        history1 = TextHistory(content="Initial content", text_id=self.text.id)
        history1.save()
        history2 = TextHistory(content="Updated content", text_id=self.text.id)
        history2.save()
        
        history2.change_version(history1.id)
        self.assertEqual(history2.content, "Initial content")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
if __name__ == '__main__':
    unittest.main()
