import tkinter as tk
from tkinter import filedialog, scrolledtext
import ffmpeg


def check_file(input_file, output_text):
    # Sprawdzenie czy plik istnieje i pobranie jego informacji
    try:
        file_info = ffmpeg.probe(input_file)

        # Wypisywanie wyników w oknie tekstowym
        output_text.insert(tk.END,
                           f"File: {file_info['format']['filename']} | Size: {file_info['format']['size']} bytes\n")
        output_text.insert(tk.END, f"Duration: {file_info['format']['duration']} seconds\n")
        output_text.insert(tk.END, f"Bitrate: {file_info['format']['bit_rate']} bps\n")
    except ffmpeg.Error as e:
        output_text.insert(tk.END, f"Error while probing the file: {e.stderr}\n")


def select_input_file(entry_widget):
    filename = filedialog.askopenfilename()
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)


def create_gui():
    root = tk.Tk()
    root.title("File Checker")

    # Input file selection
    tk.Label(root, text="Select File:").grid(column=0, row=0, padx=10, pady=10)
    input_file_entry = tk.Entry(root, width=50)
    input_file_entry.grid(column=1, row=0, padx=10, pady=10)
    tk.Button(root, text="Browse", command=lambda: select_input_file(input_file_entry)).grid(column=2, row=0, padx=10,
                                                                                             pady=10)

    # Output text area
    output_text = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
    output_text.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

    # Check file button
    tk.Button(root, text="Check File", command=lambda: check_file(input_file_entry.get(), output_text)).grid(column=0,
                                                                                                             row=2,
                                                                                                             columnspan=3,
                                                                                                             padx=10,
                                                                                                             pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
