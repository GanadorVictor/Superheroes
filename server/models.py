# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    super_name = Column(String, nullable=False)
    hero_powers = relationship('HeroPower', backref='hero', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Hero {self.name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    hero_powers = relationship('HeroPower', backref='power', cascade="all, delete-orphan")

    @validates('description')
    def validate_description(self, key, description):
        assert len(description) >= 20, "Description must be at least 20 characters long"
        return description

    def __repr__(self):
        return f'<Power {self.name}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = Column(Integer, primary_key=True)
    strength = Column(String, nullable=False)
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = Column(Integer, ForeignKey('powers.id'), nullable=False)
    hero = relationship('Hero', backref=backref('hero_powers', cascade="all, delete-orphan"))
    power = relationship('Power', backref=backref('hero_powers', cascade="all, delete-orphan"))

    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength in ['Strong', 'Weak', 'Average'], "Strength must be 'Strong', 'Weak', or 'Average'"
        return strength

    def __repr__(self):
        return f'<HeroPower {self.strength}>'
