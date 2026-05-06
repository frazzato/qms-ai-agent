import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import json
import datetime

# --- 1. UI & Page Setup ---
st.set_page_config(page_title="QMS Smart Repository", page_icon="📑", layout="wide")

# Secure API Connection
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    st.error("⚠️ System offline: API Key missing from cloud secrets. Please add it in Streamlit Cloud settings.")
    st.stop()

# Header
st.title("📑 AS9100 / ISO 9001 Smart Repository")
st.markdown("Intelligent document control, auditing, and training agent.")
st.divider()

# --- 2. Dynamic Document Scanner ---
DOCS_DIR = "docs"
doc_data = []
available_files = []

if os.path.exists(DOCS_DIR):
    for file in os.listdir(DOCS_DIR):
        if not file.startswith('.') and file != ".keep":
            available_files.append(file)
            
            # Clean up the file name for the dashboard
            name_no_ext = file.rsplit('.', 1)[0]
            ext = file.rsplit('.', 1)[1].upper() if '.' in file else "UNKNOWN"
            
            # Split "QP-001 - Document Control" into ID and Title
            if " - " in name_no_ext:
                doc_id, title = name_no_ext.split(" - ", 1)
            else:
                doc_id, title = "N/A", name_no_ext
                
            # Get file modification date
            stat = os.stat(os.path.join(DOCS_DIR, file))
            mod_date = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')

            doc_data.append({
                "Document ID": doc_id,
                "Title": title,
                "Format": ext,
                "Status": "Active Control",
                "Last Sync Date": mod_date
            })

# --- 3. App Layout (Tabs) ---
tab1, tab2, tab3 = st.tabs(["📊 Document Master List", "💬 AI Auditor Chat", "🎓 Training & Summaries"])

# --- TAB 1: The Spreadsheet Dashboard ---
with tab1:
    st.subheader("Controlled Document Master List")
    st.write("This grid automatically syncs with the GitHub repository.")
    
    if doc_data:
        # Display top metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Documents", len(doc_data))
        col2.metric("System Status", "Compliant")
        col3.metric("Latest Sync", datetime.datetime.now().strftime("%Y-%m-%d"))
        
        # Display the highly functional data-grid UI
        df = pd.DataFrame(doc_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No documents found. Please ensure files are in the /docs folder.")

# --- TAB 2: AI Chat ---
with tab2:
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
            response = model.generate_content(prompt)
            st.chat_message("assistant").write(response.text)

# --- TAB 3: Training Mode ---
with tab3:
    st.subheader("Interactive Training & Summaries")
    st.write("Select a document to instantly generate a study guide and knowledge check.")
    
    if not available_files:
        st.warning("No documents available for training.")
    else:
        doc_to_study = st.selectbox("Select Document:", available_files)
        
        if st.button("Generate Training Module"):
            with st.spinner(f"Building training module for {doc_to_study}..."):
                
                training_prompt = f"""
                You are a Senior QMS Trainer specializing in AS9100. Create a training module for the document titled: {doc_to_study}.
                Return ONLY a valid JSON object (no markdown formatting, no code blocks) with exactly these keys:
                "summary": "3 bullet points summarizing the purpose of this procedure",
                "importance": "Brief explanation of why AS9100 requires this",
                "trap": "The most common audit mistake related to this",
                "question": "One multiple choice question to test understanding",
                "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
                "answer": "The exact text of the correct option from the list above"
                """
                
                try:
                    response = model.generate_content(training_prompt)
                    raw_text = response.text.strip().replace("```json", "").replace("```", "")
                    st.session_state['training_data'] = json.loads(raw_text)
                except Exception as e:
                    st.error("Failed to generate training module. Please click generate again.")

        # Display Training Data if it exists in session memory
        if 'training_data' in st.session_state:
            data = st.session_state['training_data']
            
            st.markdown("### 1. The 30-Second Summary")
            st.write(data['summary'])
            
            st.markdown("### 2. Why It Is Important")
            st.write(data['importance'])
            
            st.markdown("### 3. The Audit Trap")
            st.warning(f"**Watch Out:** {data['trap']}")
            
            st.divider()
            
            st.markdown("### 4. Knowledge Check")
            user_answer = st.radio(data['question'], data['options'], index=None)
            
            if st.button("Submit Answer"):
                if user_answer is None:
                    st.info("Please select an answer first.")
                elif user_answer == data['answer']:
                    st.success(f"**Correct!** {user_answer}")
                else:
                    st.error(f"**Incorrect.** The correct answer was: {data['answer']}")
