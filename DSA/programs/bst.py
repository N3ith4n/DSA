import tkinter as tk
from tkinter import messagebox, simpledialog

FONT_MAIN = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 11, "bold")
BTN_COLOR = "#4C89FF"
BTN_COLOR_HOVER = "#3B6EDC"
BG_MAIN = "#F5F7FB"
PANEL_BG = "#FFFFFF"
TEXT_BG = "#ECEFF4"


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

###################################################
# CHANGED: added min_val, max_val parameters
class TreeUI:
    def __init__(self, root, min_val, max_val):
        self.root = root
        self.root.title("Binary Search Tree Visualizer")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_MAIN)

        self.tree_root = None
        self.node_positions = {}

        # Store the passed values
        self.min_val = min_val
        self.max_val = max_val

        self.build_ui()
##############################################

    # UI LAYOUT
    def build_ui(self):
        control_frame = tk.Frame(self.root, bg=PANEL_BG, bd=0)
        control_frame.pack(fill="x", padx=10, pady=10)

        btn_frame = tk.Frame(control_frame, bg=PANEL_BG)
        btn_frame.pack(side="left", padx=10, pady=5)

        self.add_button(btn_frame, "Insert Node", self.insert_node)
        self.add_button(btn_frame, "Delete Node", self.delete_node)
        self.add_button(btn_frame, "Reset Tree", self.reset_tree)

        output_frame = tk.Frame(control_frame, bg=PANEL_BG)
        output_frame.pack(side="right", padx=10)

        tk.Label(output_frame, text="Traversals:", bg=PANEL_BG, font=FONT_TITLE).pack(anchor="w")

        self.traversal_text = tk.Text(output_frame, width=45, height=5, font=FONT_MAIN, bg=TEXT_BG, bd=0)
        self.traversal_text.pack()

        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=10, pady=10)

    # BUTTON FACTORY (hover effect)
    def add_button(self, frame, text, command):
        btn = tk.Label(frame, text=text, bg=BTN_COLOR, fg="white", padx=12, pady=6, font=FONT_MAIN, cursor="hand2")
        btn.pack(side="left", padx=4)
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))
 
    # BST OPERATIONS
    def insert_node(self):
        val = simpledialog.askinteger("Insert Node", f"Enter a number ({self.min_val} to {self.max_val}):")
        if val is None:
            return

        # NEW: Min / Max validation
        if not (self.min_val <= val <= self.max_val):
            messagebox.showwarning("Out of Range",
                                   f"Value must be between {self.min_val} and {self.max_val}.")
            return

        if self.tree_root is None:
            self.tree_root = Node(val)
        else:
            if not self.bst_insert(self.tree_root, val):
                messagebox.showwarning("Duplicate", "value alreay exists")
                return

        self.redraw()

    def bst_insert(self, root, val):
        if val == root.val:
            return False
        elif val < root.val:
            if root.left:
                return self.bst_insert(root.left, val)
            else:
                root.left = Node(val)
                return True
        else:
            if root.right:
                return self.bst_insert(root.right, val)
            else:
                root.right = Node(val)
                return True

    def delete_node(self):
        if not self.tree_root:
            return

        val = simpledialog.askinteger("Delete Node", "Enter value to delete:")
        if val is None:
            return

        self.tree_root = self.delete_bst(self.tree_root, val)
        self.redraw()

    def delete_bst(self, root, val):
        if not root:
            return root
        if val < root.val:
            root.left = self.delete_bst(root.left, val)
        elif val > root.val:
            root.right = self.delete_bst(root.right, val)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            temp = self.find_min(root.right)
            root.val = temp.val
            root.right = self.delete_bst(root.right, temp.val)
        return root

    def find_min(self, root):
        while root.left:
            root = root.left
        return root

    def reset_tree(self):
        self.tree_root = None
        self.node_positions.clear()
        self.canvas.delete("all")
        self.traversal_text.delete("1.0", "end")

    # DRAW OPERATIONS or create the damn tree
    def redraw(self):
        self.canvas.delete("all")
        self.node_positions.clear()

        if self.tree_root:
            self.calc_positions(self.tree_root, 450, 40, 180)
            self.draw_tree(self.tree_root)

        self.show_traversals()

    def calc_positions(self, node, x, y, offset):
        if not node:
            return
        self.node_positions[node] = (x, y)
        self.calc_positions(node.left, x - offset, y + 80, offset // 2)
        self.calc_positions(node.right, x + offset, y + 80, offset // 2)

    def draw_tree(self, node):
        if node.left:
            x1, y1 = self.node_positions[node]
            x2, y2 = self.node_positions[node.left]
            self.canvas.create_line(x1, y1, x2, y2)
            self.draw_tree(node.left)

        if node.right:
            x1, y1 = self.node_positions[node]
            x2, y2 = self.node_positions[node.right]
            self.canvas.create_line(x1, y1, x2, y2)
            self.draw_tree(node.right)

        x, y = self.node_positions[node]
        r = 20
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#4C89FF", outline="#204A99")
        self.canvas.create_text(x, y, text=str(node.val), fill="white", font=("Segoe UI", 10, "bold"))

    # traversal logoc
    def show_traversals(self):
        inorder, preorder, postorder = [], [], []
        self.in_order(self.tree_root, inorder)
        self.pre_order(self.tree_root, preorder)
        self.post_order(self.tree_root, postorder)

        self.traversal_text.delete("1.0", "end")
        self.traversal_text.insert("end", f"In-Order  (LNR): {inorder}\n")
        self.traversal_text.insert("end", f"Pre-Order (NLR): {preorder}\n")
        self.traversal_text.insert("end", f"Post-Order(LRN): {postorder}\n") # putangina

    def in_order(self, node, arr):
        if node:
            self.in_order(node.left, arr)
            arr.append(node.val)
            self.in_order(node.right, arr)

    def pre_order(self, node, arr):
        if node:
            arr.append(node.val)
            self.pre_order(node.left, arr)
            self.pre_order(node.right, arr)

    def post_order(self, node, arr):
        if node:
            self.post_order(node.left, arr)
            self.post_order(node.right, arr)
            arr.append(node.val)

#################################################
#changed#
# START APP - Get input FIRST, then create main window
if __name__ == "__main__":
    # Create temporary hidden window for dialogs
    temp_root = tk.Tk()
    temp_root.withdraw()
    
    # Force window to appear immediately
    temp_root.attributes('-alpha', 0.0)  # Make invisible temporarily
    temp_root.update()
    temp_root.deiconify()
    temp_root.attributes('-alpha', 1.0)  # Make visible
    temp_root.after(1, lambda: temp_root.focus_force())
    
    # Force dialogs to appear on top
    temp_root.attributes('-topmost', True)
    temp_root.lift()
    temp_root.focus_force()
    
    # Get min/max values
    min_val = simpledialog.askinteger("Minimum Allowed Value", "Enter minimum acceptable value:", parent=temp_root)
    
    if min_val is None:
        temp_root.destroy()
        exit()
    
    max_val = simpledialog.askinteger("Maximum Allowed Value", "Enter maximum acceptable value:", parent=temp_root)
    
    if max_val is None:
        temp_root.destroy()
        exit()
    
    if min_val >= max_val:
        messagebox.showerror("Error", "Minimum must be LESS than Maximum!", parent=temp_root)
        temp_root.destroy()
        exit()
    
    # Destroy temp window
    temp_root.destroy()
    
    # Create main window with window forcing
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.0)  # Make invisible temporarily
    root.update()
    root.deiconify()
    root.attributes('-alpha', 1.0)  # Make visible
    root.lift()
    root.focus_force()
    root.after(1, lambda: root.focus_force())
    root.after(100, lambda: root.attributes('-topmost', False))  # Remove topmost after showing
    
    app = TreeUI(root, min_val, max_val)
    root.mainloop()