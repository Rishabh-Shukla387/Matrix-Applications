import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import affine_transform
import tkinter as tk
from tkinter import messagebox

# --- Load image ---
try:
    img = np.array(Image.open("image.jpeg"))
except FileNotFoundError:
    print("⚠️ Image not found. Please ensure 'image.jpeg' is in the same folder.")
    exit()

# --- Transformation function ---
def apply_transform(image, M):
    h, w = image.shape[:2]

    # Center coordinates
    cx, cy = w / 2, h / 2

    # Extract rotation/scaling part and translation
    A = M[:2, :2]
    t = M[:2, 2]

    # Adjust for center (move origin to center → apply → move back)
    offset = np.array([cx, cy]) - A @ np.array([cx, cy]) - t

    # Apply to each channel
    transformed = np.zeros_like(image)
    for i in range(3):
        transformed[..., i] = affine_transform(
            image[..., i],
            A,
            offset=offset,
            order=1,
            mode='constant',
            cval=0
        )


    return transformed

# --- Safe environment ---
safe_env = {
    "np": np,
    "sin": lambda d: np.sin(np.deg2rad(d)),
    "cos": lambda d: np.cos(np.deg2rad(d)),
    "pi": np.pi
}

# --- Matplotlib setup ---
plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.imshow(img)
ax1.set_title("Original Image")
ax1.axis("off")

ax2.imshow(img)
ax2.set_title("Transformed Image")
ax2.axis("off")
plt.tight_layout()
plt.pause(0.5)

# --- Tkinter GUI setup ---
root = tk.Tk()
root.title("Matrix Input")

tk.Label(root, text="Enter 2x2 matrix:").grid(row=0, column=0, columnspan=2, pady=5)
matrix_entry = tk.Entry(root, width=40)
matrix_entry.insert(0, "[[1, 0], [0, 1]]")  # Default identity
matrix_entry.grid(row=1, column=0, columnspan=2, padx=10)

tk.Label(root, text="Translation tx:").grid(row=2, column=0)
tx_entry = tk.Entry(root, width=10)
tx_entry.insert(0, "0")
tx_entry.grid(row=2, column=1)

tk.Label(root, text="Translation ty:").grid(row=3, column=0)
ty_entry = tk.Entry(root, width=10)
ty_entry.insert(0, "0")
ty_entry.grid(row=3, column=1)

def update_image():
    try:
        matrix_input = matrix_entry.get()
        tx = float(tx_entry.get())
        ty = float(ty_entry.get())

        M = np.array(eval(matrix_input, safe_env), dtype=float)
        if M.shape != (2, 2):
            messagebox.showerror("Matrix Error", "Matrix must be 2x2.")
            return

        # Build 3x3 matrix with translation
        M_full = np.array([[M[0, 0], M[0, 1], tx],
                           [M[1, 0], M[1, 1], ty],
                           [0, 0, 1]])

        transformed = apply_transform(img, M_full)

        ax2.clear()
        ax2.imshow(transformed)
        ax2.set_title(f"Transformed Image\nMatrix =\n{np.round(M_full, 2)}")
        ax2.axis("off")
        fig.canvas.draw_idle()

    except Exception as e:
        messagebox.showerror("Matrix Error", f"Error: {e}")

tk.Button(root, text="Apply", command=update_image, bg="lightgreen").grid(row=4, column=0, pady=10)
tk.Button(root, text="Exit", command=root.destroy, bg="lightcoral").grid(row=4, column=1, pady=10)
root.mainloop()
