import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','pass','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test get categories endpoint api 
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        categories = Category.query.all();
        self.assertEqual(data['success'],True)
        self.assertEqual(data['categories_count'],len(categories))

    

    # Test question endpoint api when question is available
    def test_get_question(self):
        res = self.client().get("/questions/3")
        question = Question.query.get(3)
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['question']['question'],question.question)
        self.assertEqual(data['question']['answer'],question.answer)

    # Test question endpoint api when question is not available
    def test_get_question_not_found(self):
        res = self.client().get("/questions/2")
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['status_code'])
        self.assertEqual(data['status_code'],404)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'],"Resource Not Found")

    def test_delete_question(self):
        question_id=1
        q = Question(question="Which is the tallest mountain in the world?",answer="Mount Everest",category=1,difficulty=1,rating=1)
        q.insert()
        res = self.client().delete("/questions/{}".format(question_id))
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['question_id'],question_id)
        q.delete()

    def test_add_question(self):
        res = self.client().post("/questions",json={'question':'What is your name?','answer':'kartik','category':1,'difficulty':5,'rating':2})
        data = json.loads(res.data)
        actual_data = Question.query.order_by(Question.id.desc()).all()[0]
        self.assertEqual(data['success'],True)
        self.assertEqual(data['question_id'],actual_data.id)
        Question.query.get(actual_data.id).delete()

    # test the search questions endpoint api 
    def test_search_questions(self):
        search_keyword = "which"
        res = self.client().post("/questions",json={"keyword":search_keyword})
        data = json.loads(res.data)
        actual_questions = Question.query.filter(Question.question.ilike("%{}%".format(search_keyword))).all()
        actual_questions_count = len(actual_questions)
        self.assertEqual(data['questions_count'],actual_questions_count)
        self.assertEqual(data['questions'],[q.format() for q in actual_questions])
    
    # test the search questions endpoint if question not found
    def test_search_questions_not_found(self):
        search_keyword = "gell"
        res = self.client().post("/questions/search",json={'keyword':search_keyword})
        data = json.loads(res.data)
        self.assertEqual(data['status_code'],404)
        self.assertEqual(data['success'],False)    
        self.assertEqual(data['message'],"Resource Not Found")
    

    # test to check all the questions in the category
    def test_get_questions_in_category(self):
        category_id = 1
        api_endpoint = "/categories/{}/questions".format(category_id)
        res = self.client().post(api_endpoint)
        actual_res_data = Question.query.filter(Question.category == category_id).all()
        actual_current_category = Category.query.get(category_id)
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'],len(actual_current_category.questions))
        self.assertEqual(data['current_category'],actual_current_category.format())
        for i in range(0,len(data['questions'])):
            self.assertEqual(data['questions'][i]['question'],actual_res_data[i].question)
            self.assertEqual(data['questions'][i]['answer'],actual_res_data[i].answer)
            self.assertEqual(data['questions'][i]['category'],Category.query.get(actual_res_data[i].category).format()['type'])
            self.assertEqual(data['questions'][i]['difficulty'],actual_res_data[i].difficulty)
            self.assertEqual(data['questions'][i],actual_res_data[i].format())


    # testing get quiz question without any previous questions
    def test_quiz_question_without_previous_questions(self):
        res = self.client().post("/quizzes",json={'quiz_category':1,'previous_questions':[]})
        data = json.loads(res.data)
        self.assertIsNotNone(data['question'])
        actual_data = Question.query.get(data['question']['id'])
        self.assertEqual(data['success'],True)
        self.assertEqual(data['question']['category'],Category.query.get(actual_data.category).type)
        self.assertEqual(data['question']['question'],actual_data.question)
        self.assertEqual(data['question']['answer'],actual_data.answer)

    # testing get quiz question api with all the previous questions already present in the previous_questions key
    def test_quiz_question_with_all_previous_questions_in_query(self):
        res = self.client().post('/quizzes',json={'quiz_category':0,'previous_questions':[3,8,9,10,11,12,13,14,15]})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
    


    # Test 404 error Resource Not Found
    def test_404_error(self):
        res = self.client().get("/random/url/notfound")
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status_code'],404)
        self.assertEqual(data['message'],'Resource Not Found')

    # Test 400 error Bad Request 
    def test_400_error(self):
        res = self.client().post('/questions',json={'name':'kartik'})
        data = json.loads(res.data)
        self.assertEqual(data['status_code'],400)
        self.assertEqual(data['message'],'Bad Request')
        self.assertEqual(data['success'],False)
    

    # test 422 error unprocessable
    def test_422_error(self):
        res = self.client().post("/categories",json={
            'type':'history'
        })
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status_code'],422)
        self.assertEqual(data['message'],"Unprocessable")


    # test 500 internal server error
    def test_500_error(self):
        res = self.client().post("/errors/500")   
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['status_code'],500)
        self.assertEqual(data['message'],"Internal Server Error")  
    
    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()