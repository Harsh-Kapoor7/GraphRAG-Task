import uuid
import streamlit as st
from authentication import authenticate, register
from document_processing import extract_text_and_images, split_text_into_chunks
from vector_store import initialize_vector_store
from workflow import build_workflow
from langchain import hub


def chat_interface(app):
    st.title("📚 Qdrant-Powered RAG Chatbot")

    # ✅ Ensure chat history is initialized
    if "history" not in st.session_state:
        st.session_state.history = []

    # ✅ Button to clear chat history
    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []  # Reset chat history
        st.rerun()  # Refresh UI

    # ✅ Display previous chat history
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ✅ Get user input
    user_input = st.chat_input("Ask something...")

    if user_input:
        thread_id = uuid.uuid4()
        config = {"configurable": {"thread_id": thread_id}}

        counter = 0
        last_dict = None

        # ✅ Stream response from chatbot
        for event in app.stream({"question": user_input, "history": st.session_state.history}, config, stream_mode="values"):
            counter += 1
            if counter == 3:
                last_dict = event
                break

        # ✅ Store and display user message
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # ✅ Store and display bot response
        if last_dict:
            response_text = last_dict['ans'].content
            st.session_state.history.append({"role": "assistant", "content": response_text})

            with st.chat_message("assistant"):
                st.markdown(response_text)


def initialize_chatbot():
    pdf_path = "Indika AI - Corporate Profile 2024.pdf"
    full_text, image_paths = extract_text_and_images(pdf_path)
    text_chunks = split_text_into_chunks(full_text)
    client, embeddings = initialize_vector_store(text_chunks)
    prompt = hub.pull("kaps/novacept")
    st.session_state.app = build_workflow(client, embeddings, prompt)

def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔐 User Authentication")

        action = st.radio("Select Action", ["Login", "Register"])

        if action == "Login":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful! Please wait we are getting your tool ready...")

                    # ✅ Initialize chatbot before rerunning UI
                    if "app" not in st.session_state or st.session_state.app is None:
                        initialize_chatbot()  

                    # ✅ Avoid unnecessary rerun
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        elif action == "Register":
            username = st.text_input("Username (for registration)")
            password = st.text_input("Password (for registration)", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif register(username, password):
                    st.success("Registration successful! You can now log in.")
                else:
                    st.error("Username already exists")

    else:
        # ✅ Only show chatbot after successful login
        st.write(f"Welcome, {st.session_state.username}! 👋")

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.app = None  # Clear chatbot session
            st.rerun()

        # ✅ Display chatbot after login
        # ✅ Pass chatbot instance to chat_interface
        chat_interface(st.session_state.app)


if __name__ == "__main__":
    main()
