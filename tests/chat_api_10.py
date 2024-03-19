# //////////////////////
# Archived'/
# From Hugging Face
# \\\\\\\\\\\\\\\\\\\\\\


import requests

# API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_URL = "https://api-inference.huggingface.co/models/ThisIs-Developer/Llama-2-GGML-Medical-Chatbot"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query(
    {
        "inputs": {
            "past_user_inputs": [
                """You should act as medical advisor.
                    You will get a description of a patient on its general health and any syptoms the patient has.
                    Your job is to propose which doctor the patient should consult based on the description, also you will  provide a few tips for only preparing before the appointment.
                    You should structure your reply as:  "The recommended doctor for you to consult is: <category of doctor>." and the give some tips for only preparing before the appointment.
                    I don't need any medical advice. """
                    ],
            "generated_responses": ["It is Die Hard for sure."],
            "text": "The description: When I have period I feel a lot of pain in my belly and I feel weak and my energy is low.",
        },
    }
)

print(output)
