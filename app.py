import os
from io import BytesIO
from flask import Flask, render_template, request, redirect, send_file, session, url_for
from werkzeug.utils import secure_filename
import boto3

app = Flask(__name__)

# -----------------------------
# APPLICATION CONFIGURATION
# -----------------------------
# Enforce operational cookies only over encrypted channels (HTTPS)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "prod-secure-fallback-key-override-this")
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

# Extract infrastructure properties cleanly from runtime environment variables
SOURCE_BUCKET = os.environ.get("S3_SOURCE_BUCKET", "your-source-bucket")
DEST_BUCKET = os.environ.get("S3_DEST_BUCKET", "your-destination-bucket")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
PORT_NUMBER = int(os.environ.get("APP_PORT", 5000))

# Secure Credential Intake: Boto3 natively scans standard environment locations:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN
s3 = boto3.client("s3", region_name=AWS_REGION)

# Identity Configurations
USERNAME = os.environ.get("APP_ADMIN_USER", "admin")
PASSWORD = os.environ.get("APP_ADMIN_PASS", "password")

# -----------------------------
# ACCESS CONTROL WRAPPER
# -----------------------------
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_authenticated" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------
# AUTHENTICATION ROUTING
# -----------------------------
@app.route("/")
def login():
    if "user_authenticated" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    user = request.form.get("username", "").strip()
    pwd = request.form.get("password", "")

    if not user or not pwd:
        return "Missing identity inputs", 400

    if user == USERNAME and pwd == PASSWORD:
        session.clear()  # Purge previous cache states to prevent session fixation exploits
        session["user_authenticated"] = user
        return redirect(url_for("home"))
    
    return "Invalid Credentials", 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/home")
@login_required
def home():
    return render_template("index.html")

# -----------------------------
# CORE LOGISTICS LAYER
# -----------------------------
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if "file" not in request.files:
        return "No file payload present", 400

    file = request.files["file"]
    if file.filename == "":
        return "Unselected empty transmission", 400

    if file:
        # Sanitize systemic structural filenames safely via Werkzeug utilities
        filename = secure_filename(file.filename)
        try:
            s3.upload_fileobj(file, SOURCE_BUCKET, filename)
            return "File uploaded successfully!"
        except Exception as e:
            return f"Infrastructure Storage Error: {str(e)}", 500

@app.route("/download", methods=["POST"])
@login_required
def download():
    filename = request.form.get("filename")
    if not filename:
        return "Missing identifier argument", 400
        
    filename = secure_filename(filename)

    try:
        # Optimization: Fetch file down directly into memory buffers via get_object
        s3_object = s3.get_object(Bucket=SOURCE_BUCKET, Key=filename)
        memory_buffer = BytesIO(s3_object["Body"].read())
        
        return send_file(
            memory_buffer,
            download_name=filename,
            as_attachment=True,
            mimetype=s_object.get("ContentType", "application/octet-stream")
        )
    except Exception as e:
        return f"Download Operations Exception: {str(e)}", 500

# -----------------------------
# SERVICE INITIALIZATION
# -----------------------------
if __name__ == "__main__":
    # Multi-threading active for managing concurrency requests cleanly
    app.run(host="0.0.0.0", port=PORT_NUMBER, threaded=True)
