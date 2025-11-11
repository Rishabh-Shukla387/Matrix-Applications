# Matrix-Applications

# Matrix & Path Visualizer

This repository contains two independent educational visualization tools built using **Python**, **Tkinter**, and scientific libraries.

1. **Matrix Visualizer** — demonstrates how **matrix multiplication transforms an image** (rotation, scaling, reflection, shear, translation etc.).
2. **Path Visualizer** — an interactive **graph theory tool** that finds and highlights all paths of a given length `k` using **NetworkX**.

Both are designed for **students and educators** to visually explore mathematical concepts in a hands-on way.

---

## 📁 Project Structure

├── main.py           # Launcher — lets you choose which app to run
├── matrix.py         # Matrix Visualizer (image transformation using matrices)
├── visual.py         # Path Visualizer (graph + adjacency matrix + path finding)
├── image.jpeg        # Sample image used in Matrix Visualizer
├── requirements.txt  # Python dependencies


## Features

### Matrix Visualizer — *"See Math in Motion"*
- Demonstrates how **matrix multiplication** affects an image.
- Apply various transformations:
  - Rotation  
  - Scaling  
  - Reflection  
  - Shearing
  - translation
  - Custom transformation matrices
- Observe real-time visual impact of each transformation.
- Built with:
  - `NumPy` for matrix math  
  - `SciPy` for affine transformations  
  - `Pillow` and `Matplotlib` for image processing and display  
  - `Tkinter` for UI controls

# *Example:* 

Multiplying an image by a rotation matrix rotates it around the origin — helping visualize **linear transformations** from linear algebra.

---

### 🔹 Path Visualizer — *"Explore Graph Connectivity"*
- Create nodes and edges interactively using clicks.
- Supports **Directed** and **Undirected** graphs.
- Computes all **walks of exactly `k` edges**.
- Displays:
  - Adjacency matrix `A`
  - Matrix power `A^k` (showing number of paths of length `k`)
- Highlights valid paths directly on the graph.
- Perfect for teaching **graph theory** and **matrix-based path analysis**.

---

###  Combined Launcher
- Simple Tkinter interface that lets you choose which app to open:
  -  **Matrix Visualizer**
  -  **Path Visualizer**
  -  **Exit**
- Each app runs in its own independent window.
<img width="593" height="458" alt="image" src="https://github.com/user-attachments/assets/30dc8fce-79c0-438e-9887-06202bc36158" />

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Rishabh-Shukla387/Matrix-Applications.git
cd Matrix-Applications
````

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

* **Windows:**

  ```bash
  venv\Scripts\activate
  ```
* **macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

###  Option 1 — Use the Launcher

```bash
python main.py
```

A window will appear asking which app you’d like to launch:

* **Matrix Visualizer**
* **Path Visualizer**

---

###  Option 2 — Run Individually

Run the matrix app:

```bash
python matrix.py
```

Run the graph path visualizer:

```bash
python visual.py
```

---

##  Dependencies

| Package      | Purpose                                   |
| ------------ | ----------------------------------------- |
| `tkinter`    | GUI framework                             |
| `numpy`      | Matrix computations                       |
| `matplotlib` | Image plotting and visualization          |
| `scipy`      | Image transformations (affine operations) |
| `pillow`     | Image processing (load/save)              |
| `networkx`   | Graph representation and path algorithms  |

---

## 💡 Educational Purpose

This project is built for **students, teachers, and learners** who want to *see mathematics in action*.

* Understand **matrix transformations** visually on real images.
* Explore **graph connectivity** and **path counting** through adjacency matrices.
* Strengthen intuition for **linear algebra** and **graph theory** concepts.

Each app is fully interactive — students can experiment live instead of only calculating by hand.

---

## 📚 Example: Rotation Matrix in Action

In linear algebra, a **2D rotation matrix** is:

[
R(\theta) =
\begin{bmatrix}
\cos\theta & -\sin\theta \
\sin\theta & \cos\theta
\end{bmatrix}
]

Applying this matrix to image coordinates rotates the image by angle `θ`.
The **Matrix Visualizer** lets you apply such transformations directly and see the visual result instantly.

---

##  Screenshots

<img width="593" height="458" alt="image" src="https://github.com/user-attachments/assets/256993ff-edb3-4255-9972-65efb8d2f71e" />

<img width="1489" height="846" alt="image" src="https://github.com/user-attachments/assets/282d6f67-f6cf-41a7-b668-6825289ba3b3" />

<img width="1490" height="1087" alt="image" src="https://github.com/user-attachments/assets/6e313daa-63ce-42c1-b409-b1ba59dbb1ee" />

---

##  Author

**Rishabh Shukla**
📧 [[aniketshuklag387@gmail.com](mailto:aniketshuklag387@gmail.com)]
🌐 [GitHub Profile](https://github.com/Rishabh-Shukla387)
---



---

Would you like me to add a short **“Contributing”** section (for students or teachers who might fork your repo and add new transformations or graph features)?
It can make the README look more open-source and classroom-friendly.
