import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

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
        self.assertEqual(data['success'],True)
        self.assertEqual(data['categories_count'],1)


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
        q = Question(question="Which is the tallest mountain in the world?",answer="Mount Everest",category=1,difficulty=1)
        q.insert()
        res = self.client().delete("/questions/{}".format(question_id))
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['question_id'],question_id)
        q.delete()

    def test_add_question(self):
        pass

    # test the search question endpoint api 
    def test_search_question(self):
        search_keyword = "which"
        res = self.client().post("/questions/search",json={"keyword":search_keyword})
        data = json.loads(res.data)
        actual_questions = Question.query.filter(Question.question.ilike("%{}%".format(search_keyword))).all()
        actual_questions_count = len(actual_questions)
        self.assertEqual(data['questions_count'],actual_questions_count)
        self.assertEqual(data['questions'],[q.format() for q in actual_questions])


    # test to check all the questions in the category
    def test_get_questions_in_category(self):
        category_id = 1
        res = self.client().get("/categories/{}/questions".format(category_id))
        actual_res_data = Question.query.filter(Question.category == category_id).all()
        actual_current_category = Category.query.get(category_id)
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'],9)
        self.assertEqual(data['current_category'],actual_current_category.format())
        for i in range(0,len(data['questions'])):
            self.assertEqual(data['questions'][i]['question'],actual_res_data[i].question)
            self.assertEqual(data['questions'][i]['answer'],actual_res_data[i].answer)
            self.assertEqual(data['questions'][i]['category'],actual_res_data[i].category)
            self.assertEqual(data['questions'][i]['difficulty'],actual_res_data[i].difficulty)
            self.assertEqual(data['questions'][i],actual_res_data[i].format())

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()