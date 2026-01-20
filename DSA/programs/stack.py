# --- GLOBAL DATA ---
garage_stack = []
garage_capacity = 10
total_arrivals = 0
total_departures = 0

def arrive(stack, plate, current_count):
    plate = plate.upper()
    if len(stack) < garage_capacity:
        stack.insert(0, plate)  # Add to the left
        print(f"✅ {plate} parked at the TOP.")
        return current_count + 1
    else:
        print("❌ Garage is full!")
        return current_count

def depart_middle(stack, target_plate, current_departures):
    target_plate = target_plate.upper()
    if target_plate not in stack:
        print(f"❓ Error: Car '{target_plate}' not found.")
        return current_departures

    temp_stack = []
    ops = 0

    # LIFO: We start looking from the LEFT (the Top/Newest)
    while stack:
        current = stack.pop(0) 
        ops += 1
        if current == target_plate:
            current_departures += 1
            print(f"🎯 {target_plate} departed.")
            break
        else:
            temp_stack.append(current)

    # Restack back to the Left
    while temp_stack:
        stack.insert(0, temp_stack.pop())
        ops += 1

    print(f"📊 Total Moves: {ops}")
    return current_departures

# GUI Wrapper
class GarageUI:
    def __init__(self, root):
        import tkinter as tk
        from tkinter import simpledialog, messagebox
        
        global garage_stack, total_arrivals, total_departures
        
        self.root = root
        self.root.title("LIFO GARAGE (Stack)")
        self.root.geometry("500x550")
        self.root.configure(bg="#f0f0f0")
        
        tk.Label(root, text="LIFO GARAGE (Stack)", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack(pady=10)
        
        self.stats_label = tk.Label(root, text="", font=("Arial", 11), bg="#f0f0f0")
        self.stats_label.pack()
        
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Arrive", command=self.arrive_action,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Depart", command=self.depart_action,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_garage,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        self.update_display()
    
    def arrive_action(self):
        from tkinter import simpledialog, messagebox
        global garage_stack, total_arrivals
        
        plate = simpledialog.askstring("Arrive", "Enter Plate:")
        if plate:
            plate = plate.strip()
            if plate:
                total_arrivals = arrive(garage_stack, plate, total_arrivals)
                self.update_display()
    
    def depart_action(self):
        from tkinter import simpledialog, messagebox
        global garage_stack, total_departures
        
        if not garage_stack:
            print("📭 Empty.")
            messagebox.showinfo("Empty", "📭 Empty.")
            return
        
        target = simpledialog.askstring("Depart", "Plate to remove:")
        if target:
            target = target.strip()
            if target:
                total_departures = depart_middle(garage_stack, target, total_departures)
                self.update_display()
    
    def reset_garage(self):
        global garage_stack, total_arrivals, total_departures
        garage_stack.clear()
        total_arrivals = 0
        total_departures = 0
        self.update_display()
    
    def update_display(self):
        import tkinter as tk
        global garage_stack, total_arrivals, total_departures, garage_capacity
        
        # Stats label - matches original format
        self.stats_label.config(
            text=f"Arrivals: {total_arrivals} | Departures: {total_departures}"
        )
        
        self.canvas.delete("all")
        
        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 460
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 400
        
        # TOP label matching original: (Top/Exit)
        self.canvas.create_text(w // 2, 20, text="(Top/Exit)", font=("Arial", 10, "bold"))
        
        if garage_stack:
            car_w = 150
            car_h = 40
            spacing = 5
            start_y = 50
            
            for i, plate in enumerate(garage_stack):
                x = (w - car_w) // 2
                y = start_y + i * (car_h + spacing)
                
                self.canvas.create_rectangle(x, y, x + car_w, y + car_h,
                                            fill="#e74c3c", outline="black")
                self.canvas.create_text(x + car_w // 2, y + car_h // 2, text=plate,
                                       font=("Arial", 10, "bold"), fill="white")
            
            # BOTTOM label
            bottom_y = start_y + len(garage_stack) * (car_h + spacing) + 10
            self.canvas.create_text(w // 2, bottom_y, text="(Bottom)", font=("Arial", 10, "bold"))
        else:
            self.canvas.create_text(w // 2, h // 2, text="📭 Empty",
                                   font=("Arial", 14), fill="gray")

if __name__ == "__main__":
    import tkinter as tk
    
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.0)  # Make invisible temporarily
    root.update()
    root.deiconify()
    root.attributes('-alpha', 1.0)  # Make visible
    root.lift()
    root.focus_force()
    root.after(1, lambda: root.focus_force())
    root.after(100, lambda: root.attributes('-topmost', False))
    
    app = GarageUI(root)
    root.mainloop()