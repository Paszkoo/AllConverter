import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkComponents.Tooltip import Tooltip
import ffmpeg

# audioConverter


def get_audio_bitrate(input_file):
    try:
        # Pobranie informacji o pliku za pomocą ffmpeg.probe
        probe = ffmpeg.probe(input_file)
        # Znalezienie pierwszego strumienia audio
        audio_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'audio')
        # Pobranie bitrate i konwersja na kbps
        bitrate = int(int(audio_stream['bit_rate']) / 1000)
        return bitrate
    except Exception as e:
        print(f"Error: cannot read audio bitrate: {e}")
        return None


def update_bitrate_options(input_file):
    if not input_file:
        options = ["File not chosen..."]
        bitrate_var.set(options[0])
    else:
        original_bitrate = get_audio_bitrate(input_file)
        options = [f"Same as input ({original_bitrate} kbps)"] if original_bitrate else ["Same as input"]
        options.extend([f"{bitrate} kbps" for bitrate in ["64", "96", "128", "192", "256", "320"]])
        bitrate_var.set(options[0])

    bitrate_menu['menu'].delete(0, 'end')
    for option in options:
        bitrate_menu['menu'].add_command(label=option, command=tk._setit(bitrate_var, option))

def convert_audio(input_file, output_format, bitrate):
    if not input_file:
        tk.messagebox.showwarning("No file selected", "Please select an input file before proceeding.")
        return
    if "Same as input" in bitrate:
        bitrate = get_audio_bitrate(input_file)
        if bitrate is None:
            tk.messagebox.showerror("Error", "Unable to retrieve bitrate from the input file.")
            return
    if "kbps" in bitrate:
        bitrate = bitrate.replace(" kbps", "k")


    input_ext = os.path.splitext(input_file)[1].lower()
    output_file = filedialog.asksaveasfilename(
        defaultextension=output_format,
        filetypes=[
            (f"{output_format} files", f"*{output_format}"),
            ("All files", "*.*")
        ]
    )

    if not output_file:
        return
    ffmpeg_args = {
        'video_bitrate': f'{bitrate}' if bitrate else None,
    }
    ffmpeg_command = ffmpeg.input(input_file).output(output_file, **ffmpeg_args)
    try:
        # Konwertowanie pliku audio przy użyciu ffmpeg
        ffmpeg_command.run(overwrite_output=True)
        messagebox.showinfo("Success", f"File saved as: {output_file}")
    except ffmpeg.Error as e:
        messagebox.showerror("Error", f"An error occurred during conversion: {e.stderr}")


def select_file(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)
        update_bitrate_options(filename)  # Update available bitrates
    # else:
        # tk.messagebox.showwarning("No file selected", "No file was selected. Please choose an input file.")


def create_audio_tab(tab_control):
    global bitrate_var, bitrate_menu
    tab_audio = ttk.Frame(tab_control)
    tab_control.add(tab_audio, text="Audio Conversion")
    messages = {
        ".mp3": "MP3 - A popular audio format known for its lossy compression, widely used in music files.",
        ".wav": "WAV - A lossless audio format, often used in professional recording and editing."
    }

    # Input file
    ttk.Label(tab_audio, text="Input file:").grid(column=0, row=0, padx=10, pady=10)
    input_file_entry = ttk.Entry(tab_audio, width=40)
    input_file_entry.grid(column=1, row=0, padx=10, pady=10)
    ttk.Button(tab_audio, text="Select file", command=lambda: select_file(input_file_entry)).grid(column=2, row=0,
                                                                                                  padx=10, pady=10)

    # Output format
    format_frame = ttk.LabelFrame(tab_audio, text="Output format:")
    format_frame.grid(column=0, row=1, columnspan=3, padx=10, pady=10, sticky="ew")

    output_format = tk.StringVar(value=".mp3")

    formats = [".mp3", ".wav"]
    toggle_button_width = 25

    # Dodajemy przyciski radiowe i tooltipy
    for i, ext in enumerate(formats):
        rb = ttk.Radiobutton(format_frame, text=ext, variable=output_format, value=ext)
        rb.grid(column=i, row=0, padx=15, pady=10)
        Tooltip(rb, messages[ext])

    # Bitrate selection
    ttk.Label(tab_audio, text="Bitrate (kbps):").grid(column=0, row=2, padx=10, pady=10)
    bitrate_var = tk.StringVar(value="128")
    bitrate_options = ["64", "96", "128", "192", "256", "320"]
    bitrate_menu = ttk.OptionMenu(tab_audio, bitrate_var, *bitrate_options)
    bitrate_menu.config(width=toggle_button_width)
    bitrate_menu.grid(column=1, row=2, padx=10, pady=10)

    update_bitrate_options(None)

    # Convert button
    ttk.Button(tab_audio, text="Convert",
               command=lambda: convert_audio(input_file_entry.get(), output_format.get(), bitrate_var.get())).grid(
        column=0, row=3, columnspan=3, pady=20)


