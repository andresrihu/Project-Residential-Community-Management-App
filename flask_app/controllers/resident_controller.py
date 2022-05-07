from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.resident import Resident
from flask_app.models.house import House

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#--------------------------------------
# -----------LOGIN PAGE----------------
#--------------------------------------

# Route to show form
@app.route("/")
def index():
    houses = House.show_all()
    return render_template("loginReg.html", houses=houses)

#--------------------------------------
# -----------REGISTRATION--------------
#--------------------------------------

# Route to validate and process registration form
@app.route("/register", methods=["post"])
def register():
    #1 validate information:
    if not Resident.validate_registration(request.form):
        return redirect("/")
    
    #2 create hash for password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    #3 process form_data:
    form_data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "house_id" : request.form["house_id"],
        "password" : pw_hash,
        "about" : request.form["about"]
    }
    # 4 send form_data to run query into DB and add user id to sesh
    user_id = Resident.save(form_data)
    session["user_id"] = user_id
    session["first_name"] = request.form["first_name"]
    print(user_id)
    print(session["first_name"])
    

    # 5 redirect
    return redirect("/dashboard")

#--------------------------------------
# --------------LOGIN------------------
#--------------------------------------
# Route to validate and process login
@app.route("/login", methods=["post"])
def validate_login():
    # 1 validate information:
    if not Resident.validate_login(request.form):
        return redirect("/")

    # 2 query based on data received
    form_data = {
        "email" : request.form["email"]
    }
    user_in_db = Resident.get_user_by_email(form_data)
    
    # 3 Put information in sesh
    session["user_id"] = user_in_db.id
    print(user_in_db.id)
    session["first_name"] = user_in_db.first_name
    print(user_in_db.first_name)
    session["last_name"] = user_in_db.last_name

    # 4 redirect
    return redirect("/dashboard")


#--------------------------------------
# -------------DASHBOARD---------------
#--------------------------------------

# Route to view dashboard
@app.route("/dashboard")
def dashboard():
    # 1 check if user is logged in and kick out if not
    if "user_id" not in session:
        flash("Please login or register to gain access!")
        return redirect("/")

    houses = House.show_all()

    return render_template("dashboard.html", houses=houses)

#--------------------------------------
# ------------MY DASHBOARD-------------
#--------------------------------------

# Route to show form
@app.route("/my_dash")
def my_dashboard():

    data = { "id" : session["user_id"] }

    resident = Resident.view_one_with_house(data)

    return render_template("my_dash.html", resident=resident)

#--------------------------------------
# --------RESIDENT PROFILE-------------
#--------------------------------------

# Route to show form
@app.route("/resident/<int:id>")
def show_residents(id):

    form_data = { "id" : id }

    house = House.view_one_with_resident(form_data)

    return render_template("resident_profile.html", house=house)

#--------------------------------------
# ------------EDIT PROFILE-------------
#--------------------------------------

# Route to show form
@app.route("/edit/profile/<int:id>")
def edit_resident(id):

    form_data = { "id" : id }

    resident = Resident.view_one_with_house(form_data)

    return render_template("edit_profile.html", resident=resident)

# Route to process edit form
@app.route("/edit/profile/<int:id>", methods=["post"])
def editing_resident(id):

    if not Resident.validate_edit_resident(request.form):
        return redirect(f"/edit/profile/{id}")


    form_data = {
        "id" : id,
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "resident_since" : request.form["resident_since"],
        "phone_number" : request.form["phone_number"],
        "role" : request.form["role"],
        "about" : request.form["about"]
    }
    
    Resident.edit_resident(form_data)
    
    return redirect("/my_dash")

#--------------------------------------
# -------MAINTENANCE PAGE--------------
#--------------------------------------

# Route to show form
@app.route("/maintenance")
def maintenance():
    return render_template("maintenance.html")

#--------------------------------------
# ----------FINANCES PAGE--------------
#--------------------------------------

# Route to show form
@app.route("/finances")
def finance():
    return render_template("finances.html")


#--------------------------------------
# -------LOGOUT & CLEAR SESH-----------
#--------------------------------------

# Route to logout and clear session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")