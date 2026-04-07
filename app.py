from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 1. Setup the Flask App and allow it to talk to the Frontend (CORS)
app = Flask(__name__)
CORS(app)

# 2. Database Configuration (Creates a file named cmis.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cmis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 3. Define the User Table (Database Schema)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20), default="12345") # Your required default password
    role = db.Column(db.String(20))    # student, faculty, office, management
    attendance = db.Column(db.Integer, default=0)
    team_id = db.Column(db.Integer)    # Max 50 teams constraint

# 4. Information Retrieval (IR) Logic
# This function searches for a student name within the list of users
def retrieve_student_info(query, student_list):
    """Simple IR logic to filter students by name."""
    results = [s for s in student_list if query.lower() in s.name.lower()]
    return results[:10] # Return top 10 matches

# 5. Route: System Home (Prevents the "Not Found" error in browser)
@app.route('/')
def home():
    return "<h1>CMIS Backend is Running!</h1><p>Please open index.html from your frontend folder.</p>"

# 6. Route: Login Logic
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # Logic: Match email and the fixed password '12345'
    user = User.query.filter_by(email=data['email'], password="12345").first()
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "attendance": user.attendance,
            "team_id": user.team_id
        })
    return jsonify({"error": "Invalid Credentials"}), 401

# 7. Route: Update Student Info (Faculty/Management Only)
@app.route('/update_student', methods=['POST'])
def update_student():
    data = request.json
    # Access Control: Only specific roles can edit data
    if data['admin_role'] not in ['faculty', 'management']:
        return jsonify({"error": "Permission Denied: Only Faculty/Management can edit"}), 403
    
    student = User.query.get(data['student_id'])
    if student:
        # Update attendance if provided
        if 'attendance' in data:
            student.attendance = data['attendance']
        db.session.commit()
        return jsonify({"message": f"Successfully updated {student.name}"})
    return jsonify({"error": "Student ID not found"}), 404

# 8. Start the Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Creates the database tables
    app.run(debug=True, port=5000)