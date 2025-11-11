import tkinter as tk
import subprocess
import sys
import os
import tempfile
import shutil

def run_embedded(script_name):
    """Run a bundled Python script safely when frozen with PyInstaller."""
    # Determine path of bundled or source file
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    script_src = os.path.join(base_path, script_name)

    # Copy to a temp directory, because PyInstaller bundles files as read-only
    temp_dir = tempfile.mkdtemp()
    script_temp = os.path.join(temp_dir, script_name)
    shutil.copy(script_src, script_temp)

    # Launch the script using the same interpreter
    subprocess.Popen([sys.executable, script_temp])

def run_matrix():
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    script_path = os.path.join(base_path, "matrix.py")
    subprocess.Popen([sys.executable, script_path])
    root.destroy()

def run_path():
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    script_path = os.path.join(base_path, "visual_graph_k_length.py")
    subprocess.Popen([sys.executable, script_path])
    root.destroy()


# --- GUI ---
root = tk.Tk()
root.title("Matrix Applications")
root.geometry("400x280")
root.configure(bg="#f0f0f0")

tk.Label(
    root, text="Choose Application to Launch",
    font=("Arial", 16, "bold"), bg="#f0f0f0"
).pack(pady=20)

tk.Button(
    root, text="🧮  Matrix Visualizer",
    font=("Arial", 13), bg="#4285F4", fg="white",
    width=22, height=2, command=run_matrix
).pack(pady=10)

tk.Button(
    root, text="🌐  Path Visualizer",
    font=("Arial", 13), bg="#34A853", fg="white",
    width=22, height=2, command=run_path
).pack(pady=10)

tk.Button(
    root, text="❌  Exit",
    font=("Arial", 11), bg="#EA4335", fg="white",
    width=10, command=root.destroy
).pack(pady=15)

root.mainloop()
