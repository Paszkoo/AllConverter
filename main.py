import tkinter as tk
from tkinter import ttk
from converters.videoConverter import create_video_tab
from converters.imageConverter import create_image_tab
from converters.audioConverter import create_audio_tab


def main():
    root = tk.Tk()
    root.title("File Converter")

    tab_control = ttk.Notebook(root)
    create_image_tab(tab_control)
    create_video_tab(tab_control)
    create_audio_tab(tab_control)
    tab_control.pack(expand=1, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
