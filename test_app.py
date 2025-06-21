import unittest
import json
from app import app, db, Memo


class MemoAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_empty_memos(self):
        response = self.app.get('/memo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_create_memo(self):
        memo_data = {'content': 'Test memo'}
        response = self.app.post('/memo', 
                                data=json.dumps(memo_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['content'], 'Test memo')
        self.assertEqual(data['id'], 1)
        self.assertIn('created_at', data)

    def test_get_memos_after_creation(self):
        memo_data = {'content': 'Test memo'}
        self.app.post('/memo', 
                     data=json.dumps(memo_data),
                     content_type='application/json')
        
        response = self.app.get('/memo')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['content'], 'Test memo')

    def test_create_memo_missing_content(self):
        response = self.app.post('/memo', 
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Missing content field')

    def test_create_memo_no_json(self):
        response = self.app.post('/memo')
        self.assertEqual(response.status_code, 415)

    def test_multiple_memos_id_increment(self):
        memo1 = {'content': 'First memo'}
        memo2 = {'content': 'Second memo'}
        
        response1 = self.app.post('/memo', 
                                 data=json.dumps(memo1),
                                 content_type='application/json')
        response2 = self.app.post('/memo', 
                                 data=json.dumps(memo2),
                                 content_type='application/json')
        
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        
        self.assertEqual(data1['id'], 1)
        self.assertEqual(data2['id'], 2)

    def test_delete_existing_memo(self):
        memo_data = {'content': 'Test memo to delete'}
        create_response = self.app.post('/memo', 
                                       data=json.dumps(memo_data),
                                       content_type='application/json')
        created_memo = json.loads(create_response.data)
        memo_id = created_memo['id']
        
        delete_response = self.app.delete(f'/memo/{memo_id}')
        self.assertEqual(delete_response.status_code, 200)
        
        delete_data = json.loads(delete_response.data)
        self.assertEqual(delete_data['message'], f'Memo {memo_id} deleted successfully')
        
        get_response = self.app.get('/memo')
        memos = json.loads(get_response.data)
        self.assertEqual(len(memos), 0)

    def test_delete_nonexistent_memo(self):
        response = self.app.delete('/memo/999')
        self.assertEqual(response.status_code, 404)

    def test_delete_memo_from_multiple(self):
        memo1 = {'content': 'First memo'}
        memo2 = {'content': 'Second memo'}
        memo3 = {'content': 'Third memo'}
        
        response1 = self.app.post('/memo', data=json.dumps(memo1), content_type='application/json')
        response2 = self.app.post('/memo', data=json.dumps(memo2), content_type='application/json')
        response3 = self.app.post('/memo', data=json.dumps(memo3), content_type='application/json')
        
        memo2_id = json.loads(response2.data)['id']
        
        delete_response = self.app.delete(f'/memo/{memo2_id}')
        self.assertEqual(delete_response.status_code, 200)
        
        get_response = self.app.get('/memo')
        remaining_memos = json.loads(get_response.data)
        self.assertEqual(len(remaining_memos), 2)
        
        remaining_contents = [memo['content'] for memo in remaining_memos]
        self.assertIn('First memo', remaining_contents)
        self.assertIn('Third memo', remaining_contents)
        self.assertNotIn('Second memo', remaining_contents)


if __name__ == '__main__':
    unittest.main()