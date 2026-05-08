import streamlit as st
from services.training_service import generate_training_module

def render_training(files):
    st.subheader("Interactive Training & Summaries")

    if not files:
        st.warning("No documents available for training.")
        return

    doc = st.selectbox("Select Document:", files)

    if st.button("Generate Training Module"):
        with st.spinner(f"Building training module for {doc}..."):
            st.session_state["training_data"] = generate_training_module(doc)

    if "training_data" in st.session_state:
        data = st.session_state["training_data"]

        st.markdown("### 1. The 30-Second Summary")
        st.write(data["summary"])

        st.markdown("### 2. Why It Is Important")
        st.write(data["importance"])

        st.markdown("### 3. The Audit Trap")
        st.warning(f"**Watch Out:** {data['trap']}")

        st.markdown("### 4. Knowledge Check")
        user_answer = st.radio(data["question"], data["options"], index=None)

        if st.button("Submit Answer"):
            if user_answer is None:
                st.info("Please select an answer first.")
            selected_letter = data["options"].index(user_answer)
correct_letter = ["A", "B", "C", "D"][selected_letter]

if correct_letter == data["answer"]:
    st.success(f"**Correct!** {correct_letter}")
else:
    st.error(f"**Incorrect.** The correct answer was: {data['answer']}")
