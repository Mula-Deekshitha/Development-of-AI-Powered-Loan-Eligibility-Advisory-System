 
# AI-Powered Loan Eligibility Advisory System

This is a complete, real-time credit underwriting application designed for a banking environment. It uses a sophisticated AI model, intelligent document analysis (OCR), and a voice-enabled chatbot to automate and enhance the loan approval workflow.

## Key Features

* **Bank-Grade AI:** A "Hard Rules Engine" immediately rejects high-risk applicants based on critical factors like missed EMI payments, followed by a nuanced prediction from a Random Forest model.
* **Dynamic AI Training:** The model is automatically trained on server startup using both a historical dataset and real-world application data, allowing it to become smarter over time.
* **Intelligent Document Analysis:** The system uses advanced OCR with image pre-processing (OpenCV) and a multi-pass parsing engine to accurately extract and verify data from bank statements, Aadhaar cards, and salary slips.
* **Voice-Enabled Chatbot:** An accessible, conversational AI that guides customers through the entire application process with strict, real-time validation for every question.
* **End-to-End Workflow:** A complete, seamless process from initial customer interaction to final admin approval and automatic PDF report generation.

## Technology Stack

| Category      | Technology                    | Reason                                                               |
| :------------ | :---------------------------- | :------------------------------------------------------------------- |
| **Backend** | Python, FastAPI, Socket.IO    | High performance, industry standard for AI, and robust real-time capabilities. |
| **AI/Data** | Scikit-learn, Pandas, OpenCV  | Powerful, reliable libraries for building the prediction model and processing documents. |
| **Database** | SQLModel, SQLite              | Clean, Pythonic database interaction, simple for development.        |
| **Frontend** | HTML, CSS, Vanilla JavaScript | Lightweight, fast, and universally compatible with no complex build steps. |

## Local Setup & Run Instructions

**1. Backend Setup:**
```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment
# On Windows:
python -m venv venv
venv\Scripts\activate

# Install dependencies (ensure Tesseract OCR is installed on your system)
pip install -r requirements.txt

# Run the server (this will also train the AI model)
python -m uvicorn app.main:app --reload
Frontend Setup:



# Open a NEW terminal and navigate to the frontend folder
cd web_frontend

# Start the simple web server on port 8001
python -m http.server 8001

Open your browser and go to http://localhost:8001.
