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
        self.database_name = 'trivia_test'
        self.database_user = 'postgres'
        self.database_password = 'postgres'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.database_user, self.database_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
        'question':  'Heres a new question string',
        'answer':  'Heres a new answer string',
        'difficulty': 1,
        'category': 3,
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        """Test _________________"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories']) # Test if there is a total number of books in the response
    
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertFalse(data["currentCategory"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000", json={"rating": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    # def test_get_questions_by_category(self):
    #     res = self.client().patch("/categories/1/questions", json={"rating": 1})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)

    
    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"])
        self.assertTrue(len(data["questions"]))

    def test_404_get_requesting_beyond_valid_category(self):
        res = self.client().get("/categories/100000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_question(self):
    #     res = self.client().delete("/questions/6")
    #     data = json.loads(res.data)

    #     book = Question.query.filter(Question.id == 6).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 6)
    #     self.assertTrue(data["totalQuestions"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertEqual(book, None)

    # def test_404_if_questions_does_not_exist(self):
    #     res = self.client().delete("/questions/-1")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    def test_request_one_question(self):
        res = self.client().post("/quizzes", json={
            'previous_questions': [1, 4, 20, 15], 
            'quiz_category': {'id':'1', 'type':'Science'}
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")


    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "World"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))

    def test_get_question_search_without_results(self):
        res = self.client().post(
            "/questions", json={"searchTerm": "sgfgfgfgfgfg"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["totalQuestions"], 0)
        self.assertEqual(len(data["questions"]), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()