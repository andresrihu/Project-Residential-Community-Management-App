from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.message import Message
from flask_app.models.resident import Resident

#---------------------------------
#-------------INBOX---------------
#---------------------------------
@app.route("/inbox")
def inbox():
    if "user_id" not in session:
        flash("Please login or register to gain access!")
        return redirect("/")
    query_data = {
        "id" : session["user_id"]
    }
    logged_resident = Resident.view_one_resident(query_data)
    messages = Message.get_messages(query_data)
    residents = Resident.view_all_residents()
    return render_template("inbox.html", logged_resident = logged_resident, residents=residents, messages=messages )


#---------------------------------
# Render route to process messages
#---------------------------------
@app.route("/send_message", methods=["post"])
def send_message():
    query_data = {
        "sender_id" : request.form["sender_id"],
        "receiver_id" : request.form["receiver_id"],
        "content" : request.form["content"],
    }
    Message.save_message(query_data)
    return redirect("/inbox")

# # Route to delete message

# @app.route("/delete_message/<int:id>")
# def delete(id):
#     query_data = {
#         "id" : id
#     }
#     Message.delete(query_data)
#     return redirect("/wall")