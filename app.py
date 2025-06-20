from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

memos = []

@app.route('/memo', methods=['GET'])
def get_memos():
    return jsonify(memos)

@app.route('/memo', methods=['POST'])
def create_memo():
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing content field'}), 400
    
    new_memo = {
        'id': len(memos) + 1,
        'content': data['content'],
        'created_at': datetime.now().isoformat()
    }
    
    memos.append(new_memo)
    
    return jsonify(new_memo), 201

if __name__ == '__main__':
    app.run(debug=True)