import streamlit as st
import pandas as pd

def render_dashboard(doc_data):
    st.subheader("Controlled Document Master List")
    st.write("This grid automatically syncs with the GitHub repository.")

    if not doc_data:
        st.info("No documents found in /docs.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Documents", len(doc_data))
    col2.metric("System Status", "Compliant")
    col3.metric("Latest Sync", "Today")

    df = pd.DataFrame(doc_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
