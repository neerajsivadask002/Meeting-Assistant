import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

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
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=key)
    
    parser = PydanticOutputParser(pydantic_object=MeetingSummary)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert meeting assistant. Analyze the provided notes and extract structured information."),
        ("human", "Meeting Notes:\n{notes}\n\nFormat the output strictly as JSON according to the following schema:\n{format_instructions}"),
    ])
    
    chain = prompt | llm | parser
    
    try:
        response = chain.invoke({"notes": notes, "format_instructions": parser.get_format_instructions()})
        return response
    except Exception as e:
        st.error(f"Processing error: {e}")
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
                st.write(result.summary)
                
                # Display Decisions
                st.subheader("Key Decisions")
                for decision in result.key_decisions:
                    st.write(f"- {decision}")
                
                # Display Action Items
                st.subheader("Action Items")
                for item in result.action_items:
                    with st.expander(f"Task: {item.task}"):
                        st.write(f"**Owner:** {item.owner}")
                        st.write(f"**Deadline:** {item.deadline}")
                
                # Download Option
                st.download_button(
                    label="Download Report as JSON",
                    data=result.json(),
                    file_name="meeting_report.json",
                    mime="application/json"
                )