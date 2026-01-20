import tkinter as tk
from tkinter import simpledialog, scrolledtext

# --- GLOBAL DATA ---
garage_queue = []
garage_capacity = 10
total_arrivals = 0
total_departures = 0

def arrive(queue, plate, current_count, log_func):
    plate = plate.upper()
    if len(queue) < garage_capacity:
        queue.insert(0, plate)
        log_func(f"✅ {plate} joined the queue.")
        return current_count + 1
    else:
        log_func("❌ Garage is full!")
        return current_count

def depart_middle(queue, target_plate, current_departures, log_func):
    target_plate = target_plate.upper()
    if target_plate not in queue:
        log_func(f"❓ Error: Car '{target_plate}' not found.")
        return current_departures

    temp_buffer = []
    ops = 0
    while queue:
        current = queue.pop()
        ops += 1
        if current == target_plate:
            current_departures += 1
            log_func(f"🎯 {target_plate} exited the front.")
            break
        else:
            temp_buffer.append(current)

    while temp_buffer:
        queue.append(temp_buffer.pop())
        ops += 1

    log_func(f"📊 Total Moves: {ops}")
    return current_departures

class GarageUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FIFO GARAGE (Queue)")
        self.root.geometry("700x600") 
        self.root.configure(bg="#f0f0f0")
        
        tk.Label(root, text="FIFO GARAGE (Queue)", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        self.stats_label = tk.Label(root, text="", font=("Arial", 11), bg="#f0f0f0")
        self.stats_label.pack()
        
        self.canvas = tk.Canvas(root, bg="white", height=120, highlightthickness=1)
        self.canvas.pack(fill=tk.X, padx=20, pady=10)
        
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Arrive", command=self.arrive_action).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Depart", command=self.depart_action).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_garage).pack(side=tk.LEFT, padx=5)

        # --- THE LOGGING UI ---
        tk.Label(root, text="System Logs:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=20)
        self.log_area = scrolledtext.ScrolledText(root, height=10, state='disabled', font=("Consolas", 10))
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.update_display()

    def write_log(self, message):
        """Adds a message to the UI log area."""
        self.log_area.configure(state='normal') # Enable editing
        self.log_area.insert(tk.END, message + "\n") # Add message
        self.log_area.see(tk.END) # Scroll to bottom
        self.log_area.configure(state='disabled') # Disable editing
        print(message) # Still print to terminal for backup

    def arrive_action(self):
        global total_arrivals
        plate = simpledialog.askstring("Arrive", "Enter Plate:")
        if plate and plate.strip():
            total_arrivals = arrive(garage_queue, plate.strip(), total_arrivals, self.write_log)
            self.update_display()
    
    def depart_action(self):
        global total_departures
        if not garage_queue:
            self.write_log("📭 Empty.")
            return
        
        target = simpledialog.askstring("Depart", "Plate to remove:")
        if target and target.strip():
            total_departures = depart_middle(garage_queue, target.strip(), total_departures, self.write_log)
            self.update_display()
    
    def reset_garage(self):
        global total_arrivals, total_departures
        garage_queue.clear()
        total_arrivals = 0
        total_departures = 0
        self.log_area.configure(state='normal')
        self.log_area.delete('1.0', tk.END)
        self.log_area.configure(state='disabled')
        self.update_display()
        self.write_log("System Reset.")

    def update_display(self):
        self.stats_label.config(text=f"Arrivals: {total_arrivals} | Departures: {total_departures}")
        self.canvas.delete("all")
        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 660
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 120
        
        self.canvas.create_text(60, 20, text="(Entrance)", font=("Arial", 10, "bold"))
        self.canvas.create_text(w - 60, 20, text="(Exit)", font=("Arial", 10, "bold"))
        
        if garage_queue:
            car_w = min(70, (w - 140) // len(garage_queue) - 5)
            y = h // 2
            for i, plate in enumerate(garage_queue):
                x = 70 + i * (car_w + 5)
                self.canvas.create_rectangle(x, y - 20, x + car_w, y + 20, fill="#4a90e2", outline="black")
                self.canvas.create_text(x + car_w // 2, y, text=plate, font=("Arial", 9, "bold"), fill="white")
        else:
            self.canvas.create_text(w // 2, h // 2, text="📭 Empty", font=("Arial", 14), fill="gray")

if __name__ == "__main__":
    root = tk.Tk()
    app = GarageUI(root)
    root.mainloop()
