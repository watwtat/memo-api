import unittest
import json
from app import app, memos


class MemoAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        memos.clear()

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


if __name__ == '__main__':
    unittest.main()