from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                Your job is to verify whether the given AI response is factually and contextually aligned with the user's query. Identify any hallucinations, inaccuracies, or irrelevant information.
                Accurate & Contextually Relevant – No hallucinations detected.
                Partially Relevant (Minor Hallucinations) – Some minor inconsistencies, but mostly accurate.
                Hallucinated Response – Contains significant inaccuracies or off-topic information.
                Bring output in the following format only:
                Eg.1 - 
                {
                    "output": "correct",
                    "suggested_correction": "None"
                }
                Eg. 2 - 
                {
                    "output": "incorrect",
                    "suggested_correction": "Provide a response that sticks to verifiable facts and aligns with the query."
                }
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a chatbot. Answer queries using the provided context. If the context is unrelated to the query, use your own knowledge. Keep responses concise and avoid unnecessary phrases like, 'This was not provided in the context, but according to my knowledge..."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm
