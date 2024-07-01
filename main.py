import mindsdb_sdk
from dotenv import load_dotenv
import pandas as pd
from json import loads

load_dotenv()

server = mindsdb_sdk.connect()
project = server.get_project("ai_quiz_bot")

quiz_generator = project.models.get("quizzes_generator")


def generate_quiz(number_of_questions, topic):
    quiz_df = pd.DataFrame(
        quiz_generator.predict(
            {"number_of_questions": number_of_questions, "topic": topic}
        )
    )
    data = quiz_df["quiz_data"][0]
    return loads(data)

print(generate_quiz(5, "database"))
