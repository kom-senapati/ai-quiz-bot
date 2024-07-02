import mindsdb_sdk
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# Connecting to the database and create the table

db_path = os.path.abspath(os.getcwd()) + "\\quiz_database.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_table (
  topic TEXT,
  question TEXT,
  option_a TEXT,
  option_b TEXT,
  option_c TEXT,
  option_d TEXT,
  correct_answer CHAR(1)
)
""")

server = mindsdb_sdk.connect()

server.ml_engines.create(
    "minds_endpoint_engine",
    "minds_endpoint",
    connection_data={"minds_endpoint_api_key": os.getenv("API_KEY")},
)

project = server.create_project("ai_quiz_bot")
project = server.get_project("ai_quiz_bot")

project.models.create(
    name="quizzes_generator",
    predict="quiz_data",
    engine="minds_endpoint_engine",
    max_tokens=512,
    prompt_template="Generate only {{number_of_questions}} short quiz questions about {{topic}} with 4 multiple-choice options (A, B, C, D) and the correct option letter. Format the output in parsable json as: [{'q':...,A,B,C,D,correct},{...}]",
)
