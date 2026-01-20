# --- GLOBAL DATA --- #changed to have gui
garage_queue = []
garage_capacity = 10
total_arrivals = 0
total_departures = 0

def arrive(queue, plate, current_count):
    plate = plate.upper()
    if len(queue) < garage_capacity:
        queue.insert(0, plate)  # Entrance is the Left
        print(f"✅ {plate} joined the queue.")
        return current_count + 1
    else:
        print("❌ Garage is full!")
        return current_count

def depart_middle(queue, target_plate, current_departures):
    target_plate = target_plate.upper()
    if target_plate not in queue:
        print(f"❓ Error: Car '{target_plate}' not found.")
        return current_departures

    temp_buffer = []
    ops = 0

    # FIFO: We start looking from the RIGHT (the Exit/Oldest)
    while queue:
        current = queue.pop() # Removes from the very right
        ops += 1
        if current == target_plate:
            current_departures += 1
            print(f"🎯 {target_plate} exited the front.")
            break
        else:
            temp_buffer.append(current)

    # Put back the cars that were behind the target
    while temp_buffer:
        queue.append(temp_buffer.pop(0)) # Re-insert at the end of the line
        ops += 1

    print(f"📊 Total Moves: {ops}")
    return current_departures

# GUI Wrapper
class GarageUI:
    def __init__(self, root):
        import tkinter as tk
        from tkinter import simpledialog, messagebox, scrolledtext
        
        global garage_queue, total_arrivals, total_departures
        
        self.root = root
        self.root.title("FIFO GARAGE (Queue)")
        self.root.geometry("700x550")  # Increased height for log
        self.root.configure(bg="#f0f0f0")
        
        tk.Label(root, text="FIFO GARAGE (Queue)", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack(pady=10)
        
        self.stats_label = tk.Label(root, text="", font=("Arial", 11), bg="#f0f0f0")
        self.stats_label.pack()
        
        self.canvas = tk.Canvas(root, bg="white", height=150, highlightthickness=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Terminal/Log display
        log_frame = tk.Frame(root, bg="#f0f0f0")
        log_frame.pack(fill=tk.BOTH, padx=20, pady=(0, 10))
        
        tk.Label(log_frame, text="Terminal Log:", font=("Arial", 10, "bold"),
                bg="#f0f0f0").pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, font=("Consolas", 9),
                                                  bg="#1a1a1a", fg="#00ff00", wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Arrive", command=self.arrive_action,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Depart", command=self.depart_action,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_garage,
                 font=("Arial", 10), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        self.log("System ready. FIFO GARAGE (Queue) initialized.")
        self.update_display()
    
    def log(self, message):
        """Add message to terminal log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def arrive_action(self):
        from tkinter import simpledialog, messagebox
        global garage_queue, total_arrivals
        
        plate = simpledialog.askstring("Arrive", "Enter Plate:")
        if plate:
            plate = plate.strip()
            if plate:
                plate_upper = plate.upper()
                if len(garage_queue) < garage_capacity:
                    total_arrivals = arrive(garage_queue, plate, total_arrivals)
                    self.log(f"✅ {plate_upper} joined the queue.")
                else:
                    self.log("❌ Garage is full!")
                self.update_display()
    
    def depart_action(self):
        from tkinter import simpledialog, messagebox
        global garage_queue, total_departures
        
        if not garage_queue:
            self.log("📭 Empty.")
            messagebox.showinfo("Empty", "📭 Empty.")
            return
        
        target = simpledialog.askstring("Depart", "Plate to remove:")
        if target:
            target = target.strip()
            if target:
                target_upper = target.upper()
                if target_upper not in garage_queue:
                    self.log(f"❓ Error: Car '{target_upper}' not found.")
                    return
                
                # Track operations for logging
                temp_buffer = []
                ops = 0
                found = False
                
                while garage_queue:
                    current = garage_queue.pop()
                    ops += 1
                    if current == target_upper:
                        total_departures += 1
                        found = True
                        self.log(f"🎯 {target_upper} exited the front.")
                        break
                    else:
                        temp_buffer.append(current)
                
                while temp_buffer:
                    garage_queue.append(temp_buffer.pop(0))
                    ops += 1
                
                if found:
                    self.log(f"📊 Total Moves: {ops}")
                
                self.update_display()
    
    def reset_garage(self):
        global garage_queue, total_arrivals, total_departures
        garage_queue.clear()
        total_arrivals = 0
        total_departures = 0
        self.log("🔄 Garage reset. All data cleared.")
        self.update_display()
    
    def update_display(self):
        import tkinter as tk
        global garage_queue, total_arrivals, total_departures, garage_capacity
        
        # Stats label - matches original format
        self.stats_label.config(
            text=f"Arrivals: {total_arrivals} | Departures: {total_departures}"
        )
        
        self.canvas.delete("all")
        
        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 660
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 150
        
        # Labels matching original: (Entrance) ... (Exit)
        self.canvas.create_text(60, 20, text="(Entrance)", font=("Arial", 10, "bold"))
        self.canvas.create_text(w - 60, 20, text="(Exit)", font=("Arial", 10, "bold"))
        
        if garage_queue:
            car_w = min(70, (w - 140) // len(garage_queue) - 5)
            y = h // 2
            
            for i, plate in enumerate(garage_queue):
                x = 70 + i * (car_w + 5)
                self.canvas.create_rectangle(x, y - 20, x + car_w, y + 20,
                                            fill="#4a90e2", outline="black")
                self.canvas.create_text(x + car_w // 2, y, text=plate,
                                       font=("Arial", 9, "bold"), fill="white")
        else:
            self.canvas.create_text(w // 2, h // 2, text="📭 Empty",
                                   font=("Arial", 14), fill="gray")

if __name__ == "__main__":
    import tkinter as tk
    
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()
    root.after(100, lambda: root.attributes('-topmost', False))
    
    app = GarageUI(root)
    root.mainloop()
