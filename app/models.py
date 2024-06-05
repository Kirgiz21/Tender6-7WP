from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Tender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    items = db.relationship('TenderItem', backref='tender', lazy=True, cascade="all, delete-orphan")
    bids = db.relationship('Bid', backref='tender', lazy=True, cascade="all, delete-orphan")
    awards = db.relationship('Award', backref='tender', lazy=True, cascade="all, delete-orphan")


class TenderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    tender_id = db.Column(db.Integer, db.ForeignKey('tender.id', name='fk_tenderitem_tender_id', ondelete='CASCADE'),
                          nullable=False)


class Bidder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact_info = db.Column(db.String(120), nullable=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True, cascade="all, delete-orphan")
    awards = db.relationship('Award', backref='bidder', lazy=True, cascade="all, delete-orphan")


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    terms = db.Column(db.Text, nullable=True)
    tender_id = db.Column(db.Integer, db.ForeignKey('tender.id', name='fk_bid_tender_id', ondelete='CASCADE'),
                          nullable=False)
    bidder_id = db.Column(db.Integer, db.ForeignKey('bidder.id', name='fk_bid_bidder_id', ondelete='CASCADE'),
                          nullable=False)


class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    terms = db.Column(db.Text, nullable=True)
    tender_id = db.Column(db.Integer, db.ForeignKey('tender.id', name='fk_award_tender_id', ondelete='CASCADE'),
                          nullable=False)
    bidder_id = db.Column(db.Integer, db.ForeignKey('bidder.id', name='fk_award_bidder_id', ondelete='CASCADE'),
                          nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    update_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role')
