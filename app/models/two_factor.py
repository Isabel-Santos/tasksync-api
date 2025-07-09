# models/two_factor.py
from ..extensions import db
from datetime import datetime, timedelta

class TwoFactorCode(db.Model):
    __tablename__ = 'two_factor_codes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))
