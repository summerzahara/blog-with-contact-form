import os

import requests, smtplib
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)

load_dotenv()

posts = requests.get("https://api.npoint.io/621b9dc89d63826e83a5").json()
sender_email = os.environ["SENDER_EMAIL"]
email_password = os.environ["EMAIL_PASS"]
to_email = os.environ["TO_EMAIL"]


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        print(name, email, phone, message)
        send_email(name, email, phone, message)
        return "<h1>Successfully Submitted!</h1>"


def send_email(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com:587") as connection:
        connection.starttls()
        connection.login(user=sender_email, password=email_password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=sender_email,
            msg=f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        )


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == '__main__':
    app.run()
