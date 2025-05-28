# 👥 AI-Powered HR Candidate Screening System

An intelligent automated recruitment system built with LangGraph and Google Gemini that streamlines the candidate screening process for Python Developer positions with smart classification, skill assessment, and automated decision-making.

## 🌟 Features

- **Automated Experience Classification**: Categorizes candidates into Entry-level, Mid-level, or Senior-level
- **Intelligent Skill Matching**: Assesses technical skills against job requirements
- **Smart Routing Logic**: Automatically routes applications based on assessment results
- **Interactive Web Interface**: Clean Streamlit UI with multiple input methods
- **Real-time Processing**: Instant candidate screening with detailed feedback
- **Screening History**: Track and review past screening decisions
- **Multiple Input Methods**: Text paste, file upload, or structured form

## 🏗️ System Architecture

The system uses a **3-node workflow** built with LangGraph:

1. **Experience Categorization**: Analyzes years of experience and career progression
2. **Skill Assessment**: Evaluates technical skills against Python Developer requirements
3. **Decision Routing**: Routes candidates based on assessment results:
   - **Shortlist**: Skills match → Schedule HR Interview
   - **Escalate**: Senior-level experience but skills don't match → Forward to recruiter
   - **Reject**: Insufficient experience and skills don't match → Send rejection

## 📊 Workflow Diagram

![HR Screening Workflow](https://github.com/mv1249/RecruitmentAgencyWorkflow/blob/main/image%20(4).png)

```
START → Experience Classification → Skill Assessment → Decision Router → [Shortlist | Escalate | Reject] → END
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API Key (from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/hr-candidate-screening.git
cd hr-candidate-screening
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

4. **Run the application:**
```bash
streamlit run hr_screening_system.py
```

5. **Access the application:**
Open your browser and navigate to `http://localhost:8501`

## 📦 Dependencies

```txt
streamlit>=1.28.0
langgraph>=0.0.40
langchain-google-genai>=1.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
typing-extensions>=4.0.0
```

## 🔧 Usage

### Web Interface

1. **Choose Input Method:**
   - **Paste Text**: Copy-paste resume/application text
   - **Upload File**: Upload PDF/TXT resume files
   - **Fill Form**: Use structured application form

2. **Submit Application:** Click "Screen Application" to process

3. **Review Results:** Get instant feedback with:
   - Experience level classification
   - Skill match assessment
   - Final decision with detailed explanation

### Terminal Mode

For testing and development:
```python
# Uncomment in main function
run_terminal_version()
```

## 🎯 Job Requirements

### Python Developer Position

**Required Skills:**
- Python programming (mandatory)
- Web frameworks (Django, Flask, FastAPI)
- Database knowledge (SQL, PostgreSQL, MongoDB)
- Version control (Git)
- Testing frameworks
- API development

**Preferred Skills:**
- Basic DevOps knowledge
- Cloud platforms (AWS, GCP)
- Frontend technologies
- Machine Learning experience

**Experience Categories:**
- **Entry-level**: 0-2 years (Recent graduates, junior positions)
- **Mid-level**: 3-7 years (Solid foundation, some leadership)
- **Senior-level**: 8+ years (Leadership roles, expert knowledge)

## 🔄 Decision Logic

| Experience Level | Skill Match | Decision | Action |
|------------------|-------------|----------|---------|
| Any Level | Match | ✅ **Shortlist** | Schedule HR Interview |
| Senior-level | No Match | ⚠️ **Escalate** | Forward to recruiter for other roles |
| Entry/Mid-level | No Match | ❌ **Reject** | Send rejection email |

## 📊 Example Screening Results

### Successful Candidate
```
Input: "5 years of Python development experience with Django and Flask. 
       Built REST APIs, worked with PostgreSQL, and used Git for version control."

Output:
- Experience Level: Mid-level
- Skill Match: Match
- Decision: Shortlisted for HR Interview
```

### Senior Candidate (Skills Mismatch)
```
Input: "15 years of Java enterprise development, team lead experience, 
       extensive knowledge in Spring Boot and Oracle databases."

Output:
- Experience Level: Senior-level
- Skill Match: No Match
- Decision: Escalated to recruiter for other opportunities
```

## 🛠️ Customization

### Modify Job Requirements

Update the skill assessment prompt in `assess_skillset()`:

```python
Required skills for this role:
- Python programming (mandatory)
- Your custom requirements here
```

### Adjust Experience Thresholds

Modify the experience categorization in `categorize_experience()`:

```python
- Entry-level: 0-2 years
- Mid-level: 3-7 years  
- Senior-level: 8+ years
```

### Change Decision Logic

Update the routing function in `route_application()`:

```python
def route_application(state: State) -> str:
    # Your custom routing logic here
    return "your_decision_node"
```

## 📈 Future Enhancements

- [ ] **Resume Parsing**: PDF/DOCX file processing with OCR
- [ ] **Multi-language Support**: Support for non-English resumes
- [ ] **Advanced Analytics**: Detailed screening metrics and reports
- [ ] **Integration APIs**: Connect with ATS systems
- [ ] **Custom Job Profiles**: Support for different job roles
- [ ] **Candidate Feedback**: Automated personalized feedback emails
- [ ] **Batch Processing**: Process multiple applications simultaneously
- [ ] **Interview Scheduling**: Integrate with calendar systems

## 🧪 Testing

### Sample Applications for Testing

**Entry-level Match:**
```
"Recent computer science graduate with 1 year internship experience. 
Proficient in Python, built web applications using Flask, familiar with Git and SQL."
```

**Mid-level Match:**
```
"4 years of Python development experience. Expert in Django, REST API development, 
PostgreSQL, and automated testing. Led small development teams."
```

**Senior-level No Match:**
```
"12 years of C++ game development experience. Expert in Unreal Engine, 
3D graphics programming, and performance optimization."
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Performance Metrics

- **Processing Time**: ~2-3 seconds per application
- **Accuracy**: High precision in experience classification
- **Throughput**: Suitable for small to medium-scale recruitment
- **Scalability**: Easily deployable on cloud platforms

## 🔐 Security & Privacy

- **Data Privacy**: No application data is stored permanently
- **API Security**: Environment variables for sensitive keys
- **Session Management**: Secure session handling in Streamlit
- **Data Encryption**: HTTPS recommended for production

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph** for the powerful workflow orchestration
- **Google Gemini** for advanced language processing capabilities
- **Streamlit** for the intuitive web interface framework
- **HR Community** for insights into recruitment best practices



## 🚀 Deployment

### Local Development
```bash
streamlit run hr_screening_system.py
```

### Docker Deployment
```bash
docker build -t hr-screening .
docker run -p 8501:8501 hr-screening
```

### Cloud Deployment
- **Streamlit Cloud**: Direct GitHub integration
- **Heroku**: Easy deployment with Procfile
- **AWS/GCP**: Containerized deployment options

---

**Built with ❤️ for HR professionals and recruitment teams worldwide**

---
