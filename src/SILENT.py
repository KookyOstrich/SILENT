import tkinter as tk
from tkinter import messagebox
import pyautogui
import win32gui
import win32con
import time
from PIL import Image, ImageTk
import os
import sys

class ModernTeamsMute:
    def __init__(self):
        self.is_muted = False
        
        # メインウィンドウの設定
        self.root = tk.Tk()
        self.root.title("SILENT")
        self.root.geometry("450x280")  # ウィンドウサイズを縮小
        self.root.configure(bg='#2C2F33')
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        self.setup_window_drag()
        self.create_ui()

    def create_ui(self):
        # タイトルバーフレーム
        title_frame = tk.Frame(self.root, bg='#23272A', height=30)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        # タイトルラベル
        title_label = tk.Label(
            title_frame, 
            text="SILENT",
            bg='#23272A',
            fg='white',
            font=('Helvetica', 10)
        )
        title_label.pack(side='left', padx=10, pady=5)

        # 閉じるボタン
        close_button = tk.Button(
            title_frame,
            text='×',
            command=self.root.destroy,
            bg='#23272A',
            fg='white',
            bd=0,
            font=('Helvetica', 12),
            activebackground='#ff0000',
            activeforeground='white',
            width=2
        )
        close_button.pack(side='right', padx=2)

        # メインコンテンツフレーム
        main_frame = tk.Frame(self.root, bg='#2C2F33')
        main_frame.pack(fill='both', expand=True)

        # ステータス表示
        self.status_label = tk.Label(
            main_frame,
            text="  TALKING🎙️",
            font=('Helvetica', 18, 'bold'),
            bg='#2C2F33',
            fg='#43B581',
            width=12,  # 幅を固定
            anchor='center',  # テキストを中央揃えに
            justify='center'  # 複数行の場合も中央揃え
        )
        self.status_label.pack(pady=(20, 10), padx=10)

        # ミュートボタン
        self.mute_button = tk.Button(
            main_frame,
            text="Toggle Mute",
            command=self.toggle_mute,
            bg='#7289DA',
            fg='white',
            font=('Helvetica', 12),
            relief='flat',
            activebackground='#677BC4',
            activeforeground='white',
            width=12,
            height=2
        )
        self.mute_button.pack(pady=10)

        # ステータスインジケーター
        self.status_indicator = tk.Canvas(
            main_frame,
            width=80,
            height=80,
            bg='#2C2F33',
            highlightthickness=0
        )
        self.status_indicator.pack(pady=10)
        self.draw_status_indicator()

    def draw_status_indicator(self):
        self.status_indicator.delete('all')
        color = '#43B581' if not self.is_muted else '#F04747'
        
        # 外側の円
        self.status_indicator.create_oval(5, 5, 75, 75, 
                                        fill='', outline=color, width=3)
        
        # 内側の円
        self.status_indicator.create_oval(20, 20, 60, 60, 
                                        fill=color, outline='')

    def find_teams_window(self):
        def callback(hwnd, teams_windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Microsoft Teams" in window_text:
                    teams_windows.append(hwnd)
            return True

        teams_windows = []
        win32gui.EnumWindows(callback, teams_windows)
        return teams_windows[0] if teams_windows else None

    def toggle_mute(self):
        try:
            teams_hwnd = self.find_teams_window()
            if not teams_hwnd:
                messagebox.showerror("Error", "Microsoft Teams window not found!")
                return

            current_window = win32gui.GetForegroundWindow()

            # 現在のウィンドウ状態を取得
            placement = win32gui.GetWindowPlacement(teams_hwnd)
            
            # 最大化状態を保持したままフォーカスを設定
            win32gui.SetForegroundWindow(teams_hwnd)
            time.sleep(0.2)

            self.is_muted = not self.is_muted
            pyautogui.hotkey('ctrl', 'shift', 'm')

            if self.is_muted:
                self.status_label.config(text="QUIET📵", fg='#F04747')
                self.mute_button.config(bg='#F04747')
            else:
                self.status_label.config(text="  TALKING🎙️", fg='#43B581')
                self.mute_button.config(bg='#7289DA')

            self.draw_status_indicator()

            time.sleep(0.2)
            win32gui.SetForegroundWindow(current_window)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle mute: {str(e)}")

    def setup_window_drag(self):
        self.drag_data = {"x": 0, "y": 0, "item": None}

        def start_drag(event):
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

        def drag(event):
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")

        self.root.bind("<Button-1>", start_drag)
        self.root.bind("<B1-Motion>", drag)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernTeamsMute()
    app.run()