import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import cairosvg
import os
from moviepy.editor import VideoFileClip


def convert_image(input_file, output_format):
    input_ext = os.path.splitext(input_file)[1].lower()
    output_file = filedialog.asksaveasfilename(
        defaultextension=output_format,
        filetypes=[
            (f"{output_format.upper()} files", f"*{output_format}"),
            ("All files", "*.*")
        ]
    )

    if not output_file:
        return
    if input_ext == ".svg"and output_format in [".png", ".jpg", ".jpeg", ".ico"]:
        cairosvg.svg2png(url=input_file, write_to=output_file)
    elif input_ext in [".png", ".jpg", ".jpeg", ".ico"] and output_format == ".svg":
        messagebox.showerror("Error", "Conversion from raster to SVG is not supported in this program.")
    else:
        with Image.open(input_file) as img:
            img.save(output_file)
        messagebox.showinfo("Success", f"File saved as: {output_file}")


def convert_video(input_file, output_format):
    input_ext = os.path.splitext(input_file)[1].lower()
    output_file = filedialog.asksaveasfilename(
        defaultextension=output_format,
        filetypes=[
            (f"{output_format.upper()} files", f"*{output_format}"),
            ("All files", "*.*")
        ]
    )

    if not output_file:
        return
    if input_ext == ".avi"and output_format == ".mp4":
        video = VideoFileClip(input_file)
        video.write_videofile(output_file, codec="libx264")
    elif input_ext == ".mp4"and output_format == ".avi":
        video = VideoFileClip(input_file)
        video.write_videofile(output_file, codec="png")
    else:
        messagebox.showerror("Error", "This video conversion is not supported.")
        return

    messagebox.showinfo("Success", f"File saved as: {output_file}")


def select_file(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


def create_image_tab(tab_control):
    tab_image = ttk.Frame(tab_control)
    tab_control.add(tab_image, text="Image Conversion")

    # Input file
    ttk.Label(tab_image, text="Input file:").grid(column=0, row=0, padx=10, pady=10)
    input_file_entry = ttk.Entry(tab_image, width=40)
    input_file_entry.grid(column=1, row=0, padx=10, pady=10)
    ttk.Button(tab_image, text="Select file", command=lambda: select_file(input_file_entry)).grid(column=2, row=0,
                                                                                                  padx=10, pady=10)

    # Output format
    format_frame = ttk.LabelFrame(tab_image, text="Output format:")
    format_frame.grid(column=0, row=1, columnspan=3, padx=10, pady=10, sticky="ew")

    output_format = tk.StringVar(value=".png")

    formats = [".png", ".jpg", ".jpeg", ".ico", ".svg"]

    for i, format in enumerate(formats):
        ttk.Radiobutton(format_frame, text=format.upper(), variable=output_format, value=format).grid(column=i, row=0,
                                                                                                      padx=15, pady=10)

    # Convert button
    ttk.Button(tab_image, text="Convert",
               command=lambda: convert_image(input_file_entry.get(), output_format.get())).grid(column=0, row=2,
                                                                                                columnspan=3, pady=20)


def create_video_tab(tab_control):
    tab_video = ttk.Frame(tab_control)
    tab_control.add(tab_video, text="Video Conversion")

    # Input file
    ttk.Label(tab_video, text="Input file:").grid(column=0, row=0, padx=10, pady=10)
    input_file_entry = ttk.Entry(tab_video, width=40)
    input_file_entry.grid(column=1, row=0, padx=10, pady=10)
    ttk.Button(tab_video, text="Select file", command=lambda: select_file(input_file_entry)).grid(column=2, row=0,
                                                                                                  padx=10, pady=10)

    # Output format
    format_frame = ttk.LabelFrame(tab_video, text="Output format:")
    format_frame.grid(column=0, row=1, columnspan=3, padx=10, pady=10, sticky="ew")

    output_format = tk.StringVar(value=".mp4")

    formats = [".mp4", ".avi"]

    for i, format in enumerate(formats):
        ttk.Radiobutton(format_frame, text=format.upper(), variable=output_format, value=format).grid(column=i, row=0,
                                                                                                      padx=15, pady=10)

    # Convert button
    ttk.Button(tab_video, text="Convert",
               command=lambda: convert_video(input_file_entry.get(), output_format.get())).grid(column=0, row=2,
                                                                                                columnspan=3, pady=20)


def main():
    root = tk.Tk()
    root.title("File Converter")

    tab_control = ttk.Notebook(root)
    create_image_tab(tab_control)
    create_video_tab(tab_control)
    tab_control.pack(expand=1, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
