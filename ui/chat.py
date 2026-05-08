import streamlit as st
from services.ai_service import ask_groq

def render_chat():
    st.subheader("QMS Assistant")
    st.write("Ask questions about procedures, AS9100 clauses, or request audit checklists.")

    user_query = st.chat_input("E.g., What is the standard procedure for controlling nonconforming outputs?")

    if user_query:
        st.chat_message("user").write(user_query)

        prompt = f"""
        You are an elite AS9100 and ISO 9001 QMS Auditor.
        Answer the following user query strictly using standard quality management principles.
        User Query: {user_query}
        """

        with st.spinner("Analyzing compliance standards..."):
           response = ask_groq(user_input)

        st.chat_message("assistant").write(answer)
