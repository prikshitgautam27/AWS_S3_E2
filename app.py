from flask import Flask, render_template, request, redirect, send_file
import boto3
import os

app = Flask(__name__)

# -----------------------------
# AWS CONFIG (PLACEHOLDERS)
# -----------------------------
AWS_ACCESS_KEY = "YOUR_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_SECRET_KEY"
AWS_REGION = "YOUR_REGION"

SOURCE_BUCKET = "your-source-bucket"
DEST_BUCKET = "your-destination-bucket"

# S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# -----------------------------
# SIMPLE LOGIN
# -----------------------------
USERNAME = "admin"
PASSWORD = "password"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    user = request.form["username"]
    pwd = request.form["password"]

    if user == USERNAME and pwd == PASSWORD:
        return redirect("/home")
    else:
        return "Invalid Credentials"

@app.route("/home")
def home():
    return render_template("index.html")

# -----------------------------
# FILE UPLOAD
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filename = file.filename

    s3.upload_fileobj(file, SOURCE_BUCKET, filename)

    return "File uploaded successfully!"

# -----------------------------
# FILE DOWNLOAD
# -----------------------------
@app.route("/download", methods=["POST"])
def download():
    filename = request.form["filename"]

    s3.download_file(SOURCE_BUCKET, filename, filename)

    return send_file(filename, as_attachment=True)

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT_NUMBER)
