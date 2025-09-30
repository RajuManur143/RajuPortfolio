from flask import Flask, render_template, request, redirect
from email.message import EmailMessage
import smtplib
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sendemail/", methods=["POST"])
def sendemail():
    if request.method == "POST":
        name = request.form["name"]
        subject = request.form["Subject"]
        email = request.form["_replyto"]
        message = request.form["message"]

        # Get credentials from environment variables
        your_email = os.environ.get("EMAIL_USER")
        your_password = os.environ.get("EMAIL_PASS")


        if not your_email or not your_password:
            print("Email credentials are missing!")
            return redirect("/")

        # Set up the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(your_email, your_password)

        # Compose the email
        msg = EmailMessage()
        msg.set_content(
            f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"
        )
        msg["To"] = your_email  # Send the email to yourself
        msg["From"] = your_email
        msg["Subject"] = subject

        # Send the email
        try:
            server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

        server.quit()
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
