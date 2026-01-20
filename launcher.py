from flask import Flask, send_file
import subprocess
import os

app = Flask(__name__)

BASE_DIR = r"C:\coding\DSA"

@app.route("/")
def home():
    return send_file(os.path.join(BASE_DIR, "index.html"))

@app.route("/run/binary")
def run_binary_tree():
    path = os.path.join(BASE_DIR, "programs", "binary_tree.py")
    subprocess.Popen(["python", path])
    return "Binary Tree launched"

@app.route("/run/bst")
def run_bst():
    path = os.path.join(BASE_DIR, "programs", "bst.py")
    subprocess.Popen(["python", path])
    return "BST launched"

@app.route("/run/queue")
def run_queue():
    path = os.path.join(BASE_DIR, "programs", "queue.py")
    subprocess.Popen(["python", path])
    return "Queue launched"

@app.route("/run/parking.2")  # Queue
def run_parking_queue():
    path = os.path.join(BASE_DIR, "programs", "queue.py")
    subprocess.Popen(["python", path])
    return "Queue launched"

@app.route("/run/parking")  # Stack
def run_parking():
    path = os.path.join(BASE_DIR, "programs", "stack.py")
    subprocess.Popen(["python", path])
    return "Stack launched"

@app.route("/run/stack")
def run_stack():
    path = os.path.join(BASE_DIR, "programs", "stack.py")
    subprocess.Popen(["python", path])
    return "Stack launched"

if __name__ == "__main__":
    app.run(port=5000)