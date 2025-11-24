import re

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from database import close_db, init_db, save_message, get_messages_paginated

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

ADMIN_ENTRIES_PER_PAGE = 10

@app.teardown_appcontext
def teardown_db(error):
    """This will be called by Flask after a request response cycle is handled"""
    close_db(error)


@app.route('/')
def index():
    """Redirect to admin page"""
    return redirect(url_for('admin'))


@app.route('/admin/')
def admin():
    """Render admin page from template"""
    page = int(request.args.get('page', 1))
    data = get_messages_paginated(page, ADMIN_ENTRIES_PER_PAGE)

    return render_template('admin.html',
                           rows=data["rows"],
                           total=data["total"],
                           page=data["page"],
                           total_pages=data["total_pages"],
                           prev_page=data["prev_page"],
                           next_page=data["next_page"])
    

@app.route('/api/messages/', methods=['POST'])
def api_messages():
    """
    REST API endpoint to submit a message.
    Expected JSON body:
    {
        "name": str (1-50 chars and valid name),
        "email": str (max 254 chars and valid email),
        "contact_number": str (exactly 12 digits, e.g. +27812345678 and valid contact number),
        "message": str (1-256 chars)
    }
    """
    # Ensure JSON payload exists
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Invalid JSON payload",
            "details": "Request must contain valid JSON"
        }), 400

    data = request.get_json()

    # Extract and strip fields with defaults
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    contact_number = (data.get('contact_number') or '').strip()
    message = (data.get('message') or '').strip()

    # Collect all validation errors
    errors = {}

    if not name:
        errors["name"] = "Name is required"
    elif len(name) > 50:
        errors["name"] = "Name must not exceed 50 characters"
    elif not re.match(r"^[-()'. a-zA-Z]+$", name):
        errors["email"] = "Name may only contain alphabetical characters, '-', '(', ')', '.' and '''"

    if not email:
        errors["email"] = "Email is required"
    elif len(email) > 254:
        errors["email"] = "Email must not exceed 254 characters"
    elif not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        errors["email"] = "Please provide a valid email address"

    if not contact_number:
        errors["contact_number"] = "Contact number is required"
    elif len(contact_number) != 12:
        errors["contact_number"] = "Contact number must be exactly 12 characters"
    elif not re.match(r"^\+27[1-8][0-9]{8}$", contact_number):
        errors["contact_number"] = "Please provide a valid SA contact number (e.g., +27812345678)"

    if not message:
        errors["message"] = "Message is required"
    elif len(message) > 256:
        errors["message"] = "Message must not exceed 256 characters"

    # If any validation errors, return them all at once
    if errors:
        return jsonify({
            "success": False,
            "error": "Validation failed",
            "details": errors
        }), 400

    # Save to database
    try:
        save_message(name, email, contact_number, message)

        return jsonify({
            "success": True,
            "message": "Thank you! Your message has been received.",
        }), 201

    except Exception as e:
        # Log the actual error (in production, use proper logging)
        print(f"Database error in /api/messages/: {e}")
        
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": "Failed to save message. Please try again later."
        }), 500


if __name__ == '__main__':
    # Initialize DB on startup
    init_db(app)

    app.run(debug=True, port=5175)