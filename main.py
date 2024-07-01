import mindsdb_sdk
from dotenv import load_dotenv
import pandas as pd
from json import loads

load_dotenv()

server = mindsdb_sdk.connect()
project = server.get_project("ai_quiz_bot")

quiz_generator = project.models.get("quizzes_generator")


def generate_quiz(topic, number_of_questions=5):
    quiz_df = pd.DataFrame(
        quiz_generator.predict(
            {"number_of_questions": number_of_questions, "topic": topic}
        )
    )
    data = quiz_df["quiz_data"][0]
    try:
        return loads(data)
    except Exception as e:
        start_index = data.find('```json\n') + len('```json\n')
        end_index = data.rfind('\n```')
        json_str = data[start_index:end_index].strip()
        return loads(json_str)
