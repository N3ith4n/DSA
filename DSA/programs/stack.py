import tkinter as tk
from tkinter import simpledialog, scrolledtext

# --- GLOBAL DATA ---
garage_stack = []
garage_capacity = 10
total_arrivals = 0
total_departures = 0

def arrive(stack, plate, current_count, log_func):
    plate = plate.upper()
    if len(stack) < garage_capacity:
        stack.insert(0, plate)  # Add to the left (Top of stack)
        log_func(f"✅ {plate} parked at the TOP.")
        return current_count + 1
    else:
        log_func("❌ Garage is full!")
        return current_count

def depart_middle(stack, target_plate, current_departures, log_func):
    target_plate = target_plate.upper()
    if target_plate not in stack:
        log_func(f"❓ Error: Car '{target_plate}' not found.")
        return current_departures

    temp_stack = []
    ops = 0

    # LIFO: We start looking from the TOP (index 0)
    while stack:
        current = stack.pop(0) 
        ops += 1
        if current == target_plate:
            current_departures += 1
            log_func(f"🎯 {target_plate} departed.")
            break
        else:
            temp_stack.append(current)

    # Restack back to the Top (reversing the temp stack to maintain order)
    while temp_stack:
        stack.insert(0, temp_stack.pop())
        ops += 1

    log_func(f"📊 Total Moves: {ops}")
    return current_departures

# GUI Wrapper
class GarageUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LIFO GARAGE (Stack)")
        self.root.geometry("500x700") 
        self.root.configure(bg="#f0f0f0")
        
        tk.Label(root, text="LIFO GARAGE (Stack)", font=("Arial", 16, "bold"),
                 bg="#f0f0f0").pack(pady=10)
        
        self.stats_label = tk.Label(root, text="", font=("Arial", 11), bg="#f0f0f0")
        self.stats_label.pack()
        
        # Canvas for the visual Stack
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Arrive", command=self.arrive_action,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Depart", command=self.depart_action,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_garage,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # --- THE LOGGING UI ---
        tk.Label(root, text="System Logs:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20)
        self.log_area = scrolledtext.ScrolledText(root, height=8, state='disabled', font=("Consolas", 10))
        self.log_area.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.update_display()

    def write_log(self, message):
        """Adds a message to the UI log area."""
        self.log_area.configure(state='normal') 
        self.log_area.insert(tk.END, message + "\n") 
        self.log_area.see(tk.END) 
        self.log_area.configure(state='disabled') 
        print(message) # Backup print

    def arrive_action(self):
        global garage_stack, total_arrivals
        plate = simpledialog.askstring("Arrive", "Enter Plate:")
        if plate and plate.strip():
            total_arrivals = arrive(garage_stack, plate.strip(), total_arrivals, self.write_log)
            self.update_display()
    
    def depart_action(self):
        global garage_stack, total_departures
        if not garage_stack:
            self.write_log("📭 Empty.")
            return
        
        target = simpledialog.askstring("Depart", "Plate to remove:")
        if target and target.strip():
            total_departures = depart_middle(garage_stack, target.strip(), total_departures, self.write_log)
            self.update_display()
    
    def reset_garage(self):
        global garage_stack, total_arrivals, total_departures
        garage_stack.clear()
        total_arrivals = 0
        total_departures = 0
        self.log_area.configure(state='normal')
        self.log_area.delete('1.0', tk.END)
        self.log_area.configure(state='disabled')
        self.update_display()
        self.write_log("System Reset.")
    
    def update_display(self):
        global garage_stack, total_arrivals, total_departures, garage_capacity
        
        self.stats_label.config(
            text=f"Arrivals: {total_arrivals} | Departures: {total_departures}"
        )
        
        self.canvas.delete("all")
        
        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 460
        # Calculate height dynamically based on canvas size
        
        # TOP label matching original: (Top/Exit)
        self.canvas.create_text(w // 2, 20, text="(Top/Exit)", font=("Arial", 10, "bold"))
        
        if garage_stack:
            car_w = 150
            car_h = 30 # Made slightly smaller to fit more cars
            spacing = 5
            start_y = 40
            
            for i, plate in enumerate(garage_stack):
                x = (w - car_w) // 2
                y = start_y + i * (car_h + spacing)
                
                self.canvas.create_rectangle(x, y, x + car_w, y + car_h,
                                            fill="#e74c3c", outline="black")
                self.canvas.create_text(x + car_w // 2, y + car_h // 2, text=plate,
                                       font=("Arial", 10, "bold"), fill="white")
            
            # BOTTOM label
            bottom_y = start_y + len(garage_stack) * (car_h + spacing) + 15
            self.canvas.create_text(w // 2, bottom_y, text="(Bottom)", font=("Arial", 10, "bold"))
        else:
            # Center the empty text roughly in the middle of the available canvas
            self.canvas.create_text(w // 2, 100, text="📭 Empty",
                                   font=("Arial", 14), fill="gray")

if __name__ == "__main__":
    root = tk.Tk()
    # Force window focus trick
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.0)
    root.update()
    root.deiconify()
    root.attributes('-alpha', 1.0)
    root.lift()
    root.focus_force()
    root.after(1, lambda: root.focus_force())
    root.after(100, lambda: root.attributes('-topmost', False))
    
    app = GarageUI(root)
    root.mainloop()
