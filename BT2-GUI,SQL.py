import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import psycopg2
from datetime import datetime

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x300")
        self.root.config(bg="#1f1f1f")

        mixer.init()

        self.is_paused = False
        self.current_file = None

        # Kết nối với PostgreSQL
        self.conn = psycopg2.connect(
            dbname="music_player",  # Tên cơ sở dữ liệu
            user="postgres",        # Tên người dùng
            password="12345",    # Mật khẩu
            host="localhost",       # Địa chỉ host
            port="5432"             # Cổng
        )
        self.cursor = self.conn.cursor()

        # Title label
        self.label = tk.Label(self.root, text="Music Player", font=("Helvetica", 24, "bold"), bg="#1f1f1f", fg="#f0f0f0")
        self.label.pack(pady=20)

        # Frame for buttons
        self.button_frame = tk.Frame(self.root, bg="#1f1f1f")
        self.button_frame.pack(pady=10)

        # Play button
        self.play_button = tk.Button(self.button_frame, text="Play", command=self.play_music, font=("Helvetica", 12), width=10, bg="#28a745", fg="white")
        self.play_button.grid(row=0, column=0, padx=10)

        # Pause button
        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.pause_music, font=("Helvetica", 12), width=10, bg="#ffc107", fg="black")
        self.pause_button.grid(row=0, column=1, padx=10)

        # Stop button
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_music, font=("Helvetica", 12), width=10, bg="#dc3545", fg="white")
        self.stop_button.grid(row=0, column=2, padx=10)

        # Open file button
        self.open_button = tk.Button(self.root, text="Open File", command=self.open_file, font=("Helvetica", 12), width=15, bg="#007bff", fg="white")
        self.open_button.pack(pady=10)

        # File Label
        self.file_label = tk.Label(self.root, text="No file selected", font=("Helvetica", 10), bg="#1f1f1f", fg="#f0f0f0")
        self.file_label.pack(pady=5)

    def play_music(self):
        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
        else:
            if self.current_file:
                mixer.music.load(self.current_file)
                mixer.music.play()
                self.file_label.config(text=f"Now playing: {self.current_file.split('/')[-1]}")
                self.save_song_to_db(self.current_file)
            else:
                self.open_file()

    def pause_music(self):
        if not self.is_paused:
            mixer.music.pause()
            self.is_paused = True

    def stop_music(self):
        mixer.music.stop()
        self.file_label.config(text="No file selected")

    def open_file(self):
        self.current_file = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp3 *.wav")])
        if self.current_file:
            self.play_music()

    def save_song_to_db(self, song_file):
        song_name = song_file.split("/")[-1]  # Lấy tên bài hát từ đường dẫn
        play_time = datetime.now()  # Thời gian phát bài hát
        query = "INSERT INTO songs (song_name, play_time) VALUES (%s, %s)"
        self.cursor.execute(query, (song_name, play_time))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
