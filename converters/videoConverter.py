import tkinter as tk
from tkinter import ttk, filedialog
import ffmpeg
from tkComponents.Tooltip import Tooltip


def select_file(entry_widget):
    filename = filedialog.askopenfilename()
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)
        update_bitrate_options(filename)  # Update available bitrates
        update_resolution_options(filename)  # Update available resolutions
    else:
        tk.messagebox.showwarning("No file selected", "No file was selected. Please choose an input file.")


def get_video_resolution(input_file):
    try:
        probe = ffmpeg.probe(input_file)
        video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return width, height
    except Exception as e:
        print(f"Error, can not read video resoultion: {e}")
        return None, None


def get_video_bitrate(input_file):
    try:
        probe = ffmpeg.probe(input_file)
        video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        bitrate = int(int(video_stream['bit_rate']) / 1000)  # Konwersja na kbps
        return bitrate
    except Exception as e:
        print(f"Error can not read video bitrate: {e}")
        return None


# def update_bitrate_options(input_file):
#     if not input_file:
#         options = ["File not chosen..."]
#         bitrate_var.set(options[0])
#     else:
#         original_bitrate = get_video_bitrate(input_file)
#         options = [f"Same as input ({original_bitrate} kbps)"] if original_bitrate else ["Same as input"]
#         options.extend([f"{bitrate} kbps" for bitrate in ["500", "1000", "1500", "2000", "2500", "3000"]])
#         bitrate_var.set(options[0])
#
#     bitrate_menu['menu'].delete(0, 'end')
#     for option in options:
#         bitrate_menu['menu'].add_command(label=option, command=tk._setit(bitrate_var, option))

def update_bitrate_options(input_file):
    if not input_file:
        options = ["File not chosen..."]
        bitrate_var.set(options[0])
    else:
        original_bitrate = get_video_bitrate(input_file)
        options = [f"Same as input ({original_bitrate} kbps)"] if original_bitrate else ["Same as input"]
        options.extend([f"{bitrate} kbps" for bitrate in ["500", "1000", "1500", "2000", "2500", "3000"]])
        bitrate_var.set(options[0])

    bitrate_menu['menu'].delete(0, 'end')
    for option in options:
        bitrate_menu['menu'].add_command(label=option, command=tk._setit(bitrate_var, option))


def update_resolution_options(input_file):
    if not input_file:
        options = ["File not chosen..."]
        resolution_var.set(options[0])
    else:
        width, height = get_video_resolution(input_file)
        if width and height:
            aspect_ratio = width / height
            if abs(aspect_ratio - 16/9) < 0.01:
                options = [f"Same as input ({width}x{height})", "1920x1080", "1280x720", "854x480", "640x360"]
            elif abs(aspect_ratio - 4/3) < 0.01:
                options = [f"Same as input ({width}x{height})", "1024x768", "800x600", "640x480"]
            else:
                options = [f"Same as input ({width}x{height})", f"{width}x{height} (Original)"]

            resolution_var.set(options[0])
        else:
            options = ["Choose file..."]
            resolution_var.set(options[0])

    resolution_menu['menu'].delete(0, 'end')
    for option in options:
        resolution_menu['menu'].add_command(label=option, command=tk._setit(resolution_var, option))


def create_video_tab(tab_control):
    global bitrate_var, bitrate_menu, resolution_var, resolution_menu

    tab_video = ttk.Frame(tab_control)
    tab_control.add(tab_video, text="Video Conversion")
    messages = {
        ".mp4": "MP4 - A popular format used in streaming and on mobile devices.",
        ".avi": "AVI - An older video format still commonly used on Windows systems.",
        ".mov": "MOV - An Apple format often used in video editing.",
        ".mkv": "MKV - A container format supporting multiple audio tracks and subtitles.",
        ".webm": "WebM - A format optimized for use on the internet."
    }

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

    formats = [".mp4", ".avi", ".mov", ".mkv", ".webm"]

    for i, ext in enumerate(formats):
        rb = ttk.Radiobutton(format_frame, text=ext, variable=output_format, value=ext)
        rb.grid(column=i, row=0, padx=15, pady=10)
        Tooltip(rb, messages[ext])
    toggle_button_width = 25
    default_message = "File not chosen..."

    # Bitrate and Resolution
    bitrate_var = tk.StringVar(value=default_message)
    resolution_var = tk.StringVar(value=default_message)

    ttk.Label(tab_video, text="Bitrate (kbps):").grid(column=0, row=2, padx=10, pady=10)

    bitrate_menu = ttk.OptionMenu(tab_video, bitrate_var, default_message, default_message)
    bitrate_menu.config(width=toggle_button_width)
    bitrate_menu.grid(column=1, row=2, padx=10, pady=10)

    ttk.Label(tab_video, text="Resolution:").grid(column=0, row=3, padx=10, pady=10)
    resolution_menu = ttk.OptionMenu(tab_video, resolution_var, default_message, default_message)
    resolution_menu.config(width=toggle_button_width)
    resolution_menu.grid(column=1, row=3, padx=10, pady=10)

    # Inicjalizacja wartości "Choose file..."
    update_bitrate_options(None)
    update_resolution_options(None)

    # Convert button
    ttk.Button(tab_video, text="Convert",
               command=lambda: convert_video(input_file_entry.get(), output_format.get(),
                                             bitrate_var.get(), resolution_var.get())).grid(column=0, row=4,
                                                                                            columnspan=3, pady=20)


def convert_video(input_file, output_format, bitrate, resolution):
    if not input_file:
        tk.messagebox.showwarning("No file selected", "Please select an input file before proceeding.")
        return

    # If bitrate is "Same as input", retrieve it from the input file
    if "Same as input" in bitrate:
        bitrate = get_video_bitrate(input_file)
        if bitrate is None:
            tk.messagebox.showerror("Error", "Unable to retrieve bitrate from the input file.")
            return
    if "kbps" in bitrate:
        bitrate = bitrate.replace(" kbps", "k")

    # If resolution is "Same as input", retrieve it from the input file
    if "Same as input" in resolution:
        width, height = get_video_resolution(input_file)
        if width is None or height is None:
            tk.messagebox.showerror("Error", "Unable to retrieve resolution from the input file.")
            return
        resolution = f"{width}x{height}"

    print(f"Converting file to: {output_format}, bitrate: {bitrate}, resolution: {resolution}")

    # Ask the user for the output file location and name
    output_file = filedialog.asksaveasfilename(
        defaultextension=output_format,
        filetypes=[("Video files", f"*{output_format}"), ("All files", "*.*")],
        title="Select the location to save the converted file"
    )

    if not output_file:  # If the user canceled the save dialog
        tk.messagebox.showinfo("Canceled", "The conversion operation has been canceled.")
        return

    # Prepare FFmpeg arguments
    ffmpeg_args = {
        'video_bitrate': f'{bitrate}' if bitrate else None,
    }

    # Set the resolution if it's not "Same as input"
    if resolution:
        ffmpeg_args['s'] = resolution

    # Build the FFmpeg command
    ffmpeg_command = ffmpeg.input(input_file).output(output_file, **ffmpeg_args)

    # Execute the command
    try:
        ffmpeg_command.run(overwrite_output=True)
        tk.messagebox.showinfo("Conversion Complete", f"Conversion finished successfully! File saved as: {output_file}")
    except ffmpeg.Error as e:
        tk.messagebox.showerror("Error", f"An error occurred during conversion: {e.stderr}")
