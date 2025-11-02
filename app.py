import os
from flask import Flask, request, send_from_directory

BUILD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "build")   # <— root/build
)
app = Flask(__name__, static_folder=BUILD_DIR, static_url_path="/")



# ------------------ HW5 Task 1 endpoints ------------------

@app.get("/api/health")
def health():
    return jsonify(status="ok")

@app.get("/api/joinProject")
def join_project():
    project_id = request.args.get("projectId")
    if not project_id:
        return "Missing projectId", 400, {"Content-Type": "text/plain"}
    msg = f"Joined {project_id}"
    # Return plain text if your rubric requires it; swap to jsonify if JSON is okay
    return msg, 200, {"Content-Type": "text/plain"}

@app.get("/api/leaveProject")
def leave_project():
    project_id = request.args.get("projectId")
    if not project_id:
        return "Missing projectId", 400, {"Content-Type": "text/plain"}
    msg = f"Left {project_id}"
    return msg, 200, {"Content-Type": "text/plain"}

@app.get("/api/checkOut_hardware")
def check_out_hardware():
    project_id = request.args.get("projectId")
    qty = request.args.get("qty")
    if not project_id or qty is None:
        return "Missing projectId or qty", 400, {"Content-Type": "text/plain"}
    try:
        qty_int = int(qty)
    except ValueError:
        return "qty must be an integer", 400, {"Content-Type": "text/plain"}
    msg = f"{qty_int} hardware checked out"
    return msg, 200, {"Content-Type": "text/plain"}

@app.get("/api/checkIn_hardware")
def check_in_hardware():
    project_id = request.args.get("projectId")
    qty = request.args.get("qty")
    if not project_id or qty is None:
        return "Missing projectId or qty", 400, {"Content-Type": "text/plain"}
    try:
        qty_int = int(qty)
    except ValueError:
        return "qty must be an integer", 400, {"Content-Type": "text/plain"}
    msg = f"{qty_int} hardware checked in"
    return msg, 200, {"Content-Type": "text/plain"}

# ------------------ Static React build ------------------

@app.get("/")
def index():
    # Serve index.html from the build folder
    return send_from_directory(app.static_folder, "index.html")

@app.get("/<path:path>")
def static_proxy(path):
    # Serve static assets or fall back to index.html for client-side routing
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    # 0.0.0.0 so it binds for deployment/containers; port 5000 by default
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
