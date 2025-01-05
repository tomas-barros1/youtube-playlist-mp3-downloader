import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
from queue import Queue
from yt_dlp import YoutubeDL
import sys


class MyLogger:
    def debug(self, msg):
        print(f'Debug: {msg}')

    def warning(self, msg):
        print(f'Warning: {msg}')

    def error(self, msg):
        print(f'Error: {msg}')


def download_and_convert(url, output_dir, progress_queue):
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'cookiesfrombrowser': ('chrome', 'firefox', 'edge', 'opera', 'brave', 'safari', 'vivaldi'),
        'quiet': False,
        'verbose': True,
        'ignoreerrors': True,
        'no_warnings': True,
        'logger': MyLogger(),
    }

    try:
        subprocess.run([sys.executable, "-m", "pip", "install",
                       "--upgrade", "yt-dlp"], capture_output=True)

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            videos = info.get('entries', [])

            if not videos:
                raise Exception("Nenhum vídeo encontrado na playlist")

            total_videos = len(videos)
            progress_queue.put(
                {'status': 'playlist_info', 'total_files': total_videos})

            for index, video in enumerate(videos, 1):
                if not video:
                    continue

                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                try:
                    ydl.download([video_url])
                    progress_queue.put(
                        {'status': 'downloading', 'downloaded_bytes': index, 'total_files': total_videos})
                except Exception as e:
                    print(f"Error downloading {video_url}: {e}")
                    continue

            progress_queue.put({'status': 'finished'})

    except Exception as e:
        progress_queue.put({'status': 'error', 'error_message': str(e)})


def start_download(url, output_folder, progress_var, status_label):
    if not url or not output_folder:
        messagebox.showerror(
            'Erro', 'Insira o link da playlist e selecione a pasta de destino.')
        return

    status_label.config(text="Iniciando download...")
    progress_queue = Queue()

    Thread(target=update_progress, args=(progress_queue,
           progress_var, status_label), daemon=True).start()
    Thread(target=download_and_convert, args=(
        url, output_folder, progress_queue), daemon=True).start()


def update_progress(progress_queue, progress_var, status_label):
    total_files, completed_files = 0, 0

    while True:
        if not progress_queue.empty():
            progress_data = progress_queue.get()

            if progress_data.get('status') == 'error':
                status_label.config(
                    text=f"Erro: {progress_data.get('error_message')}")
                break
            elif progress_data.get('status') == 'finished':
                status_label.config(text="Download concluído!")
                break
            elif progress_data.get('status') == 'playlist_info':
                total_files = progress_data.get('total_files', 1)
            elif progress_data.get('status') == 'downloading':
                downloaded = progress_data.get('downloaded_bytes', 0)
                if total_files > 0:
                    progress_var.set((downloaded / total_files) * 100)
                    status_label.config(text=f"Progresso: {
                                        downloaded}/{total_files}")


def select_output_folder(folder_var):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)
        with open("last_folder.txt", "w") as f:
            f.write(folder_selected)


def load_last_folder():
    if os.path.exists("last_folder.txt"):
        with open("last_folder.txt", "r") as f:
            return f.read().strip()
    return ""


def create_gui():
    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("600x500")
    root.configure(bg="#f0f0f0")

    last_folder = load_last_folder()

    center_frame = tk.Frame(root, bg="#f0f0f0")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(center_frame, text="Link da Playlist:",
             bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    url_entry = tk.Entry(center_frame, width=50, bd=2,
                         relief="groove", font=("Arial", 12))
    url_entry.pack(pady=5)

    tk.Label(center_frame, text="Pasta de Destino:",
             bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    folder_var = tk.StringVar(value=last_folder)
    tk.Entry(center_frame, textvariable=folder_var, width=40, bd=2,
             relief="groove", font=("Arial", 12)).pack(pady=5)
    tk.Button(center_frame, text="Selecionar", command=lambda: select_output_folder(
        folder_var), bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    progress_var = tk.DoubleVar()
    ttk.Progressbar(center_frame, orient="horizontal", length=400,
                    mode="determinate", variable=progress_var).pack(pady=10)

    status_label = tk.Label(
        center_frame, text="Aguardando...", bg="#f0f0f0", font=("Arial", 10))
    status_label.pack(pady=5)

    tk.Button(center_frame, text="Baixar", bg="#4CAF50", fg="white", command=lambda: start_download(
        url_entry.get(), folder_var.get(), progress_var, status_label), font=("Arial", 12, "bold")).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
