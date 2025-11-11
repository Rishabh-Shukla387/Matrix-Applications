"""
visual_graph_k_length.py
Click-based visual graph maker that finds all simple paths with exactly k edges.
Uses tkinter for UI and networkx for graph operations.

How to use:
- Choose Directed or Undirected.
- Click "Add Node" then click on canvas to place nodes (or use auto-add mode).
- To add an edge: click a node (it will be highlighted as source), then click a second node as target.
  A popup will ask for weight (optional, numeric). Press Cancel to use default weight=1.
- Enter target path length k (integer) and press "Find paths". Results will be shown and matching
  paths highlighted.
- "Clear highlights" removes highlighting.
- "Reset" clears graph.
"""
import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import numpy as np
import math

NODE_RADIUS = 18
FONT = ("Arial", 10)

class VisualGraphApp:
    def __init__(self, root):
        self.root = root
        root.title("Visual Graph Maker — Paths of single length (k)")
        self.directed = tk.BooleanVar(value=False)
        self.node_mode = tk.BooleanVar(value=True)  # if True, clicking canvas adds node
        self.node_labels_auto = tk.BooleanVar(value=True)

        # Graph data
        # self.G = nx.DiGraph() 
        self.G = nx.Graph() if not self.directed.get() else nx.DiGraph()

        self.node_positions = {}  # node -> (x, y)
        self.node_ids = []  # ordering used for auto-naming
        self.node_widgets = {}  # node -> canvas id for circle
        self.text_widgets = {}  # node -> canvas id for label
        self.edge_widgets = {}  # (u,v) -> canvas id for line (u->v or undirected)
        self.selected_node = None  # node clicked to start an edge
        self.highlight_widgets = []  # list of canvas ids used for highlighting

        self._build_ui()

    def _show_adjacency_matrix(self, k):
            
    # Build and display adjacency matrix and its k-th power.
        nodes = sorted(self.G.nodes())
        n = len(nodes)
        if n == 0:
            return

        # --- Build adjacency matrix ---
        A = np.zeros((n, n), dtype=int)
        for i, u in enumerate(nodes):
            for j, v in enumerate(nodes):
                if self.G.has_edge(u, v):
                    A[i, j] = 1  # treat as 1 for connectivity (ignore weight)

        # --- Compute A^k for path counts ---
        Ak = np.linalg.matrix_power(A, k)

        # --- Prepare display text ---
        matrix_str = f"\nAdjacency Matrix (A):\n"
        matrix_str += "   " + " ".join(f"{v:>3}" for v in nodes) + "\n"
        for i, u in enumerate(nodes):
            row = " ".join(f"{A[i,j]:>3}" for j in range(n))
            matrix_str += f"{u:>3} {row}\n"

        matrix_str += f"\nA^{k} (Number of paths of length {k}):\n"
        matrix_str += "   " + " ".join(f"{v:>3}" for v in nodes) + "\n"
        for i, u in enumerate(nodes):
            row = " ".join(f"{Ak[i,j]:>3}" for j in range(n))
            matrix_str += f"{u:>3} {row}\n"

        # --- Show in result box ---
        self.result_box.config(state=tk.NORMAL)           # make text box editable
        self.result_box.insert(tk.END, matrix_str)        # insert the matrix text
        self.result_box.see(tk.END)                       # auto-scroll to the bottom
        self.result_box.config(state=tk.DISABLED)          # lock the text box again



    def _build_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        tk.Label(toolbar, text="Graph type:").pack(side=tk.LEFT)
        tk.Radiobutton(toolbar, text="Undirected", variable=self.directed, value=False, command=self._switch_graph).pack(side=tk.LEFT)
        tk.Radiobutton(toolbar, text="Directed", variable=self.directed, value=True, command=self._switch_graph).pack(side=tk.LEFT)

        tk.Checkbutton(toolbar, text="Click-to-add node", variable=self.node_mode).pack(side=tk.LEFT, padx=8)
        tk.Checkbutton(toolbar, text="Auto-label (A, B, C...)", variable=self.node_labels_auto).pack(side=tk.LEFT)

        tk.Button(toolbar, text="Reset", command=self.reset_graph).pack(side=tk.RIGHT, padx=4)
        tk.Button(toolbar, text="Clear highlights", command=self.clear_highlights).pack(side=tk.RIGHT, padx=4)

        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=6)

        tk.Label(control_frame, text="Target length k (edges):").pack(side=tk.LEFT)
        self.k_entry = tk.Entry(control_frame, width=6)
        self.k_entry.pack(side=tk.LEFT, padx=6)
        self.k_entry.insert(0, "2")

        tk.Button(control_frame, text="Find paths of length k", command=self.find_paths_k).pack(side=tk.LEFT, padx=6)

        # ---- Scrollable + expandable results area ----
        result_frame = tk.Frame(self.root)
        # result_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_box = tk.Text(
            result_frame,
            height=8,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10)
        )
        self.result_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.result_box.yview)

        # Canvas area
        split_frame = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        split_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Left side: canvas area
        canvas_frame = tk.Frame(split_frame)
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        split_frame.add(canvas_frame, stretch="always")
        self.canvas.bind("<Button-1>", self.canvas_click)


        # Right side: results area with scrollbar
        result_frame = tk.Frame(split_frame)
        scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_box = tk.Text(
            result_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
        )
        self.result_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_box.yview)
        split_frame.add(result_frame, stretch="always")

        # Add instructions
        inst = (
            "Instructions:\n"
            "- Click to add nodes (if Click-to-add node is checked).\n"
            "- To add edge: click a node to select it (highlighted), then click another node.\n"
            "- A dialog will ask for weight (optional). Cancel => weight=1.\n"
            "- Paths of length k (edges) are shown on the right."
        )
        self.result_box.insert(tk.END, inst)
        self.result_box.config(state=tk.DISABLED)


    def _switch_graph(self):
        # reinitialize graph type preserving nodes and edges
        if self.directed.get():
            H = nx.DiGraph()
        else:
            H = nx.Graph()
        H.add_nodes_from(self.G.nodes(data=True))
        H.add_edges_from(self.G.edges(data=True))
        self.G = H
        # redraw edges (arrow style only visual)
        self.redraw_all()

    def reset_graph(self):
        self.G.clear()
        self.node_positions.clear()
        self.node_ids.clear()
        self.node_widgets.clear()
        self.text_widgets.clear()
        self.edge_widgets.clear()
        self.selected_node = None
        self.clear_highlights()
        self.canvas.delete("all")
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        inst = (
            "Instructions:\n"
            "- Click to add nodes (if Click-to-add node is checked).\n"
            "- To add edge: click a node to select it (highlighted), then click another node.\n"
            "- A dialog will ask for weight (optional). Cancel => weight=1.\n"
            "- Paths of length k (edges) are shown on the right."
        )
        self.result_box.insert(tk.END, inst)
        self.result_box.config(state=tk.DISABLED)
       
    def canvas_click(self, event):
        x, y = event.x, event.y
        clicked = self._node_at_point(x, y)
        if self.node_mode.get():
            # If clicked on a node, start edge creation; otherwise add a new node
            if clicked:
                # if first click select node to add edge
                if self.selected_node is None:
                    self.select_node(clicked)
                else:
                    # add edge between selected_node and clicked
                    self.add_edge(self.selected_node, clicked)
                    self.unselect_node(self.selected_node)
                    self.selected_node = None
            else:
                # add new node at this position
                self.add_node_at(x, y)
        else:
            # not in add-node click mode: used to create edges by selecting nodes
            if clicked:
                if self.selected_node is None:
                    self.select_node(clicked)
                else:
                    self.add_edge(self.selected_node, clicked)
                    self.unselect_node(self.selected_node)
                    self.selected_node = None

    # ---------------- Node / Edge creation ----------------
    def _node_at_point(self, x, y):
        for node, (nx_, ny_) in self.node_positions.items():
            if (x - nx_)**2 + (y - ny_)**2 <= (NODE_RADIUS+2)**2:
                return node
        return None

    def add_node_at(self, x, y, name=None):
        if name is None and self.node_labels_auto.get():
            name = self._next_auto_label()
        elif name is None:
            # ask for name
            name = simpledialog.askstring("Node name", "Enter node name (leave blank for auto):")
            if not name:
                name = self._next_auto_label()
        if name in self.G.nodes():
            messagebox.showerror("Duplicate node", f"Node '{name}' already exists.")
            return
        self.G.add_node(name)
        self.node_positions[name] = (x, y)
        cid = self.canvas.create_oval(x-NODE_RADIUS, y-NODE_RADIUS, x+NODE_RADIUS, y+NODE_RADIUS,
                                      fill="lightgray", outline="black", width=2)
        tid = self.canvas.create_text(x, y, text=str(name), font=FONT)
        self.node_widgets[name] = cid
        self.text_widgets[name] = tid
        self.node_ids.append(name)

    def _next_auto_label(self):
        # Auto generate A, B, C, ..., Z, AA, AB ...
        n = len(self.node_ids)
        label = ""
        while True:
            label = ""
            t = n
            while True:
                label = chr(65 + (t % 26)) + label
                t = t // 26 - 1
                if t < 0:
                    break
            if label not in self.G.nodes():
                return label
            n += 1

    def select_node(self, node):
        self.selected_node = node
        # visually indicate selection
        cid = self.node_widgets.get(node)
        if cid:
            self.canvas.itemconfig(cid, outline="blue", width=3)

    def unselect_node(self, node):
        cid = self.node_widgets.get(node)
        if cid:
            self.canvas.itemconfig(cid, outline="black", width=2)
        self.selected_node = None

    def add_edge(self, u, v):
        if u == v:
            # no self-edge handling currently (could be allowed)
            if not messagebox.askyesno("Self-loop", "Create self-loop?"):
                return
        # get weight
        w = simpledialog.askstring("Edge weight", f"Enter weight for edge {u} -> {v} (default 1):")
        if w is None:
            weight = 1.0
        else:
            try:
                weight = float(w) if w.strip() != "" else 1.0
            except ValueError:
                messagebox.showwarning("Invalid", "Weight not numeric, using 1")
                weight = 1.0
        # add to networkx graph
        if self.directed.get():
            self.G.add_edge(u, v, weight=weight)
        else:
            # for undirected, use ordered tuple key for widgets
            self.G.add_edge(u, v, weight=weight)
        self._draw_edge(u, v)

    def _draw_edge(self, u, v):
        # Remove existing line for this pair (if any) and redraw to update weights
        key = (u, v)
        if key in self.edge_widgets:
            self.canvas.delete(self.edge_widgets[key])
            del self.edge_widgets[key]

        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]

        # compute simple offset so line doesn't touch circle centers (draw from circle boundary)
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy) or 1.0
        ux = dx / dist
        uy = dy / dist
        start_x = x1 + ux * NODE_RADIUS
        start_y = y1 + uy * NODE_RADIUS
        end_x = x2 - ux * NODE_RADIUS
        end_y = y2 - uy * NODE_RADIUS

        # draw line
        if self.directed.get():
            # draw with arrow
            line = self.canvas.create_line(start_x, start_y, end_x, end_y,
                                           width=2, arrow=tk.LAST, arrowshape=(12, 16, 6))
        else:
            line = self.canvas.create_line(start_x, start_y, end_x, end_y, width=2)

        self.edge_widgets[key] = line

        # draw weight label near midpoint
        midx = (start_x + end_x) / 2
        midy = (start_y + end_y) / 2
        # remove previous weight text if any (search and delete)
        # We'll create a small text; tag it for later removal
        w = self.G[u][v].get("weight", "")
        tagid = f"w_{u}_{v}"
        # delete prior text if exists
        for item in self.canvas.find_withtag(tagid):
            self.canvas.delete(item)
        self.canvas.create_text(midx, midy-8, text=str(w), font=("Arial", 9), tags=(tagid,))

    def redraw_all(self):
        self.canvas.delete("all")
        self.edge_widgets.clear()
        # draw edges first so nodes on top
        for (u, v, data) in self.G.edges(data=True):
            # ensure positions exist; if not, place randomly
            if u not in self.node_positions:
                self.node_positions[u] = (50 + 30 * len(self.node_positions), 50)
            if v not in self.node_positions:
                self.node_positions[v] = (70 + 30 * len(self.node_positions), 90)
            self._draw_edge(u, v)
        # draw nodes
        self.node_widgets.clear()
        self.text_widgets.clear()
        for node, (x, y) in self.node_positions.items():
            cid = self.canvas.create_oval(x-NODE_RADIUS, y-NODE_RADIUS, x+NODE_RADIUS, y+NODE_RADIUS,
                                          fill="lightgray", outline="black", width=2)
            tid = self.canvas.create_text(x, y, text=str(node), font=FONT)
            self.node_widgets[node] = cid
            self.text_widgets[node] = tid

    # ---------------- Path finding ----------------
    def find_paths_k(self):
        k_str = self.k_entry.get().strip()
        try:
            k = int(k_str)
            if k < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid k", "Please enter a non-negative integer for k.")
            return

        self.clear_highlights()
        all_paths = []
        nodes = list(self.G.nodes())

        # Generate all walks (can revisit nodes)
        for start in nodes:
            self._dfs_walks_exact_k(start, k, [start], all_paths)

        # Group by start→end
        grouped = {}
        for p in all_paths:
            start, end = p[0], p[-1]
            grouped.setdefault((start, end), []).append("".join(p))

        # Sort by start node, then end node
        sorted_keys = sorted(grouped.keys())

        # Display results
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, f"All walks (paths may repeat nodes) of length {k}:\n\n")
        total_count = 0
        for (s, e) in sorted_keys:
            paths_list = ", ".join(sorted(grouped[(s, e)]))
            total_count += len(grouped[(s, e)])
            self.result_box.insert(tk.END, f"{s} → {e}: {paths_list}\n")
        if not total_count:
            self.result_box.insert(tk.END, "(none)\n")
        self.result_box.config(state=tk.DISABLED)

        # Highlight all unique edge pairs used
        self._highlight_paths(all_paths)
        self._show_adjacency_matrix(k)


    def _dfs_walks_exact_k(self, current, remain_k, path, collector):
        """DFS for all walks (nodes may repeat) of exactly k edges."""
        if remain_k == 0:
            collector.append(list(path))
            return
        for nbr in self.G.neighbors(current):
            path.append(nbr)
            self._dfs_walks_exact_k(nbr, remain_k - 1, path, collector)
            path.pop()


    def _report_paths(self, paths, k):
        self.result_box.config(state=tk.NORMAL)
        self.result_box.config(state=tk.DISABLED)
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, f"Found {len(paths)} paths of length {k}:\n\n")
        for p in paths:
            self.result_box.insert(tk.END, " → ".join(p) + "\n")
        if not paths:
            self.result_box.insert(tk.END, "(none)\n")
        self.result_box.config(state=tk.DISABLED)

    def _highlight_paths(self, paths):
        # draw highlighted overlays on top of existing edges for each path
        for p in paths:
            if len(p) < 2:
                # single node path => highlight node
                node = p[0]
                x,y = self.node_positions[node]
                circ = self.canvas.create_oval(x-NODE_RADIUS-4, y-NODE_RADIUS-4, x+NODE_RADIUS+4, y+NODE_RADIUS+4,
                                               outline="green", width=3)
                self.highlight_widgets.append(circ)
                continue
            for i in range(len(p)-1):
                u = p[i]; v = p[i+1]
                # compute coordinates and draw a bold colored line on top
                x1,y1 = self.node_positions[u]; x2,y2 = self.node_positions[v]
                dx = x2-x1; dy = y2-y1
                dist = math.hypot(dx,dy) or 1.0
                ux = dx/dist; uy = dy/dist
                sx = x1 + ux*NODE_RADIUS; sy = y1 + uy*NODE_RADIUS
                ex = x2 - ux*NODE_RADIUS; ey = y2 - uy*NODE_RADIUS
                hl = self.canvas.create_line(sx, sy, ex, ey, width=6, fill="green", stipple="gray50")
                self.highlight_widgets.append(hl)

    def clear_highlights(self):
        for wid in self.highlight_widgets:
            try:
                self.canvas.delete(wid)
            except Exception:
                pass
        self.highlight_widgets.clear()

# ---------------- Run ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualGraphApp(root)
    root.geometry("1000x700")
    root.mainloop()
