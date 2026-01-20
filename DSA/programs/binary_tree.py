import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from collections import deque

class Node:
    def __init__(self, x=0, y=0):
        self.value = None
        self.left = None
        self.right = None
        self.x = x
        self.y = y

def create_empty_tree(levels):
    if levels <= 0:
        return None
    root = Node()
    queue = deque([root])
    for _ in range(levels - 1):
        for _ in range(len(queue)):
            cur = queue.popleft()
            cur.left = Node()
            cur.right = Node()
            queue.append(cur.left)
            queue.append(cur.right)
    return root

# Traversal Logic
def inorder(node, result):
    if node:
        inorder(node.left, result)
        if node.value is not None: result.append(node.value)
        inorder(node.right, result)

def preorder(node, result):
    if node:
        if node.value is not None: result.append(node.value)
        preorder(node.left, result)
        preorder(node.right, result)

def postorder(node, result):
    if node:
        postorder(node.left, result)
        postorder(node.right, result)
        if node.value is not None: result.append(node.value)

class TreeApp:
    def __init__(self, levels, min_val, max_val):
        self.root_node = create_empty_tree(levels)
        self.levels = levels
        self.min_val = min_val
        self.max_val = max_val
        self.node_radius = 22
        
        # Color Palette
        self.bg_dark = "#1e1e2e"
        self.bg_panel = "#2b2b3b"
        self.accent = "#5865f2"
        self.node_color = "#3d5afe"
        self.text_color = "#ffffff"

        self.win = tk.Tk()
        self.win.title("DSA Binary Tree Visualizer")
        self.win.geometry("1100x750") # Increased height slightly
        self.win.configure(bg=self.bg_dark)

        # UI Layout: Main Canvas and Side Control Panel
        self.canvas = tk.Canvas(self.win, width=800, height=750, bg=self.bg_dark, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.win, width=300, bg=self.bg_panel, padx=20, pady=20)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sidebar.pack_propagate(False) # Prevent sidebar from shrinking

        self.setup_sidebar()
        self.draw_tree()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        self.write_log("System initialized.")
        self.write_log(f"Range: {self.min_val} - {self.max_val}")
        
        self.win.mainloop()

    def setup_sidebar(self):
        # Header
        tk.Label(self.sidebar, text="CONTROLS", font=("Segoe UI", 14, "bold"), 
                 bg=self.bg_panel, fg=self.accent).pack(pady=(0, 10))

        # Instructions
        instr = "Left Click: Add Value\nRight Click: Clear Node"
        tk.Label(self.sidebar, text=instr, font=("Segoe UI", 9), bg=self.bg_panel, 
                 fg="#a0a0a0", justify=tk.CENTER).pack(pady=(0, 20))

        # Traversal Buttons
        self.add_side_button("Inorder (LTR)", self.show_inorder)
        self.add_side_button("Preorder (TLR)", self.show_preorder)
        self.add_side_button("Postorder (LRT)", self.show_postorder)
        
        tk.Frame(self.sidebar, height=2, bg="#444").pack(fill=tk.X, pady=15)

        # BST Operations
        self.add_side_button("BST Auto-Insert", self.bst_insert_prompt, color="#43a047")
        
        tk.Frame(self.sidebar, height=2, bg="#444").pack(fill=tk.X, pady=15)

        # --- LOGGING AREA ---
        tk.Label(self.sidebar, text="System Logs", font=("Segoe UI", 10, "bold"), 
                 bg=self.bg_panel, fg=self.accent).pack(anchor="w", pady=(0, 5))
        
        self.log_area = scrolledtext.ScrolledText(self.sidebar, height=15, 
                                                 bg="#181825", fg="#a6accd", 
                                                 font=("Consolas", 9), relief=tk.FLAT)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.configure(state='disabled')

    def add_side_button(self, text, command, color=None):
        btn = tk.Button(self.sidebar, text=text, command=command, 
                        bg=color if color else self.accent, fg="white", 
                        font=("Segoe UI", 10, "bold"), relief=tk.FLAT, 
                        padx=10, pady=8, cursor="hand2")
        btn.pack(fill=tk.X, pady=5)

    def write_log(self, message):
        """Adds a message to the sidebar log area."""
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, f"> {message}\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')
        print(message) # Keep terminal output as backup

    def draw_tree(self):
        levels = self.get_levels(self.root_node)
        spacing_y = 120
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 100: canvas_width = 800

        for depth, nodes in enumerate(levels):
            spacing_x = canvas_width // (len(nodes) + 1)
            for i, node in enumerate(nodes):
                node.x = (i + 1) * spacing_x
                node.y = (depth + 1) * spacing_y

        self.canvas.delete("all")
        self.draw_connections(self.root_node)
        self.draw_nodes(self.root_node)
        
    def check_duplicate(self, node, value):
        """Recursively checks if a value exists anywhere in the tree."""
        if not node: 
            return False
        if node.value == value: 
            return True
        return self.check_duplicate(node.left, value) or self.check_duplicate(node.right, value)

    def get_levels(self, root):
        levels = []
        if not root: return levels
        queue = deque([(root, 0)])
        while queue:
            node, lvl = queue.popleft()
            if lvl == len(levels): levels.append([])
            levels[lvl].append(node)
            if node.left: queue.append((node.left, lvl+1))
            if node.right: queue.append((node.right, lvl+1))
        return levels

    def draw_connections(self, node):
        if not node: return
        line_settings = {"fill": "#44475a", "width": 2}
        if node.left:
            self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, **line_settings)
            self.draw_connections(node.left)
        if node.right:
            self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, **line_settings)
            self.draw_connections(node.right)

    def draw_nodes(self, node):
        if not node: return
        r = self.node_radius
        # Shadow effect
        self.canvas.create_oval(node.x-r+2, node.y-r+2, node.x+r+2, node.y+r+2, fill="#000000", outline="")
        # Main Node
        self.canvas.create_oval(node.x-r, node.y-r, node.x+r, node.y+r, fill=self.node_color, outline=self.text_color)
        
        text = str(node.value) if node.value is not None else "?"
        self.canvas.create_text(node.x, node.y, text=text, fill=self.text_color, font=("Segoe UI", 11, "bold"))
        
        self.draw_nodes(node.left)
        self.draw_nodes(node.right)

    def on_click(self, event):
        clicked_node = self.find_clicked_node(self.root_node, event.x, event.y)
        
        if clicked_node:
            # Get input from user
            value = simpledialog.askinteger("Input", f"Enter ({self.min_val}-{self.max_val}):")
            
            if value is not None:
                # 1. Check Range
                if not (self.min_val <= value <= self.max_val):
                    self.write_log(f"Error: {value} is out of range")
                    messagebox.showerror("Error", "Out of range")
                    return

                # 2. Check Duplicates (Skip check if user entered the same number that was already there)
                if value != clicked_node.value and self.check_duplicate(self.root_node, value):
                    self.write_log(f"Error: {value} already exists!")
                    messagebox.showwarning("Duplicate", f"The value {value} is already in the tree.")
                    return

                # 3. Success - Update Node
                prev_val = clicked_node.value
                clicked_node.value = value
                self.write_log(f"Manual Update: Changed {prev_val} to {value}")
                self.draw_tree()

    def on_right_click(self, event):
        clicked_node = self.find_clicked_node(self.root_node, event.x, event.y)
        if clicked_node:
            prev_val = clicked_node.value
            clicked_node.value = None
            self.write_log(f"Cleared Node (was {prev_val})")
            self.draw_tree()

    def find_clicked_node(self, node, x, y):
        if not node: return None
        if (node.x-25 <= x <= node.x+25) and (node.y-25 <= y <= node.y+25):
            return node
        return self.find_clicked_node(node.left, x, y) or self.find_clicked_node(node.right, x, y)

    def bst_insert(self, node, value):
        if node.value is None:
            node.value = value
            return True
        if value == node.value: return False
        if value < node.value:
            return self.bst_insert(node.left, value) if node.left else False
        else:
            return self.bst_insert(node.right, value) if node.right else False

    def bst_insert_prompt(self):
        val = simpledialog.askinteger("BST Insert", "Value:")
        if val is not None:
            if self.min_val <= val <= self.max_val:
                if self.bst_insert(self.root_node, val):
                    self.write_log(f"BST Inserted: {val}")
                    self.draw_tree()
                else:
                    self.write_log(f"Insert Failed: {val} (Duplicate or No Space)")
                    messagebox.showwarning("Warning", "Could not insert (Duplicate or no space)")
            else:
                self.write_log(f"Insert Failed: {val} (Out of Range)")
                messagebox.showerror("Error", "Out of range")

    def show_inorder(self):
        arr = []
        inorder(self.root_node, arr)
        res = " , ".join(map(str, arr))
        self.write_log(f"Inorder: [{res}]")
        messagebox.showinfo("Inorder Traversal", res)

    def show_preorder(self):
        arr = []
        preorder(self.root_node, arr)
        res = " , ".join(map(str, arr))
        self.write_log(f"Preorder: [{res}]")
        messagebox.showinfo("Preorder Traversal", res)

    def show_postorder(self):
        arr = []
        postorder(self.root_node, arr)
        res = " , ".join(map(str, arr))
        self.write_log(f"Postorder: [{res}]")
        messagebox.showinfo("Postorder Traversal", res)

if __name__ == "__main__":
    from tkinter import simpledialog
    
    # Create a temporary root window for dialogs
    temp_root = tk.Tk()
    temp_root.withdraw()  # Hide the temporary window
    
    # Force window to appear on top
    temp_root.attributes('-topmost', True)
    temp_root.attributes('-alpha', 0.0) 
    temp_root.update()
    temp_root.deiconify() 
    temp_root.attributes('-alpha', 1.0) 
    temp_root.lift()
    temp_root.focus_force()
    temp_root.after(1, lambda: temp_root.focus_force()) 
    
    try:
        lvls = simpledialog.askinteger("Setup", "Input desired level of Binary tree:", 
                                      minvalue=1, maxvalue=5, parent=temp_root)
        if lvls is None:
            temp_root.destroy()
            exit()
            
        min_v = simpledialog.askinteger("Setup", "Min value:", parent=temp_root)
        if min_v is None:
            temp_root.destroy()
            exit()
            
        max_v = simpledialog.askinteger("Setup", "Max value:", parent=temp_root)
        if max_v is None:
            temp_root.destroy()
            exit()
            
        temp_root.destroy()
        TreeApp(lvls, min_v, max_v)
    except Exception as e:
        temp_root.destroy()
        print(f"Error: {e}")
