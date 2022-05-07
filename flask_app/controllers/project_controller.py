from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.project import Project
from flask_app.models.resident import Resident
from flask_app.models.votes import Vote

#--------------------------------------
# ---------CREATE PROJECT--------------
#--------------------------------------

# Route to view Create form
@app.route("/submit_project")
def create():
    if "user_id" not in session:
        flash("Please login or register to gain access!")
        return redirect("/")

    return render_template("new_project.html")

# Route to process create project form
@app.route("/create_project", methods=["post"])
def creating_project():

    if not Project.validate_project(request.form):
        return redirect("/submit_project")

    form_data = {
        "resident_id" : session["user_id"],
        "name" : request.form["name"],
        "description" : request.form["description"],
    }

    Project.save(form_data)

    return redirect("/all_projects")


#--------------------------------------
# -----------EDIT PROJECT--------------
#--------------------------------------

# Route to view edit page
@app.route("/edit/<int:id>")
def edit_project(id):
    if "user_id" not in session:
        flash("You must login to view this page")
        return redirect("/")

    form_data = {"id" : id}

    project = Project.view_one(form_data)
    print(form_data)

    return render_template("edit_project.html", project=project)

# Route to process Edit form
@app.route("/edit/project/<int:id>", methods=["post"])
def editing_projects(id):

    if not Project.validate_project(request.form):
        return redirect(f"/edit/project/{id}")

    form_data = {
        "id" : id,
        "name" : request.form["name"],
        "description" : request.form["description"]
    }

    Project.edit_project(form_data)
    
    return redirect("/all_projects")

#--------------------------------------
# -----------DELETE PROJECT--------------
#--------------------------------------
# Route to delete project
@app.route("/delete/<int:id>")
def delete_project(id):
    if "user_id" not in session:
        flash("You must login to view this page")
        return redirect("/")

    data = { "id" : id }
    print(data)
    Project.delete_project(data)
    return redirect("/all_projects")

#--------------------------------------
# -----------PROJECT LIST--------------
#--------------------------------------

# route to see all projects with resident info
@app.route("/all_projects")
def show_all_projects():
    if "user_id" not in session:
        flash("You must login to view this page")
        return redirect("/")

    projects = Project.get_projects_with_resident()
    print("********************************************")
    print(projects)
    # projects = Project.view_all()

    return render_template("all_projects.html", projects=projects)

#--------------------------------------
# -----------VOTING PAGE---------------
#--------------------------------------

# Route to view voting form
@app.route("/vote/<int:id>")
def show_one_project(id):
    if "user_id" not in session:
        flash("You must login to view this page")
        return redirect("/")
    
    form_data = { "id" : id }

    project = Project.view_one_with_resident(form_data)

    return render_template("voting.html", project=project)

# Route to update vote for selected project
@app.route("/update/vote/<int:id>", methods=["post"])
def update_votes(id):


    form_data = {
        "id" : id,
        "votes" : int(request.form["votes"]),
        "resident_id" : session["user_id"]
    }
    if not Vote.validate_vote(form_data):
        return redirect("/all_projects")

    Project.update_votes(form_data)
    Vote.save(form_data)
    print("*********Insert into DB***************")
    print(form_data)
    return redirect("/all_projects")