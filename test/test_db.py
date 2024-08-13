import unittest
from sqlalchemy import text

from app import create_app, db


class ConnectionTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        ##chat
        #db.engine.execute(text('DROP TABLE IF EXISTS text_histories CASCADE'))
        #db.engine.execute(text('DROP TABLE IF EXISTS texts CASCADE'))
        #chat andando
        """
        with db.engine.connect() as conn:
            conn.execute(text('DROP TABLE IF EXISTS text_histories CASCADE'))
            conn.execute(text('DROP TABLE IF EXISTS texts CASCADE'))
        """
        self.app_context.pop()
            
    # test connection to db
    def test_db_connection(self):
        #chat andando
        
        with db.engine.connect() as conn:
            # Use a valid SQL query or expression
            result = conn.execute(text('SELECT 1')).scalar()
            self.assertEqual(result, 1)
        #chat
        #result = db.session.execute(text("'Hello world'")).scalar()
        #self.assertEqual(result, 'Hello world')
        #profe
        #result = db.session.query(text("'Hello world'")).one()
        #self.assertEqual(result[0], 'Hello world')
    
if __name__ == '__main__':
    unittest.main()
