import os
from flask import Flask, request, abort, jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category,db

from helpers import paginate

from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = {'svg','png','jpeg','jpg'}


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS






def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  setup_db(app)
  
  # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  
  CORS(app,resources={'/':{'origins':'*'}})

  # Access-Allow-Control set up
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,True")
    response.headers.add("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS")
    return response

  
  # Get all the available categories
  @app.route("/categories",methods=['GET','POST'])
  def get_categories():
    if(request.method =='GET'):
      categories = Category.query.all()
      return jsonify({
        "success":True,
        "categories":[c.format() for c in categories],
        "categories_count":len(categories)
      })
    if(request.method == 'POST'):
      category_type = request.form.get('type')
      if('icon' not in request.files):
        abort(422)
      icon = request.files['icon']
      if icon.filename == '':
        abort(400)
      if icon and allowed_file(icon.filename) and category_type is not None:
        iconname = secure_filename(icon.filename)
        category = Category(type=category_type,icon=iconname)
        category.insert()
        icon.save(os.path.join(app.config['UPLOAD_FOLDER']+"/icons",iconname))
        return jsonify({
          'success':True,
          'message':'Added Successfully',
          'category':category.format()
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
    search_term = data.get('keyword',None)
    if search_term is not None:
      questions = Question.query.filter(Question.question.ilike("%{}%".format(search_term.lower()))).all()
      if(len(questions) == 0):
        return abort(404)
      return jsonify({
        "success":True,
        "questions_count":len(questions),
        "questions":[q.format() for q in questions]
      })
    question = data.get('question',None)
    answer = data.get('answer',None)
    category_id = data.get('category',None)
    difficulty = data.get('difficulty',None)
    rating = data.get('rating',None)
    if((question is None) and (answer is None) and (category_id is None) and (difficulty is None) and (rating is None)):    
      return abort(400)
    if(question == '' or answer == '' or category_id == 0 or difficulty == 0 or rating == 0):
      return abort(400)
    q = Question(question=question,answer=answer,category=category_id,difficulty=difficulty,rating=rating)
    q.insert()
    return jsonify({
      'success':True,
      "question_id":q.id
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


  
  # @app.route("/questions/search",methods = ['POST'])
  # def search_question():
  #   data = request.get_json()
  #   search_keyword = data.get("keyword",None)
  #   if(search_keyword is None):
  #     return abort(400)
  #   questions = Question.query.filter(Question.question.ilike("%{}%".format(search_keyword.lower()))).all()
  #   if(len(questions) == 0):
  #     return abort(404)
  #   return jsonify({
  #     "success":True,
  #     "questions_count":len(questions),
  #     "questions":[q.format() for q in questions]
  #   })
      



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route("/categories/<int:category_id>/questions",methods=['POST'])
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

    if(len(prevQuestions) == questions_len):
          return jsonify({
        'success':True
      })
    else:
      while(check_if_already_asked(question)):
        question = get_random_question()
    
           

    return jsonify({
      'success':True,
      'question':question.format()
    })

  # get the question by the id or update the question based on the request data
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


  @app.route("/uploads/<file_name>",methods=['GET'])
  def uploaded_file(file_name):
    print(file_name)
    return send_from_directory(app.config['UPLOAD_FOLDER']+"/icons/",file_name)



  # dummy url for validate the error 500 test
  @app.route("/errors/500",methods=['POST'])
  def error_500_endpoint():
    return abort(500)    


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  # error handler for 404 not found error
  @app.errorhandler(404)
  def not_found_error_handler(self):
    return jsonify({
      "status_code":404,
      "success":False,
      "message":"Resource Not Found"
    }),404


  # error handler for bad request error
  @app.errorhandler(400)
  def bad_request_error_handler(self):
    return jsonify({
      "success":False,
      "message":"Bad Request",
      "status_code":400
    }),400
  
  # error handler for unprocessable error
  @app.errorhandler(422)
  def unprocessable_error_handler(self):
    return jsonify({
      "success":False,
      "status_code":422,
      "message":"Unprocessable"
    })

  # error handler for internal server error
  @app.errorhandler(500)
  def internal_server_error_handler(self):
    return jsonify({
      "success":False,
      "status_code":500,
      "message":"Internal Server Error"
    })

  app.register_error_handler(500,internal_server_error_handler)
  app.register_error_handler(404,not_found_error_handler)
  app.register_error_handler(400,bad_request_error_handler)
  app.register_error_handler(422,unprocessable_error_handler)



  



  

  

  
  return app

    