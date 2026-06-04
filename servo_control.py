# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import serial
from serial.tools import list_ports

class ServoControlApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("舵机控制系统")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b")
        
        self.ser = None
        self.servo_vars = [tk.IntVar(value=90) for _ in range(5)]
        self.auto_send = tk.BooleanVar(value=True)
        
        self.create_ui()
        
    def create_ui(self):
        tk.Label(self.root, text="舵机控制系统", font=("Arial", 20, "bold"),
                fg="white", bg="#2b2b2b").pack(pady=15)
        
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        servo_frame = tk.LabelFrame(main, text="舵机角度控制 (0-180)", 
                                    font=("Arial", 12), fg="white",
                                    bg="#3c3c3c", padx=10, pady=10)
        servo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.servo_sliders = []
        self.servo_entries = []
        self.servo_value_labels = []
        
        for i in range(5):
            row = ttk.Frame(servo_frame)
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(row, text=f"舵机 {i}:", font=("Arial", 11), 
                    fg="#6af", bg="#3c3c3c", width=8).pack(side=tk.LEFT)
            
            slider = ttk.Scale(row, from_=0, to=180, orient=tk.HORIZONTAL,
                             variable=self.servo_vars[i], length=200,
                             command=lambda v, idx=i: self.on_slider_change(idx))
            slider.pack(side=tk.LEFT, padx=5)
            self.servo_sliders.append(slider)
            
            entry = ttk.Entry(row, textvariable=self.servo_vars[i], 
                            width=5, font=("Arial", 11), justify="center")
            entry.pack(side=tk.LEFT, padx=5)
            entry.bind('<Return>', lambda e, idx=i: self.on_entry_change(idx))
            entry.bind('<FocusOut>', lambda e, idx=i: self.on_entry_change(idx))
            self.servo_entries.append(entry)
            
            lbl = tk.Label(row, text="90°", font=("Arial", 11, "bold"),
                          fg="#6f6", bg="#3c3c3c", width=6)
            lbl.pack(side=tk.LEFT, padx=5)
            self.servo_value_labels.append(lbl)
        
        ctrl_frame = tk.LabelFrame(main, text="控制面板", font=("Arial", 12),
                                   fg="white", bg="#3c3c3c", padx=10, pady=10)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        
        port_row = ttk.Frame(ctrl_frame)
        port_row.pack(fill=tk.X, pady=5)
        
        tk.Label(port_row, text="串口:", font=("Arial", 10), 
                fg="white", bg="#3c3c3c").pack(side=tk.LEFT)
        
        self.port_combo = ttk.Combobox(port_row, width=12, state="readonly")
        self.port_combo.pack(side=tk.LEFT, padx=5)
        self.refresh_ports()
        
        ttk.Button(port_row, text="刷新", command=self.refresh_ports,
                  width=6).pack(side=tk.LEFT, padx=2)
        
        self.conn_btn = ttk.Button(port_row, text="连接", 
                                   command=self.toggle_connection, width=6)
        self.conn_btn.pack(side=tk.LEFT)
        
        self.conn_label = tk.Label(port_row, text="未连接", fg="#f66",
                                   bg="#3c3c3c", font=("Arial", 9))
        self.conn_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Checkbutton(ctrl_frame, text="自动发送数据", 
                       variable=self.auto_send).pack(pady=10)
        
        preset_frame = ttk.Frame(ctrl_frame)
        preset_frame.pack(pady=10)
        
        for angle in [0, 45, 90, 135, 180]:
            ttk.Button(preset_frame, text=f"{angle}°",
                      command=lambda a=angle: self.set_all(a),
                      width=6).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(ctrl_frame, text="发送数据", 
                  command=self.send_data, width=15).pack(pady=10)
        
        ttk.Button(ctrl_frame, text="重置", 
                  command=lambda: self.set_all(90), width=15).pack()
        
        self.status = tk.Text(ctrl_frame, height=6, width=25,
                             font=("Courier", 9), bg="#1a1a1a", fg="#0f0")
        self.status.pack(pady=10)
        
        self.update_display()
        
    def on_slider_change(self, idx):
        try:
            val = self.servo_vars[idx].get()
            self.servo_value_labels[idx].config(text=f"{val}°")
            self.update_display()
        except:
            pass
    
    def on_entry_change(self, idx):
        try:
            val = self.servo_vars[idx].get()
            val = max(0, min(180, val))
            self.servo_vars[idx].set(val)
            self.servo_sliders[idx].set(val)
            self.servo_value_labels[idx].config(text=f"{val}°")
            self.update_display()
        except:
            pass
    
    def update_display(self):
        angles = [v.get() for v in self.servo_vars]
        self.status.delete("1.0", tk.END)
        self.status.insert(tk.END, f"舵机角度:\n")
        for i, a in enumerate(angles):
            self.status.insert(tk.END, f"  舵机{i}: {a}°\n")
        self.status.insert(tk.END, f"\n串口状态: {'已连接' if self.ser and self.ser.is_open else '未连接'}")
        
        if self.auto_send.get() and self.ser and self.ser.is_open:
            self.send_data()
    
    def refresh_ports(self):
        ports = list(list_ports.comports())
        self.port_combo['values'] = [p.device for p in ports] if ports else ['无可用串口']
        if ports:
            self.port_combo.current(0)
    
    def toggle_connection(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.conn_label.config(text="未连接", fg="#f66")
            self.conn_btn.config(text="连接")
        else:
            port = self.port_combo.get()
            if port and port != '无可用串口':
                try:
                    self.ser = serial.Serial(port, 9600, timeout=1)
                    self.conn_label.config(text="已连接", fg="#6f6")
                    self.conn_btn.config(text="断开")
                    self.update_display()
                except Exception as e:
                    self.conn_label.config(text="连接失败", fg="#f66")
    
    def send_data(self):
        if self.ser and self.ser.is_open:
            try:
                angles = [v.get() for v in self.servo_vars]
                # 格式: 舵机号 角度
                # 例如: 0 90
                data = f"{angles[0]} {angles[1]} {angles[2]} {angles[3]} {angles[4]}\n"
                self.ser.write(data.encode())
            except:
                pass
    
    def set_all(self, angle):
        for v in self.servo_vars:
            v.set(angle)
        for s in self.servo_sliders:
            s.set(angle)
        self.update_display()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ServoControlApp()
    app.run()
