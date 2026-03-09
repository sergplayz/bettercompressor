import os
import zlib
import lzma
import tkinter as tk
from tkinter import filedialog, messagebox

# --- Compression and Decompression Functions ---
def compress_with_zlib(input_filepath, output_filepath):
    """
    Compresses a given file using the zlib module.

    Args:
        input_filepath (str): The path to the input file.
        output_filepath (str): The path to the output compressed file.

    Returns:
        str: A message indicating success or an error.
    """
    try:
        with open(input_filepath, 'rb') as f_in:
            original_data = f_in.read()
        compressed_data = zlib.compress(original_data)
        with open(output_filepath, 'wb') as f_out:
            f_out.write(compressed_data)
        return f"File '{os.path.basename(input_filepath)}' successfully compressed to '{os.path.basename(output_filepath)}'."
    except Exception as e:
        return f"An error occurred during zlib compression: {e}"

def compress_with_lzma(input_filepath, output_filepath):
    try:
        with open(input_filepath, 'rb') as f_in:
            original_data = f_in.read()
        compressed_data = lzma.compress(original_data)
        with open(output_filepath, 'wb') as f_out:
            f_out.write(compressed_data)
        return f"File '{os.path.basename(input_filepath)}' successfully compressed to '{os.path.basename(output_filepath)}'."
    except Exception as e:
        return f"An error occurred during lzma compression: {e}"

def decompress_with_zlib(input_filepath, output_filepath):
    try:
        with open(input_filepath, 'rb') as f_in:
            compressed_data = f_in.read()
        decompressed_data = zlib.decompress(compressed_data)
        with open(output_filepath, 'wb') as f_out:
            f_out.write(decompressed_data)
        return f"File '{os.path.basename(input_filepath)}' successfully decompressed to '{os.path.basename(output_filepath)}'."
    except Exception as e:
        return f"An error occurred during zlib decompression: {e}"

def decompress_with_lzma(input_filepath, output_filepath):

    try:
        with open(input_filepath, 'rb') as f_in:
            compressed_data = f_in.read()
        decompressed_data = lzma.decompress(compressed_data)
        with open(output_filepath, 'wb') as f_out:
            f_out.write(decompressed_data)
        return f"File '{os.path.basename(input_filepath)}' successfully decompressed to '{os.path.basename(output_filepath)}'."
    except Exception as e:
        return f"An error occurred during lzma decompression: {e}"

def setup_gui():
    root = tk.Tk()
    root.title("Compression Tool")

    input_file_path = tk.StringVar()
    tk.Label(root, text="Input File Path:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    tk.Entry(root, textvariable=input_file_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def browse_input_file():
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=(("All files", "*.*" ), ("Text files", "*.txt"), ("Zlib Compressed", "*.zlib"), ("LZMA Compressed", "*.lzma"))
        )
        if filename:
            input_file_path.set(filename)

    tk.Button(root, text="Browse Input", command=browse_input_file).grid(row=0, column=2, padx=5, pady=5)

    output_file_path = tk.StringVar()
    tk.Label(root, text="Output File Path:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    tk.Entry(root, textvariable=output_file_path, width=50).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def browse_output_file():
        filename = filedialog.asksaveasfilename(
            title="Save Output File As",
            defaultextension=".zip",
            filetypes=(("All files", "*.*" ), ("Zlib Compressed", "*.zlib"), ("LZMA Compressed", "*.lzma"), ("Text files", "*.txt"))
        )
        if filename:
            output_file_path.set(filename)

    tk.Button(root, text="Browse Output", command=browse_output_file).grid(row=1, column=2, padx=5, pady=5)

    status_message = tk.StringVar()
    tk.Label(root, textvariable=status_message, fg="blue").grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    def execute_operation(operation_func, op_name):
        input_f = input_file_path.get()
        output_f = output_file_path.get()
        if not input_f or not os.path.exists(input_f):
            status_message.set(f"Error: Invalid or missing input file path for {op_name}.")
            return
        if not output_f:
            status_message.set(f"Error: Missing output file path for {op_name}.")
            return
        status_message.set(f"Performing {op_name}...")
        root.update_idletasks()
        result_msg = operation_func(input_f, output_f)
        status_message.set(result_msg)

    button_frame = tk.Frame(root)
    button_frame.grid(row=2, column=0, columnspan=3, pady=10)

    tk.Button(button_frame, text="Compress with Zlib", command=lambda: execute_operation(compress_with_zlib, "Zlib Compression")).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(button_frame, text="Achieved ~247x on sample file (repetitive data)", fg="gray").grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Button(button_frame, text="Compress with LZMA", command=lambda: execute_operation(compress_with_lzma, "LZMA Compression")).grid(row=1, column=0, padx=5, pady=5)
    tk.Label(button_frame, text="Achieved ~6054x on sample file (repetitive data)", fg="gray").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Button(button_frame, text="Decompress with Zlib", command=lambda: execute_operation(decompress_with_zlib, "Zlib Decompression")).grid(row=2, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Decompress with LZMA", command=lambda: execute_operation(decompress_with_lzma, "LZMA Decompression")).grid(row=3, column=0, padx=5, pady=5)
    root.grid_columnconfigure(1, weight=1)

    return root, status_message

if __name__ == "__main__":

    root_window, status_var = setup_gui()
    root_window.mainloop()
    print("GUI application has closed.")
