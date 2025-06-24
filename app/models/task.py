from .. import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default = "A fazer")
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref = db.backref('tasks', lazy = True))

    def __repr__(self):
        return f'<Task{self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'user_id': self.user_id
        }