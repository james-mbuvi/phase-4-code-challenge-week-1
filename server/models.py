from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Define the relationship to HeroPower
    hero_power = db.relationship('HeroPower', backref='hero', lazy=True)
    
    serialize_rules = ('-hero_power.hero',)
    
    def __repr__(self):
        return f'<Hero {self.id}: {self.super_name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Define the relationship to HeroPower
    hero_power = db.relationship('HeroPower', backref='power', lazy=True)
    
    serialize_rules = ('-hero_power.power',)
    
    @validates('description')
    def validate_description(self, key, body):
        if len(body) < 20:
            raise ValueError('description must be at least 20 characters')
        return body
    
    def __repr__(self):
        return f'<Power {self.id}: {self.name}; {self.description}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    serialize_rules = ('-hero.hero_power', '-power.hero_power',)
    
    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError('Invalid strength')
        return value
    
    def __repr__(self):
        return f'<Hero-Power {self.id}: {self.strength} {self.hero_id} {self.power_id}>'
