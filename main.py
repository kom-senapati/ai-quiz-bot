import mindsdb_sdk
from dotenv import load_dotenv
import pandas as pd
import re

load_dotenv()

server = mindsdb_sdk.connect()
project = server.get_project("ai_quiz_bot")

quiz_generator = project.models.get("quiz_generator")


def parse_question(quiz_str):
    pattern = re.compile(
        r"Question:\s*(.*?)\s*Options:\s*A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*?)\s*Correct Answer:\s*([A-D])",
        re.DOTALL
    )
    
    match = pattern.search(quiz_str)
    
    if match:
        return {
            "Question": match.group(1).strip(),
            "Options": {
                "A": match.group(2).strip(),
                "B": match.group(3).strip(),
                "C": match.group(4).strip(),
                "D": match.group(5).strip()
            },
            "Correct Answer": match.group(6).strip()
        }
    else:
        return None

def generate_quiz(topic):
    quiz_df = pd.DataFrame(quiz_generator.predict({"topic": topic}))
    data = quiz_df["quiz_data"][0]
    return parse_question(data)

print(generate_quiz("Database"))