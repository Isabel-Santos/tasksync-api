from ..extensions import db
from datetime import datetime

class TaskShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    permission = db.Column(db.String(10), nullable=False, default='view')  # 'view' ou 'edit'
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)  # ⬅️ Adicione isso

    task = db.relationship('Task', backref=db.backref('shared_with', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('shared_tasks', lazy='dynamic'))

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "permission": self.permission,
            "shared_at": self.shared_at.isoformat(),
        }
