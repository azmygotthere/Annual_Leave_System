from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "employees.json"
employees = {}

# Load data from file
def load_data():
    global employees
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            employees = json.load(f)
    else:
        employees = {}

# Save data to file
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(employees, f, indent=4)

# Home page - list employees
@app.route("/")
def index():
    load_data()
    return render_template_string("""
        <h1>Annual Leave Management System</h1>
        <a href="{{ url_for('add_employee') }}">Add Employee</a>
        <table border="1" cellpadding="5" style="margin-top:10px;">
            <tr><th>Employee ID</th><th>Name</th><th>Annual Leave</th><th>Actions</th></tr>
            {% for emp_id, data in employees.items() %}
            <tr>
                <td>{{ emp_id }}</td>
                <td>{{ data['name'] }}</td>
                <td>{{ data['annual_leave'] }}</td>
                <td>
                    <a href="{{ url_for('update_leave', emp_id=emp_id) }}">Take Leave</a> |
                    <a href="{{ url_for('restore_leave', emp_id=emp_id) }}">Restore Leave</a> |
                    <a href="{{ url_for('delete_employee', emp_id=emp_id) }}">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </table>
    """, employees=employees)

# Add employee
@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        emp_id = request.form["emp_id"]
        name = request.form["name"]
        annual_leave = int(request.form["annual_leave"])
        employees[emp_id] = {"name": name, "annual_leave": annual_leave}
        save_data()
        return redirect(url_for("index"))
    return render_template_string("""
        <h2>Add Employee</h2>
        <form method="post">
            Employee ID: <input type="text" name="emp_id"><br>
            Name: <input type="text" name="name"><br>
            Annual Leave Days: <input type="number" name="annual_leave"><br>
            <input type="submit" value="Add">
        </form>
        <a href="{{ url_for('index') }}">Back</a>
    """)

# Delete employee
@app.route("/delete/<emp_id>")
def delete_employee(emp_id):
    if emp_id in employees:
        employees.pop(emp_id)
        save_data()
    return redirect(url_for("index"))

# Update leave (take leave)
@app.route("/update/<emp_id>", methods=["GET", "POST"])
def update_leave(emp_id):
    if request.method == "POST":
        days_taken = int(request.form["days_taken"])
        if emp_id in employees and days_taken <= employees[emp_id]["annual_leave"]:
            employees[emp_id]["annual_leave"] -= days_taken
            save_data()
        return redirect(url_for("index"))
    return render_template_string("""
        <h2>Update Leave for {{ employees[emp_id]['name'] }}</h2>
        <form method="post">
            Days Taken: <input type="number" name="days_taken"><br>
            <input type="submit" value="Update">
        </form>
        <a href="{{ url_for('index') }}">Back</a>
    """, emp_id=emp_id, employees=employees)

# Restore leave (grant extra days)
@app.route("/restore/<emp_id>", methods=["GET", "POST"])
def restore_leave(emp_id):
    if request.method == "POST":
        days_added = int(request.form["days_added"])
        if emp_id in employees:
            employees[emp_id]["annual_leave"] += days_added
            save_data()
        return redirect(url_for("index"))
    return render_template_string("""
        <h2>Restore Leave for {{ employees[emp_id]['name'] }}</h2>
        <form method="post">
            Days Added: <input type="number" name="days_added"><br>
            <input type="submit" value="Restore">
        </form>
        <a href="{{ url_for('index') }}">Back</a>
    """, emp_id=emp_id, employees=employees)

if __name__ == "__main__":
    load_data()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=10000)



