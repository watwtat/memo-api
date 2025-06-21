from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "memos.db")}'
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

@app.route('/memo', methods=['POST'])
def create_memo():
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing content field'}), 400
    
    new_memo = Memo(content=data['content'])
    db.session.add(new_memo)
    db.session.commit()
    
    return jsonify(new_memo.to_dict()), 201

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)