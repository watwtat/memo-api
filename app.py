from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

data_dir = os.environ.get('DATA_DIR', os.path.abspath(os.path.dirname(__file__)))
os.makedirs(data_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(data_dir, "memos.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

@app.route('/memo', methods=['GET'])
def get_memos():
    memos = Memo.query.all()
    return jsonify([memo.to_dict() for memo in memos])

@app.route('/memo/<int:memo_id>', methods=['GET'])
def get_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    return jsonify(memo.to_dict())

@app.route('/memo/<int:memo_id>', methods=['PUT'])
def update_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing content field'}), 400
    
    memo.content = data['content']
    db.session.commit()
    
    return jsonify(memo.to_dict())

@app.route('/memo', methods=['POST'])
def create_memo():
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing content field'}), 400
    
    new_memo = Memo(content=data['content'])
    db.session.add(new_memo)
    db.session.commit()
    
    return jsonify(new_memo.to_dict()), 201

@app.route('/memo/<int:memo_id>', methods=['DELETE'])
def delete_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    db.session.delete(memo)
    db.session.commit()
    
    return jsonify({'message': f'Memo {memo_id} deleted successfully'}), 200

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)