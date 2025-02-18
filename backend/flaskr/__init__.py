from http.client import HTTPException
from multiprocessing import AuthenticationError
import os
from sunau import AUDIO_FILE_ENCODING_ADPCM_G721
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    # app.run(debug=True)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #CORS(app, resources={r"*/api/*" : {origins: '*'}})
    CORS(app)
    

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=['GET'])
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            categories_formated={categorie.format()['id']: categorie.format()['type'] for categorie in categories}

            if len(categories_formated) == 0:
                abort(404)
                
            return jsonify(
                {
                    "success": True,
                    "categories": categories_formated,
                }
            )
        except (AuthenticationError, MemoryError): # included for future use case
            abort(422)
        except Exception as e:
            if e.code == 404:
                abort(e.code)
            else:
                abort(422)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route("/questions")
    def retrieve_questions():
        try:
            selection = Question.query.order_by(
            Question.id).paginate(per_page=QUESTIONS_PER_PAGE).items
        
            current_questions = [question.format() for question in selection]
            categories = Category.query.order_by(Category.id).all()
            categories_formated={categorie.format()['id']: categorie.format()['type'] for categorie in categories}

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "categories": categories_formated,
                    "currentCategory": None,
                    "total_questions": len(Question.query.order_by(Question.id).all()),
                }
            )
        except (AuthenticationError, MemoryError, TypeError):  # included for future use case
            abort(422)
        except Exception:
            abort(422)

    

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            

            selection = Question.query.order_by(
                Question.id).paginate(per_page=QUESTIONS_PER_PAGE).items

            current_questions = [question.format() for question in selection]

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "totalQuestions": len(Question.query.order_by(Question.id).all()),
                }
            )

        except (AuthenticationError, MemoryError, TypeError):  # included for future use case
            abort(422)
        except Exception as e:
            if e.code == 404:
                abort(e.code)
            else:
                abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def create_question():
        new_question = ""
        new_answer = ""
        new_difficulty = None
        new_category = None
        search_term = None
        try:
            body = request.get_json()
            search_term = body.get("searchTerm", None)
            body = request.get_json()
            new_question = body.get("question", "")
            new_answer = body.get("answer", "")
            new_difficulty = body.get("difficulty", None)
            new_category = body.get("category", None)
            if search_term:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search_term))
                ).paginate(per_page=QUESTIONS_PER_PAGE).items
                current_questions = [question.format()
                                    for question in selection]

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "totalQuestions": len(selection),
                        "currentCategory": None,
                    }
                )

            else:

                # User Input handling
                if new_question.isspace() or new_answer.isspace() or new_question == "" or new_answer == "":
                    print("Hello deux")
                    raise AttributeError(
                        "Sorry, question, answer, category, and difficulty should not be empty")

                if not isinstance(new_difficulty, int):
                    print("exception raise two")
                    raise TypeError("Sorry, difficulty should be an integer")
                if new_difficulty not in range(1, 6):
                    print("exception raise two")
                    raise TypeError("Sorry, difficulty should be an integer between 1 and 5")

                if not isinstance(new_category, int):
                    abort(422)

                category = Category.query.filter(Category.id == new_category).all()
                if len(category) == 0:
                    abort(422)

                question = Question(question=new_question,
                                answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()
                selection = Question.query.order_by(Question.id).paginate(
                    per_page=QUESTIONS_PER_PAGE).items
                current_questions = [question.format()
                                        for question in selection]

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_questions,
                        "total_questions": len(Question.query.order_by(Question.id).all()),
                    }
                )

        except (AuthenticationError, MemoryError, TypeError):  # included for future use case
            abort(422)
        except Exception:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    # @app.route("/questions/search", methods=["POST"])
    # def search_question():
    #     try:
    #         body = request.get_json()
    #         search_term = body.get("searchTerm", None)
    #         selection = Question.query.order_by(Question.id).filter(
    #             Question.question.ilike("%{}%".format(search_term))
    #         ).paginate(per_page=QUESTIONS_PER_PAGE).items
    #         current_questions = [question.format()
    #                                 for question in selection]

    #         return jsonify(
    #             {
    #                 "success": True,
    #                 "questions": current_questions,
    #                 "totalQuestions": len(selection),
    #                 "currentCategory": None,
    #             }
    #         )

    #     except (AuthenticationError, MemoryError, TypeError):  # included for future use case
    #         abort(422)
    #     except Exception:
    #         abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def retrieve_questions_by_category(category_id):
        questions = list()
        try:
            questions = Question.query.join(Category, Question.category == Category.id).filter(
                Category.id == category_id).all()

            if not questions:
                abort(404)

            questions = [question.format() for question in questions]
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "currentCategory": category_id,
                    "totalQuestions": len(Question.query.order_by(Question.id).all()),
                }
            )

        except (AuthenticationError, MemoryError, TypeError):  # included for future use case
            abort(422)
        except Exception as e:
            if e.code == 404:
                abort(e.code)
            else:
                abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def request_quizes():

        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category = body.get("quiz_category", None)
            question = 0
            if quiz_category != None:

                rand = random.randrange(0, len(Category.query.join(
                    Question, Category.id == Question.category).filter(Category.id == quiz_category['id']).one().questions))

                question = Category.query.join(Question, Category.id == Question.category).filter(
                    Category.id == quiz_category['id']).filter(Question.id.notin_(previous_questions)).one().questions[rand]
            else:
                rand = random.randrange(0, Question.query.count()) 
                question = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()[rand]
            if question != 0:
                return jsonify(
                    {
                        "success": True,
                        "question": question.format(),
                    }
                )
            else:
                abort(404)

        except (AuthenticationError, MemoryError, TypeError):  # included for future use case
            abort(422)
        except Exception as e:
            if e.code == 404:
                abort(e.code)
            else:
                abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )


    return app

