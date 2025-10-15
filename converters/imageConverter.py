import os
from PIL import Image
import cairosvg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkComponents.Tooltip import Tooltip

# imageConverter


def convert_image(input_file, output_format):

    print(f"Trying co convert image: {input_file}, to: {output_format}")
    if not input_file:
        tk.messagebox.showwarning("No file selected", "Please select an input file before proceeding.")
        return
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
    if input_ext == ".svg" and output_format in [".png", ".jpg", ".jpeg", ".ico"]:
        cairosvg.svg2png(url=input_file, write_to=output_file)
    elif input_ext in [".png", ".jpg", ".jpeg", ".ico"] and output_format == ".svg":
        messagebox.showerror("Error", ("Conversion from raster (.png, .jpg, .jpeg, .ico)"
                                       "to SVG is not supported in this program."))
    else:
        with Image.open(input_file) as img:
            img.save(output_file)
        messagebox.showinfo("Success", f"File saved as: {output_file}")


def select_file(entry_widget):
    filename = filedialog.askopenfilename()
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)
    # else:
        # tk.messagebox.showwarning("No file selected", "No file was selected. Please choose an input file.")


def create_image_tab(tab_control):
    tab_image = ttk.Frame(tab_control)
    tab_control.add(tab_image, text="Image Conversion")
    messages = {
        ".png": "PNG - A widely used image format that supports lossless compression and transparency.",
        ".jpg": "JPG - A commonly used image format that offers lossy compression, ideal for photographs.",
        ".jpeg": (
            "JPEG - Similar to JPG, it's a popular format for compressing "
            "digital images with minimal quality loss."
        ),
        ".ico": "ICO - A format used for icons, often seen in computer programs and websites.",
        ".svg": (
            "SVG - A vector image format ideal for graphics that can "
            "scale without losing quality, commonly used on the web."
        )
    }

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

    formats = [".png", ".jpg", ".jpeg", ".ico"]

    # Dodajemy przyciski radiowe i tooltipy
    for i, ext in enumerate(formats):
        rb = ttk.Radiobutton(format_frame, text=ext, variable=output_format, value=ext)
        rb.grid(column=i, row=0, padx=15, pady=10)
        Tooltip(rb, messages[ext])

    # Convert button
    ttk.Button(tab_image, text="Convert",
               command=lambda: convert_image(input_file_entry.get(), output_format.get())).grid(column=0, row=2,
                                                                                                columnspan=3, pady=20)
