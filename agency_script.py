from dotenv import load_dotenv
import os
from typing import List, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain.schema import AgentAction
import requests
import json
import streamlit as st
from datetime import datetime

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


class State(TypedDict):
    application: str
    experience_level: str
    skill_match: str
    response: str


workflow = StateGraph(State)


def categorize_experience(state: State) -> State:
    """Categorize candidate's experience level based on their application"""
    prompt = ChatPromptTemplate.from_template(
        """Based on the job application below, categorize the candidate's experience level.

    Consider the following criteria:
    - Entry-level: 0-2 years of experience, recent graduate, junior positions
    - Mid-level: 3-7 years of experience, solid foundation, some leadership
    - Senior-level: 8+ years of experience, leadership roles, expert knowledge

    Respond with ONLY one of these exact phrases: 'Entry-level', 'Mid-level', or 'Senior-level'

    Application: {application}"""
    )
    chain = prompt | llm
    experience_level = chain.invoke({"application": state["application"]}).content.strip()
    return {"experience_level": experience_level}


def assess_skillset(state: State) -> State:
    """Assess if candidate's skills match the Python Developer job requirements"""
    prompt = ChatPromptTemplate.from_template(
        """You are evaluating a candidate for a Python Developer position.

    Required skills for this role:
    - Python programming (mandatory)
    - Web frameworks (Django, Flask, FastAPI)
    - Database knowledge (SQL, PostgreSQL, MongoDB)
    - Version control (Git)
    - Testing frameworks
    - API development
    - Basic DevOps knowledge is a plus

    Based on the application below, determine if the candidate's skills match our requirements.
    Consider both direct mentions and transferable skills.

    Respond with ONLY one of these exact phrases: 'Match' or 'No Match'

    Application: {application}"""
    )
    chain = prompt | llm
    skill_match = chain.invoke({"application": state["application"]}).content.strip()
    return {"skill_match": skill_match}


def schedule_hr_interview(state: State) -> State:
    """Schedule HR interview for qualified candidates"""
    return {
        "response": "🎉 Congratulations! Your application has been shortlisted. You will be contacted within 2-3 business days to schedule an HR interview. Our team will discuss the role details, compensation, and next steps with you."
    }


def escalate_to_recruiter(state: State) -> State:
    """Escalate senior candidates who don't match current role to recruiter"""
    return {
        "response": "🔄 Thank you for your application. While your experience is impressive, your skillset doesn't align with our current Python Developer role. However, we're forwarding your profile to our recruitment team to explore other suitable opportunities within our organization."
    }


def reject_application(state: State) -> State:
    """Send rejection for candidates who don't meet requirements"""
    return {
        "response": "📝 Thank you for your interest in our Python Developer position. After careful review, we've decided to move forward with other candidates whose experience and skills more closely match our current requirements. We encourage you to apply for future openings that align with your background."
    }


# Add nodes to workflow
workflow.add_node("categorize_experience", categorize_experience)
workflow.add_node("assess_skillset", assess_skillset)
workflow.add_node("schedule_hr_interview", schedule_hr_interview)
workflow.add_node("escalate_to_recruiter", escalate_to_recruiter)
workflow.add_node("reject_application", reject_application)


def route_application(state: State) -> str:
    """Route application based on skill match and experience level"""
    if "Match" in state["skill_match"]:
        return "schedule_hr_interview"
    elif "Senior-level" in state["experience_level"]:
        return "escalate_to_recruiter"
    else:
        return "reject_application"


# Add edges to workflow
workflow.add_edge(START, "categorize_experience")
workflow.add_edge("categorize_experience", "assess_skillset")
workflow.add_conditional_edges("assess_skillset", route_application)
workflow.add_edge("schedule_hr_interview", END)
workflow.add_edge("escalate_to_recruiter", END)
workflow.add_edge("reject_application", END)

# Compile the workflow
app = workflow.compile()


def run_candidate_screening(application: str):
    """Main function to process candidate application"""
    results = app.invoke({"application": application})
    return {
        "experience_level": results["experience_level"],
        "skill_match": results["skill_match"],
        "response": results["response"]
    }


def get_status_color(skill_match: str, experience_level: str) -> str:
    """Return color based on application status"""
    if "Match" in skill_match:
        return "success"
    elif "Senior-level" in experience_level:
        return "warning"
    else:
        return "error"


def main():
    """Streamlit UI for HR Candidate Screening System"""
    st.set_page_config(
        page_title="HR Candidate Screening System",
        page_icon="👥",
        layout="wide"
    )

    # Header
    st.title("👥 AI-Powered HR Candidate Screening System")
    st.markdown("**Python Developer Position - Automated Resume Screening**")
    st.markdown("---")

    # Initialize session state
    if "screening_history" not in st.session_state:
        st.session_state.screening_history = []

    # Main content in columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📄 Submit Candidate Application")

        # Input methods
        input_method = st.radio(
            "Choose input method:",
            ["Paste Application Text", "Upload Resume", "Fill Application Form"],
            horizontal=True
        )

        application_text = ""

        if input_method == "Paste Application Text":
            application_text = st.text_area(
                "Paste the candidate's application or resume text:",
                height=200,
                placeholder="Paste the complete application text here including experience, skills, education, and projects..."
            )

        elif input_method == "Upload Resume":
            uploaded_file = st.file_uploader(
                "Upload Resume (PDF/TXT)",
                type=['pdf', 'txt'],
                help="Upload the candidate's resume file"
            )
            if uploaded_file:
                st.info("📎 File uploaded successfully! Resume parsing feature coming soon.")
                application_text = st.text_area(
                    "For now, please paste the resume content:",
                    height=150
                )

        else:  # Fill Application Form
            st.write("**Quick Application Form:**")
            name = st.text_input("Full Name")
            experience_years = st.number_input("Years of Experience", min_value=0, max_value=50)
            skills = st.multiselect(
                "Technical Skills",
                ["Python", "Django", "Flask", "FastAPI", "JavaScript", "React", "SQL", "PostgreSQL",
                 "MongoDB", "Git", "Docker", "AWS", "REST APIs", "GraphQL", "Machine Learning", "Data Science"]
            )
            additional_info = st.text_area("Additional Information (Projects, Achievements, etc.)")

            if name and skills:
                application_text = f"""
                Name: {name}
                Experience: {experience_years} years
                Skills: {', '.join(skills)}
                Additional Information: {additional_info}
                """

        # Screen Application Button
        if st.button("🔍 Screen Application", type="primary", use_container_width=True):
            if application_text.strip():
                with st.spinner("🤖 AI is analyzing the application..."):
                    try:
                        results = run_candidate_screening(application_text)

                        # Store in session state
                        screening_result = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "application": application_text[:100] + "..." if len(
                                application_text) > 100 else application_text,
                            **results
                        }
                        st.session_state.screening_history.insert(0, screening_result)

                        # Display Results
                        st.success("✅ Screening completed!")

                        # Results in an attractive format
                        with st.container():
                            st.subheader("📊 Screening Results")

                            # Create columns for results
                            res_col1, res_col2, res_col3 = st.columns(3)

                            with res_col1:
                                st.metric("Experience Level", results["experience_level"])

                            with res_col2:
                                skill_color = "🟢" if "Match" in results["skill_match"] else "🔴"
                                st.metric("Skill Match", f"{skill_color} {results['skill_match']}")

                            with res_col3:
                                status_color = get_status_color(results["skill_match"], results["experience_level"])
                                if status_color == "success":
                                    status_icon = "✅ Shortlisted"
                                elif status_color == "warning":
                                    status_icon = "⚠️ Escalated"
                                else:
                                    status_icon = "❌ Rejected"
                                st.metric("Status", status_icon)

                            # Final Response
                            st.subheader("💬 Final Decision")
                            if "shortlisted" in results["response"].lower():
                                st.success(results["response"])
                            elif "forwarding" in results["response"].lower():
                                st.warning(results["response"])
                            else:
                                st.error(results["response"])

                    except Exception as e:
                        st.error(f"❌ Error during screening: {str(e)}")
            else:
                st.warning("⚠️ Please provide application text before screening.")

    with col2:
        st.subheader("📋 Job Requirements")
        st.markdown("""
        **Python Developer Position**

        **Required Skills:**
        - ✅ Python programming
        - ✅ Web frameworks (Django/Flask)
        - ✅ Database knowledge (SQL)
        - ✅ Version control (Git)
        - ✅ API development

        **Preferred Skills:**
        - 🔹 Testing frameworks
        - 🔹 Cloud platforms (AWS/GCP)
        - 🔹 DevOps knowledge
        - 🔹 Frontend technologies

        **Experience Levels:**
        - **Entry:** 0-2 years
        - **Mid:** 3-7 years  
        - **Senior:** 8+ years
        """)

        # Quick Stats
        if st.session_state.screening_history:
            st.subheader("📈 Quick Stats")
            total_applications = len(st.session_state.screening_history)
            shortlisted = sum(
                1 for app in st.session_state.screening_history if "shortlisted" in app["response"].lower())
            escalated = sum(1 for app in st.session_state.screening_history if "forwarding" in app["response"].lower())
            rejected = total_applications - shortlisted - escalated

            st.metric("Total Applications", total_applications)
            st.metric("Shortlisted", shortlisted)
            st.metric("Escalated", escalated)
            st.metric("Rejected", rejected)

    # Screening History
    if st.session_state.screening_history:
        st.markdown("---")
        st.subheader("📚 Recent Screening History")

        for i, result in enumerate(st.session_state.screening_history[:5]):  # Show last 5
            with st.expander(f"Application {i + 1} - {result['timestamp']} - {result['experience_level']}"):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.write("**Application Text:**")
                    st.write(result["application"])
                with col_b:
                    st.write(f"**Experience:** {result['experience_level']}")
                    st.write(f"**Skills:** {result['skill_match']}")
                st.write("**Response:**")
                st.write(result["response"])

        if st.button("🗑️ Clear History"):
            st.session_state.screening_history = []
            st.rerun()


def run_terminal_version():
    """Terminal version for testing"""
    print("🤖 HR Candidate Screening System")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Screen a candidate")
        print("2. Exit")

        choice = input("\nEnter your choice (1-2): ").strip()

        if choice == "1":
            print("\n" + "=" * 50)
            application_text = input("Enter candidate application text: ")

            if application_text.strip():
                print("\n🤖 Processing application...")
                results = run_candidate_screening(application_text)

                print(f"\n📊 SCREENING RESULTS")
                print("=" * 30)
                print(f"Experience Level: {results['experience_level']}")
                print(f"Skill Match: {results['skill_match']}")
                print(f"\n💬 Final Decision:")
                print(results['response'])
                print("=" * 50)
            else:
                print("⚠️ Please provide application text.")

        elif choice == "2":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    # Uncomment the line below to run in terminal mode
    # run_terminal_version()

    # Run Streamlit app
    main()