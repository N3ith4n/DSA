import tkinter as tk
from tkinter import messagebox, simpledialog #added simple dialog
import time

class HanoiApp:
    def __init__(self, root, n=5):
        self.root = root
        self.root.title("Tower of Hanoi App")
        self.n = n
        self.main_frame = tk.Frame(root, bg="#e6f2ff")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.setup_menu()

    def setup_menu(self):
        """Clears the screen and shows the main menu."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        self.is_solving = False
        self.moves = 0
        self.pegs = [[], [], []]
        self.discs_objs = {}

        menu_container = tk.Frame(self.main_frame, bg="#e6f2ff")
        menu_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(menu_container, text="TOWER OF HANOI", font=("Arial", 28, "bold"), 
                 bg="#e6f2ff", fg="#333333").pack(pady=30)
        
        btn_style = {"font": ("Arial", 12, "bold"), "width": 20, "pady": 10, 
                     "bg": "#ffffff", "cursor": "hand2"}
        
        tk.Button(menu_container, text="PLAY MANUALLY", command=lambda: self.start_game("P"), **btn_style).pack(pady=10)
        tk.Button(menu_container, text="WATCH AUTO-SOLVE", command=lambda: self.start_game("S"), **btn_style).pack(pady=10)
        tk.Label(menu_container, text=f"Goal: Move {self.n} discs to Peg C", bg="#e6f2ff", font=("Arial", 10, "italic")).pack(pady=20)

    def start_game(self, mode):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Top Bar for Controls
        self.top_bar = tk.Frame(self.main_frame, bg="#d0e1f9", height=50)
        self.top_bar.pack(fill=tk.X)
        
        tk.Button(self.top_bar, text="← Return to Menu", command=self.setup_menu, 
                  bg="#ff6666", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10, pady=10)
        
        self.info_label = tk.Label(self.top_bar, text=f"Moves: {self.moves}", 
                                   font=("Arial", 12, "bold"), bg="#d0e1f9")
        self.info_label.pack(side=tk.RIGHT, padx=20)

        # Game Canvas
        self.canvas = tk.Canvas(self.main_frame, width=600, height=400, bg="#e6f2ff", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.draw_environment()
        self.setup_discs()

        if mode == "P":
            self.canvas.bind("<Button-1>", self.on_click)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_release)
        else:
            self.is_solving = True
            self.root.after(800, self.start_auto_solve)

    def draw_environment(self):
        self.peg_x = [120, 300, 480]
        self.floor_y = 350
        self.disc_height = 25
        # Draw Floor
        self.canvas.create_rectangle(20, self.floor_y, 580, self.floor_y + 15, fill="#808080", outline="#505050")
        # Draw Pegs
        for x in self.peg_x:
            self.canvas.create_rectangle(x - 6, 120, x + 6, self.floor_y, fill="#5d5d5d", outline="#333333")

    def setup_discs(self):
        colors = ["#ff0000", "#ff8c00", "#ffff00", "#00ff00", "#008000", "#00ffff", "#0000ff", "#8b00ff", "#ff00ff"]
        for i in range(self.n, 0, -1):
            width = 40 + (i * 32)
            color = colors[(i-1) % len(colors)]
            x1 = self.peg_x[0] - width//2
            y1 = self.floor_y - (self.n - i + 1) * self.disc_height
            rect = self.canvas.create_rectangle(x1, y1, x1 + width, y1 + self.disc_height, 
                                               fill=color, outline="#222222", width=2)
            self.pegs[0].append(i)
            self.discs_objs[i] = rect

    # --- Interaction Logic ---

    def on_click(self, event):
        if self.is_solving: return
        peg_idx = self.get_peg_from_x(event.x)
        if self.pegs[peg_idx]:
            self.selected_disc = self.pegs[peg_idx][-1]
            self.start_peg = peg_idx
            self.canvas.tag_raise(self.discs_objs[self.selected_disc])

    def on_drag(self, event):
        if hasattr(self, 'selected_disc') and self.selected_disc:
            rect = self.discs_objs[self.selected_disc]
            w = (40 + (self.selected_disc * 32)) // 2
            self.canvas.coords(rect, event.x - w, event.y - 12, event.x + w, event.y + 12)

    def on_release(self, event):
        if hasattr(self, 'selected_disc') and self.selected_disc:
            end_peg = self.get_peg_from_x(event.x)
            if end_peg != self.start_peg and (not self.pegs[end_peg] or self.pegs[end_peg][-1] > self.selected_disc):
                self.pegs[self.start_peg].pop()
                self.pegs[end_peg].append(self.selected_disc)
                self.moves += 1
                self.info_label.config(text=f"Moves: {self.moves}")
                self.update_disc_pos(self.selected_disc, end_peg)
            else:
                self.update_disc_pos(self.selected_disc, self.start_peg)
            
            self.selected_disc = None
            if len(self.pegs[2]) == self.n:
                messagebox.showinfo("Victory!", f"You solved it in {self.moves} moves!")
                self.setup_menu()

    def update_disc_pos(self, disc_size, peg_idx):
        if disc_size not in self.discs_objs: return
        rect = self.discs_objs[disc_size]
        pos_in_stack = self.pegs[peg_idx].index(disc_size)
        width = 40 + (disc_size * 32)
        x1 = self.peg_x[peg_idx] - width//2
        y1 = self.floor_y - (pos_in_stack + 1) * self.disc_height
        self.canvas.coords(rect, x1, y1, x1 + width, y1 + self.disc_height)
        self.root.update()

    def get_peg_from_x(self, x):
        if x < 210: return 0
        if x < 390: return 1
        return 2

    # --- Solver Logic ---

    def start_auto_solve(self):
        try:
            self.solve_hanoi(self.n, 0, 2, 1)
            if self.is_solving:
                messagebox.showinfo("Done", "The computer has finished.")
                self.setup_menu()
        except tk.TclError: # Handles case where window is closed during recursion
            pass

    def solve_hanoi(self, n, source, target, auxiliary):
        if not self.is_solving: return # Exit if user returned to menu
        if n > 0:
            self.solve_hanoi(n - 1, source, auxiliary, target)
            if not self.is_solving: return
            
            disc = self.pegs[source].pop()
            self.pegs[target].append(disc)
            self.moves += 1
            self.info_label.config(text=f"Auto-Solving... Moves: {self.moves}")
            self.update_disc_pos(disc, target)
            time.sleep(0.4) 
            
            self.solve_hanoi(n - 1, auxiliary, target, source)


################################################################
#changed#
if __name__ == "__main__":
    # Create temporary root for input dialog
    temp_root = tk.Tk()
    temp_root.withdraw()
    
    # Force dialog to appear on top
    temp_root.attributes('-alpha', 0.0)
    temp_root.update()
    temp_root.deiconify()
    temp_root.attributes('-alpha', 1.0)
    temp_root.after(1, lambda: temp_root.focus_force())
    temp_root.attributes('-topmost', True)
    temp_root.lift()
    temp_root.focus_force()
    
    # Ask for number of discs
    num_discs = simpledialog.askinteger("Tower of Hanoi", "Enter number of discs (1-9):", 
                                        minvalue=1, maxvalue=9, parent=temp_root)
    
    if num_discs is None:
        temp_root.destroy()
        exit()
    
    temp_root.destroy()
    
    # Create main window with aggressive window forcing
    root = tk.Tk()
    root.geometry("600x550")
    root.resizable(False, False)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.0)
    root.update()
    root.deiconify()
    root.attributes('-alpha', 1.0)
    root.lift()
    root.focus_force()
    root.after(1, lambda: root.focus_force())
    root.after(100, lambda: root.attributes('-topmost', False))
    
    app = HanoiApp(root, num_discs)
    root.mainloop()