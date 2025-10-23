from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from reportlab.pdfgen import canvas
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def generate_assessment(data):
    credit_score = int(data.get('credit_score', 0))
    income = int(data.get('income', 0))
    loan_amnt = data.get('loan_amnt', 'N/A')
    loan_type = data.get('loan_type', 'N/A')
    bank = data.get('bank_name', 'N/A')
    tenure = data.get('loan_tenure', 'N/A')

    reason = "Low credit score and high existing debt" if credit_score < 650 else "Eligible"
    recommendations = [
        "Improve your credit score through timely payments",
        "Consider reducing existing debt obligations",
        "Add a co-applicant to strengthen application",
        "Apply for a lower loan amount initially",
        "Maintain consistent income inflow"
    ] if credit_score < 650 else ["You're on track! Maintain your financial discipline."]

    summary = f"""
📋 Loan Eligibility Assessment

🔍 Reason: {reason}  
💳 Credit Score: {credit_score}  
💰 Monthly Income: ₹{income}  
🏦 Bank: {bank}  
📄 Loan Type: {loan_type}  
💸 Requested Amount: ₹{loan_amnt}  
📆 Tenure: {tenure} months  

✅ Recommendations:
{chr(10).join([f"{i+1}. {r}" for i, r in enumerate(recommendations)])}
"""
    return summary


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # You can add authentication logic here
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect('/dashboard')
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.json.get('message', '').strip()
        session.setdefault('loan_data', {})
        data = session['loan_data']

        def is_valid_number(value): return value.isdigit()
        def is_valid_credit_score(value): return value.isdigit() and 300 <= int(value) <= 900
        def is_valid_employment(value): return value.lower() in ['salaried', 'self-employed', 'freelancer']

        if 'name' not in data:
            data['name'] = user_input
            reply = f"Hi {user_input}! How old are you?"
        elif 'age' not in data:
            reply = "What’s your employment type?" if is_valid_number(user_input) else "Please enter a valid age."
            if is_valid_number(user_input): data['age'] = user_input
        elif 'employment_type' not in data:
            reply = "What is your monthly income?" if is_valid_employment(user_input) else "Please enter a valid employment type."
            if is_valid_employment(user_input): data['employment_type'] = user_input.lower()
        elif 'income' not in data:
            reply = "Do you have any existing EMIs or loans?" if is_valid_number(user_input) else "Please enter your income in numbers."
            if is_valid_number(user_input): data['income'] = user_input
        elif 'existing_emis' not in data:
            data['existing_emis'] = user_input
            reply = "What is your credit score?"
        elif 'credit_score' not in data:
            reply = "Which bank do you hold your salary account with?" if is_valid_credit_score(user_input) else "Enter a valid credit score (300–900)."
            if is_valid_credit_score(user_input): data['credit_score'] = user_input
        elif 'bank_name' not in data:
            data['bank_name'] = user_input
            reply = "Do you have a co-applicant? (Yes / No)"
        elif 'co_applicant' not in data:
            data['co_applicant'] = user_input
            reply = "Please enter co-applicant’s monthly income." if user_input.lower() == 'yes' else "What is your PAN number?"
            if user_input.lower() != 'yes':
                data['co_income'] = "N/A"
                data['co_credit_score'] = "N/A"
        elif data.get('co_applicant', '').lower() == 'yes' and 'co_income' not in data:
            reply = "What is co-applicant’s credit score?" if is_valid_number(user_input) else "Enter co-applicant’s income in numbers."
            if is_valid_number(user_input): data['co_income'] = user_input
        elif data.get('co_applicant', '').lower() == 'yes' and 'co_credit_score' not in data:
            reply = "What is your PAN number?" if is_valid_credit_score(user_input) else "Enter a valid credit score (300–900)."
            if is_valid_credit_score(user_input): data['co_credit_score'] = user_input
        elif 'pan_number' not in data:
            data['pan_number'] = user_input
            reply = "What type of loan are you applying for?"
        elif 'loan_type' not in data:
            data['loan_type'] = user_input
            reply = "What is the desired loan amount?"
        elif 'loan_amnt' not in data:
            reply = "What is the preferred tenure in months?" if is_valid_number(user_input) else "Enter loan amount in numbers."
            if is_valid_number(user_input): data['loan_amnt'] = user_input
        elif 'loan_tenure' not in data:
            reply = "Do you have collateral or property to pledge?" if is_valid_number(user_input) else "Enter tenure in months (numbers only)."
            if is_valid_number(user_input): data['loan_tenure'] = user_input
        elif 'collateral' not in data:
            data['collateral'] = user_input
            reply = "Thanks! You can now upload your documents on the dashboard."
        else:
            reply = "You're all set! Head to the dashboard to upload documents and view your eligibility report."

        session.modified = True
        return jsonify({"reply": reply})

    return render_template('chatbot.html')

@app.route('/upload', methods=['POST'])
def upload_docs():
    for field in ['aadhar', 'salary', 'bank']:
        file = request.files.get(field)
        if file:
            folder = os.path.join(app.config['UPLOAD_FOLDER'], field + '_slips' if field == 'salary' else field)
            os.makedirs(folder, exist_ok=True)
            file.save(os.path.join(folder, file.filename))

    loan_data = session.get('loan_data', {})
    result = "Eligible"
    assessment = generate_assessment(loan_data)

    session['loan_result'] = result
    session['loan_assessment'] = assessment
    return redirect('/result')

@app.route('/result')
def result_page():
    result = session.get('loan_result', 'N/A')
    assessment = session.get('loan_assessment', 'No assessment available.')
    return render_template('result.html', result=result, assessment=assessment)

@app.route('/generate_pdf')
def generate_pdf():
    data = session.get('loan_data', {})
    uploaded_files = []

    for field in ['aadhar', 'salary', 'bank']:
        folder = os.path.join(app.config['UPLOAD_FOLDER'], field + '_slips' if field == 'salary' else field)
        if os.path.exists(folder):
            files = os.listdir(folder)
            uploaded_files.extend([f"{field.capitalize()}: {file}" for file in files])

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)
    y = 800

    p.drawString(100, y, "LoanAdvisor Summary Report")
    y -= 30

    for key, value in data.items():
        p.drawString(100, y, f"{key.replace('_', ' ').title()}: {value}")
        y -= 20

    y -= 10
    p.drawString(100, y, "Uploaded Documents:")
    for doc in uploaded_files:
        y -= 20
        p.drawString(120, y, doc)

    y -= 30
    p.drawString(100, y, "Loan Eligibility: Eligible")

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, download_name="LoanAdvisor_Report.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)