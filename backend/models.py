import os
from sqlalchemy import Column, String, Integer, create_engine,ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "trivia"
database_path = "postgres://{}:{}@{}/{}".format('postgres','pass','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)
    db.create_all()

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'
  id = db.Column(db.Integer, primary_key=True)
  question = db.Column(db.String)
  answer = db.Column(db.String)
  category = db.Column(db.Integer,ForeignKey('categories.id'),nullable=True)
  difficulty = Column(db.Integer)
  rating = Column(db.Integer,nullable=True)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': Category.query.get(self.category).type,
      'difficulty': self.difficulty,
      'rating':self.rating
    }

'''
Category

'''
class Category(db.Model): 

  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String)
  questions = db.relationship("Question",backref="categories",lazy=True)
  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }