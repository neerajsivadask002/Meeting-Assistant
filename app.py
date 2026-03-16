import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import List
import json

# --- Page Configuration ---
st.set_page_config(page_title="AI Meeting Assistant", page_icon="📝")
st.title("📝 AI Meeting Assistant")
st.markdown("""
Transform raw meeting notes into structured summaries and actionable tasks.
""")

# --- Sidebar for API Key ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    st.markdown("[Get your API Key](https://platform.openai.com/api-keys)")
    st.info("Keys are not stored and are only used for the current session.")

# --- Data Models ---
class ActionItem(BaseModel):
    task: str = Field(description="The specific action to be taken")
    owner: str = Field(description="The person responsible for the task")
    deadline: str = Field(description="Mentioned deadline or 'Not specified'")

class MeetingSummary(BaseModel):
    summary: str = Field(description="A concise summary of the meeting")
    key_decisions: List[str] = Field(description="List of key decisions made")
    action_items: List[ActionItem] = Field(description="List of actionable tasks")

# --- Functions ---
def process_meeting_notes(notes, key):
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=key)
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert meeting assistant. Analyze the provided notes and extract structured information. Output ONLY valid JSON."),
            ("human", "Meeting Notes:\n{notes}"),
        ])
        
        # Create the chain
        chain = prompt | llm | StrOutputParser()
        
        # Invoke the chain
        response = chain.invoke({"notes": notes})
        
        # Clean the response (remove markdown code blocks if present)
        response = response.replace("```json", "").replace("```", "").strip()
        
        # Parse JSON
        data = json.loads(response)
        return data
    except Exception as e:
        st.error(f"Processing error: {str(e)}")
        return None

# --- Main Interface ---
text_input = st.text_area("Paste Meeting Notes Here", height=200, placeholder="e.g., John agreed to update the API by Friday...")

if st.button("Generate Summary"):
    if not api_key:
        st.warning("Please enter your OpenAI API Key in the sidebar.")
    elif not text_input:
        st.warning("Please enter some meeting notes.")
    else:
        with st.spinner("Analyzing notes..."):
            result = process_meeting_notes(text_input, api_key)
            
            if result:
                st.success("Analysis Complete!")
                
                # Display Summary
                st.subheader("Summary")
                st.write(result.get("summary", "No summary available"))
                
                # Display Decisions
                st.subheader("Key Decisions")
                for decision in result.get("key_decisions", []):
                    st.write(f"- {decision}")
                
                # Display Action Items
                st.subheader("Action Items")
                for item in result.get("action_items", []):
                    with st.expander(f"Task: {item.get('task', 'Unknown Task')}"):
                        st.write(f"**Owner:** {item.get('owner', 'Unassigned')}")
                        st.write(f"**Deadline:** {item.get('deadline', 'Not specified')}")
                
                # Download Option
                st.download_button(
                    label="Download Report as JSON",
                    data=json.dumps(result, indent=2),
                    file_name="meeting_report.json",
                    mime="application/json"
                )
