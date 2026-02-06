import tkinter as tk
from tkinter import ttk
import math
import time
import random
from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum

class RotationDirection(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1

@dataclass
class MotorState:
    running: bool = False
    current_angle: float = 0.0
    target_speed: float = 0.0
    direction: RotationDirection = RotationDirection.CLOCKWISE
    actual_speed: float = 0.0

class AnimatedGauge(tk.Canvas):
    def __init__(self, parent, width=300, height=300, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.gauge_radius = min(width, height) // 2 - 20
        
        self.bg_color = "#2E3440"
        self.arc_color = "#4C566A"
        self.text_color = "#D8DEE9"
        self.needle_color = "#BF616A"
        self.speed_color = "#88C0D0"
        
        self.configure(bg=self.bg_color, highlightthickness=0)
        self.draw_gauge()
        
    def draw_gauge(self):
        # Clear canvas
        self.delete("all")
        
        # Draw outer circle
        self.create_oval(
            self.center_x - self.gauge_radius,
            self.center_y - self.gauge_radius,
            self.center_x + self.gauge_radius,
            self.center_y + self.gauge_radius,
            outline=self.arc_color,
            width=3
        )
        
        # Draw speed markings
        for speed in range(-100, 101, 20):
            angle = self.speed_to_angle(speed)
            self.draw_speed_mark(angle, str(speed), speed == 0)
        
        # Draw center circle
        self.create_oval(
            self.center_x - 8,
            self.center_y - 8,
            self.center_x + 8,
            self.center_y + 8,
            fill=self.needle_color,
            outline=self.needle_color
        )
        
        # Initialize needle
        self.needle = self.create_line(
            self.center_x, self.center_y,
            self.center_x, self.center_y - self.gauge_radius + 10,
            fill=self.needle_color,
            width=3,
            arrow=tk.LAST
        )
        
        # Speed display
        self.speed_text = self.create_text(
            self.center_x,
            self.center_y + 40,
            text="0 RPM",
            fill=self.speed_color,
            font=("Arial", 14, "bold")
        )
        
        # Angle display
        self.angle_text = self.create_text(
            self.center_x,
            self.center_y + 70,
            text="0°",
            fill=self.text_color,
            font=("Arial", 12)
        )
        
    def speed_to_angle(self, speed: float) -> float:
        """Convert speed (-100 to 100) to angle (0 to 360)"""
        normalized = (speed + 100) / 200
        return normalized * 300 + 120  # Start from 120°, end at 420°
    
    def draw_speed_mark(self, angle: float, label: str, is_zero: bool = False):
        """Draw a speed mark on the gauge"""
        rad_angle = math.radians(angle)
        length = 15 if is_zero else 10
        width = 3 if is_zero else 2
        
        # Mark line
        x1 = self.center_x + (self.gauge_radius - 5) * math.cos(rad_angle)
        y1 = self.center_y - (self.gauge_radius - 5) * math.sin(rad_angle)
        x2 = self.center_x + (self.gauge_radius - length) * math.cos(rad_angle)
        y2 = self.center_y - (self.gauge_radius - length) * math.sin(rad_angle)
        
        self.create_line(x1, y1, x2, y2, fill=self.text_color, width=width)
        
        # Label
        label_radius = self.gauge_radius - 25
        x_label = self.center_x + label_radius * math.cos(rad_angle)
        y_label = self.center_y - label_radius * math.sin(rad_angle)
        
        self.create_text(
            x_label, y_label,
            text=label,
            fill=self.text_color,
            font=("Arial", 9, "bold" if is_zero else "normal")
        )
    
    def update_needle(self, speed: float, angle: float):
        """Update needle position and displays"""
        # Update needle
        gauge_angle = self.speed_to_angle(speed)
        rad_angle = math.radians(gauge_angle)
        
        needle_length = self.gauge_radius - 15
        x_end = self.center_x + needle_length * math.cos(rad_angle)
        y_end = self.center_y - needle_length * math.sin(rad_angle)
        
        self.coords(self.needle, self.center_x, self.center_y, x_end, y_end)
        
        # Update displays
        self.itemconfig(self.speed_text, text=f"{int(speed)} RPM")
        self.itemconfig(self.angle_text, text=f"{angle % 360:.1f}°")
        
        # Update needle color based on speed
        if abs(speed) < 1:  # Use small epsilon for comparison
            color = "#A3BE8C"  # Green for stopped
        elif speed > 0:
            color = "#88C0D0"  # Blue for forward
        else:
            color = "#BF616A"  # Red for reverse
            
        self.itemconfig(self.needle, fill=color)

class StepperMotorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Управление шаговым двигателем")
        self.geometry("800x600")
        self.configure(bg="#3B4252")
        
        # Initialize motor state
        self.motor_state = MotorState()
        
        # Setup styles
        self.setup_styles()
        
        # Build UI
        self.setup_ui()
        
        # Animation variables
        self.last_update_time = time.time()
        self.animation_running = True
        
        # Start update loop
        self.after(16, self.update_loop)  # ~60 FPS
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure colors
        bg_color = "#3B4252"
        fg_color = "#E5E9F0"
        accent_color = "#81A1C1"
        
        # Button style
        style.configure(
            "Accent.TButton",
            background=accent_color,
            foreground=fg_color,
            borderwidth=1,
            focuscolor="none"
        )
        
        # Regular button style
        style.configure(
            "TButton",
            background="#4C566A",
            foreground=fg_color
        )
        
        # Scale style
        style.configure(
            "Custom.Horizontal.TScale",
            background=bg_color,
            troughcolor="#4C566A",
            sliderlength=20
        )
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Контроллер шагового двигателя",
            font=("Arial", 20, "bold"),
            fg="#ECEFF4",
            bg="#3B4252"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Control panel (left)
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="15")
        control_frame.grid(row=1, column=0, padx=(0, 20), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Gauge (right)
        self.gauge = AnimatedGauge(main_frame, width=400, height=400)
        self.gauge.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_btn = ttk.Button(
            btn_frame,
            text="▶ Запуск",
            command=self.start_motor,
            style="Accent.TButton",
            width=12
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(
            btn_frame,
            text="⏹ Стоп",
            command=self.stop_motor,
            style="TButton",
            width=12
        )
        self.stop_btn.pack(side=tk.LEFT)
        
        # Speed control
        speed_frame = ttk.LabelFrame(control_frame, text="Скорость вращения", padding="10")
        speed_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Speed slider
        self.speed_var = tk.DoubleVar(value=0)
        self.speed_slider = ttk.Scale(
            speed_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            style="Custom.Horizontal.TScale",
            length=250
        )
        self.speed_slider.pack(fill=tk.X)
        
        # Speed value display
        self.speed_display = tk.Label(
            speed_frame,
            text="0 RPM",
            font=("Arial", 16, "bold"),
            fg="#88C0D0",
            bg="#3B4252"
        )
        self.speed_display.pack(pady=(10, 0))
        
        # Direction control
        direction_frame = ttk.LabelFrame(control_frame, text="Направление вращения", padding="10")
        direction_frame.pack(fill=tk.X)
        
        self.direction_var = tk.StringVar(value="clockwise")
        
        ttk.Radiobutton(
            direction_frame,
            text="По часовой стрелке",
            variable=self.direction_var,
            value="clockwise",
            command=self.update_direction
        ).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Radiobutton(
            direction_frame,
            text="Против часовой стрелки",
            variable=self.direction_var,
            value="counterclockwise",
            command=self.update_direction
        ).pack(anchor=tk.W)
        
        # Motor info panel
        info_frame = ttk.LabelFrame(control_frame, text="Состояние двигателя", padding="10")
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Status indicator
        self.status_label = tk.Label(
            info_frame,
            text="⏹ Остановлен",
            font=("Arial", 11),
            fg="#A3BE8C",
            bg="#3B4252"
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Real-time info
        self.info_text = tk.Text(
            info_frame,
            height=5,
            width=30,
            bg="#4C566A",
            fg="#D8DEE9",
            font=("Courier", 10),
            relief=tk.FLAT,
            state="normal"
        )
        self.info_text.pack(fill=tk.X)
        
        # Add scrollbar to info text
        info_scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        # Bind events
        self.speed_slider.bind("<B1-Motion>", self.on_speed_change)
        self.speed_slider.bind("<ButtonRelease-1>", self.on_speed_change)
        
        # Initial update
        self.update_displays()
    
    def on_speed_change(self, event=None):
        """Handle speed slider changes"""
        new_speed = self.speed_var.get()
        self.motor_state.target_speed = new_speed
        self.speed_display.config(text=f"{int(new_speed)} RPM")
        
        # Smooth acceleration simulation
        self.motor_state.actual_speed = self.lerp(
            self.motor_state.actual_speed,
            new_speed,
            0.1
        )
        
        self.update_displays()
    
    def lerp(self, a: float, b: float, t: float) -> float:
        """Linear interpolation"""
        return a + (b - a) * t
    
    def update_direction(self):
        """Update rotation direction"""
        if self.direction_var.get() == "clockwise":
            self.motor_state.direction = RotationDirection.CLOCKWISE
        else:
            self.motor_state.direction = RotationDirection.COUNTERCLOCKWISE
    
    def start_motor(self):
        """Start the motor"""
        self.motor_state.running = True
        self.status_label.config(text="▶ Запущен", fg="#A3BE8C")
        self.start_btn.state(['disabled'])
        self.stop_btn.state(['!disabled'])
        
        # Log event
        self.log_info("Двигатель запущен")
    
    def stop_motor(self):
        """Stop the motor"""
        self.motor_state.running = False
        self.status_label.config(text="⏹ Остановлен", fg="#BF616A")
        self.start_btn.state(['!disabled'])
        self.stop_btn.state(['disabled'])
        
        # Smooth stop
        self.motor_state.target_speed = 0
        self.speed_var.set(0)
        self.speed_display.config(text="0 RPM")
        
        # Log event
        self.log_info("Двигатель остановлен")
    
    def log_info(self, message: str):
        """Add message to info panel"""
        timestamp = time.strftime("%H:%M:%S")
        self.info_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.info_text.see(tk.END)
        
        # Keep only last 10 lines
        lines = self.info_text.get("1.0", tk.END).split("\n")
        if len(lines) > 11:
            self.info_text.delete("1.0", f"{len(lines)-10}.0")
    
    def update_displays(self):
        """Update all displays"""
        # Update gauge
        self.gauge.update_needle(
            self.motor_state.actual_speed,
            self.motor_state.current_angle
        )
        
        # Update info panel periodically
        if random.random() < 0.05:  # 5% chance each frame
            self.log_info(f"Текущая скорость: {self.motor_state.actual_speed:.1f} RPM")
    
    def update_loop(self):
        """Main animation loop"""
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        if self.motor_state.running and self.animation_running:
            # Update motor angle based on speed and direction
            speed_factor = self.motor_state.actual_speed / 60.0  # Convert RPM to RPS
            angle_change = speed_factor * 360 * delta_time * self.motor_state.direction.value
            self.motor_state.current_angle += angle_change
            
            # Smooth speed changes
            self.motor_state.actual_speed = self.lerp(
                self.motor_state.actual_speed,
                self.motor_state.target_speed,
                0.2
            )
        else:
            # When not running, still allow speed changes via slider
            self.motor_state.actual_speed = self.lerp(
                self.motor_state.actual_speed,
                self.motor_state.target_speed,
                0.2
            )
        
        # Update displays
        self.update_displays()
        
        # Continue loop
        self.after(16, self.update_loop)
    
    def on_closing(self):
        """Handle window closing"""
        self.animation_running = False
        self.destroy()

def main():
    app = StepperMotorApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()
