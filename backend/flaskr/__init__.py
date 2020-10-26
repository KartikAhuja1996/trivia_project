import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category,db

from helpers import paginate

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app,resources={'/':{'origins':'*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
        response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,True")
        response.headers.add("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS")
        return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route("/categories",methods=['GET'])
  def get_categories():
        categories = Category.query.all()
        return jsonify({
          "success":True,
          "categories":[c.format() for c in categories],
          "categories_count":len(categories)
        })



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''




  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
        error = False
        question = Question.query.get(question_id)
        if(question is not None):
          try:
            question.delete()
          except:
            error= True
            db.session.rollback()
          finally:
            db.session.close()
          
        return jsonify({
          "success":True,
          "question_id":question_id
        })



  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route("/questions",methods=['POST'])
  def add_question():
    data = request.get_json()
    question = data.get('question',None)
    answer = data.get('answer',None)
    category_id = data.get('category',None)
    difficulty = data.get('difficulty',None)
    if((question is None) and (answer is None) and (category_id is None) and (difficulty is None)):    
      return abort(400)
    q = Question(question=question,answer=answer,category=category_id,difficulty=difficulty)
    q.insert()
    return jsonify({
      'success':True,
      "question":q.format()
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 


  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''


  
  @app.route("/questions/search",methods = ['POST'])
  def search_question():
    data = request.get_json()
    search_keyword = data.get("keyword",None).lower()
    if(search_keyword is None):
      return abort(422)
    questions = Question.query.filter(Question.question.ilike("%{}%".format(search_keyword))).all()
    return jsonify({
      "success":True,
      "questions_count":len(questions),
      "questions":[q.format() for q in questions]
    })
      



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route("/categories/<int:category_id>/questions")
  def handle_category_questions(category_id):
        category = Category.query.get(category_id)
        if(category is None):
              return abort(404)
        questions = category.questions
        return jsonify({
          'success':True,
          'questions':[question.format() for question in questions],
          'total_questions':len(questions),
          'current_category':Category.query.get(category_id).format()
        })

  

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route("/quizzes",methods=['POST'])
  def get_random_question():
    data = request.get_json()
    print(data)
    questions = []
    questions_len = 0
    quiz_category = data.get('quiz_category')
    prevQuestions = data.get('previous_questions')
    print(prevQuestions)

    if((quiz_category is None) or (prevQuestions is None)):
      return abort(400)
    if(data.get('quiz_category') == 0):
      questions = Question.query.all()
    else:
      questions = Question.query.filter(Question.category == quiz_category).all()
    questions_len = len(questions)

    def get_random_question():
      return questions[random.randrange(0,len(questions),1)]


    def check_if_already_asked(question):
      asked = False
      for q in prevQuestions:
        if q == question.id:
          asked = True
      return asked

    question = get_random_question()

    while(check_if_already_asked(question)):
      question = get_random_question()

      if(len(prevQuestions) == questions_len):
        return jsonify({
          'success':True
        })
            

    return jsonify({
      'success':True,
      'question':question.format()
    })
    



              

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found_error_handler(self):
      return jsonify({
        "status_code":404,
        "success":False,
        "message":"Resource Not Found"
      }),404


  @app.errorhandler(400)
  def bad_request_error_handler(self):
        return jsonify({
          "success":False,
          "message":"Bad Request",
          "error":400
        }),400
  
  @app.errorhandler(422)
  def unprocessable_error_handler(self):
        return jsonify({
          "success":False,
          "error":422,
          "message":"unprocessable"
        })

  app.register_error_handler(404,not_found_error_handler)
  app.register_error_handler(400,bad_request_error_handler)
  app.register_error_handler(422,unprocessable_error_handler)



  @app.route("/questions")
  def index():
        selection = Question.query.order_by(Question.id.desc()).all()
        questions = paginate(request,selection)
        categories = Category.query.all()
        print([category.format() for category in categories])
        return jsonify({
          "data":True,
          "success":True,
          "total_questions":len(selection),
          "categories":[category.format() for category in categories],
          "questions":[q.format() for q in questions]
        })

  @app.route("/questions/<int:question_id>",methods=['POST','GET'])
  def questions(question_id):
        if(request.method == 'GET'):
          question = Question.query.filter(Question.id == question_id).first()
          if(question is None):
                return abort(404)
          return jsonify({
            'success':True,
            'question':question.format()
          })
        elif(request.method == 'POST'):    
          data = request.get_json()
          question = Question.query.filter(Question.id == question_id).first()
          if 'question' in data:
              question.question = data['question']
          if 'answer' in data:
                question.answer = data['answer']
          try:
            question.update()
          except:
            db.session.rollback()
          finally:
            db.session.close()
          return jsonify({
            "success":True
          })



  

  

  
  return app

    