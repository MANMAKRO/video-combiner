import tkinter as tk
from tkinter import filedialog, ttk
from moviepy.editor import VideoFileClip, concatenate_videoclips
from threading import Thread
import multiprocessing

def select_video1():
    global video1_path
    video1_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    video1_label.config(text=f"Selected: {video1_path}")

def select_video2():
    global video2_path
    video2_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    video2_label.config(text=f"Selected: {video2_path}")

def combine_videos():
    if video1_path and video2_path:
        cores = multiprocessing.cpu_count()  # Automatically use the maximum available cores
        video1 = VideoFileClip(video1_path)
        video2 = VideoFileClip(video2_path)
        combined = concatenate_videoclips([video1, video2], method="compose")
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        
        progress_label.config(text="Combining videos...")
        progress_bar.start()
        
        def process_videos():
            combined.write_videofile(
                save_path,
                codec="h264_nvenc",  # NVIDIA GPU accelerated codec
                audio_codec="aac",
                threads=cores,
                ffmpeg_params=["-preset", "slow", "-b:v", "5M"]
            )
            progress_bar.stop()
            progress_label.config(text="Videos combined successfully!")
        
        Thread(target=process_videos).start()

# Set up the main GUI window
root = tk.Tk()
root.title("Video Combiner")

video1_path = ""
video2_path = ""

# Create the GUI elements
video1_button = tk.Button(root, text="Select Video 1", command=select_video1)
video1_button.pack(pady=10)

video1_label = tk.Label(root, text="No video selected")
video1_label.pack()

video2_button = tk.Button(root, text="Select Video 2", command=select_video2)
video2_button.pack(pady=10)

video2_label = tk.Label(root, text="No video selected")
video2_label.pack()

combine_button = tk.Button(root, text="Combine Videos", command=combine_videos)
combine_button.pack(pady=20)

# Progress bar
progress_label = tk.Label(root, text="")
progress_label.pack()

progress_bar = ttk.Progressbar(root, mode="indeterminate")
progress_bar.pack(pady=10, fill=tk.X)

# Run the GUI loop
root.mainloop()
