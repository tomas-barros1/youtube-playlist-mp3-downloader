import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
from threading import Thread
from queue import Queue
from yt_dlp import YoutubeDL


class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")

        if os.path.exists("icon.ico"):
            self.root.iconbitmap("icon.ico")

        self.center_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.create_widgets()

        self.progress_queue = Queue()

    def create_widgets(self):
        tk.Label(self.center_frame, text="Playlist URL:",
                 bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.url_entry = tk.Entry(
            self.center_frame, width=50, font=("Arial", 12))
        self.url_entry.pack(pady=5)

        tk.Label(self.center_frame, text="Output Folder:",
                 bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.folder_var = tk.StringVar()
        tk.Entry(self.center_frame, textvariable=self.folder_var,
                 width=40, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.center_frame, text="Browse", command=self.select_output_folder,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        tk.Label(self.center_frame, text="Select Browser for Cookies:",
                 bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
        self.browser_var = StringVar()
        self.browser_var.set("None")
        browsers = ["None", "chrome", "firefox", "edge", "opera", "brave"]
        self.browser_dropdown = ttk.Combobox(
            self.center_frame, textvariable=self.browser_var, values=browsers, state="readonly", font=("Arial", 12))
        self.browser_dropdown.pack(pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.center_frame, orient="horizontal", length=400, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        self.status_label = tk.Label(
            self.center_frame, text="Waiting...", bg="#f0f0f0", font=("Arial", 10))
        self.status_label.pack(pady=5)

        tk.Button(self.center_frame, text="Download", command=self.start_download,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

    def select_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_var.set(folder_selected)

    def start_download(self):
        url = self.url_entry.get()
        output_folder = self.folder_var.get()

        if not url or not output_folder:
            messagebox.showerror(
                "Error", "Please enter a playlist URL and select an output folder.")
            return

        browser = self.browser_var.get()
        if browser == "None":
            browser = None

        self.status_label.config(text="Starting download...")
        Thread(target=self.download_and_convert, args=(
            url, output_folder, browser), daemon=True).start()
        self.update_progress()

    def download_and_convert(self, url, output_folder, browser):
        ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'quiet': False,
            'verbose': True,
            'ignoreerrors': True,
            'no_warnings': True,
        }

        if browser:
            ydl_opts['cookiesfrombrowser'] = (browser,)

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                videos = info.get('entries', [])

                if not videos:
                    self.progress_queue.put(
                        {'status': 'error', 'error_message': "No videos found in the playlist."})
                    return

                total_videos = len(videos)
                self.progress_queue.put(
                    {'status': 'playlist_info', 'total_files': total_videos})

                for index, video in enumerate(videos, 1):
                    if not video:
                        continue

                    video_url = f"https://www.youtube.com/watch?v={
                        video['id']}"
                    try:
                        ydl.download([video_url])
                        self.progress_queue.put(
                            {'status': 'downloading', 'downloaded_bytes': index, 'total_files': total_videos})
                    except Exception as e:
                        print(f"Error downloading {video_url}: {e}")
                        continue

                self.progress_queue.put({'status': 'finished'})

        except Exception as e:
            self.progress_queue.put(
                {'status': 'error', 'error_message': str(e)})

    def update_progress(self):
        if not self.progress_queue.empty():
            progress_data = self.progress_queue.get()

            if progress_data.get('status') == 'error':
                self.status_label.config(
                    text=f"Error: {progress_data.get('error_message')}")
            elif progress_data.get('status') == 'finished':
                self.status_label.config(text="Download completed!")
                self.progress_var.set(100)
            elif progress_data.get('status') == 'playlist_info':
                self.total_files = progress_data.get('total_files', 1)
            elif progress_data.get('status') == 'downloading':
                downloaded = progress_data.get('downloaded_bytes', 0)
                if self.total_files > 0:
                    progress = (downloaded / self.total_files) * 100
                    self.progress_var.set(progress)
                    self.status_label.config(text=f"Downloading: {
                                             downloaded}/{self.total_files}")

        self.root.after(100, self.update_progress)


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloadApp(root)
    root.mainloop()
