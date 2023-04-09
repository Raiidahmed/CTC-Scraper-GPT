import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    location_column_label = tk.Label(settings_window, text="Location Column Index:")
    location_column_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    location_column_entry = tk.Entry(settings_window, width=10)
    location_column_entry.grid(row=0, column=1, padx=5, pady=5)
    location_column_entry.insert(0, "5")

    def save_settings():
        global location_column_index
        location_column_index = int(location_column_entry.get())
        settings_window.destroy()

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.grid(row=1, column=1, padx=5, pady=5)

def remove_duplicates_and_non_alphanumeric(text):
    words = re.findall(r'\b\w+\b', text)
    unique_words = list(dict.fromkeys(words))
    cleaned_text = ' '.join(unique_words)
    return cleaned_text


def browse_input_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    input_files_entry.delete(0, tk.END)
    input_files_entry.insert(0, ', '.join(file_paths))


def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)


def process_files():
    input_files = input_files_entry.get().split(', ')
    output_file = output_file_entry.get()

    if not input_files or not output_file:
        messagebox.showerror("Error", "Please specify input files and output file")
        return

    try:
        df = pd.concat([pd.read_csv(file) for file in input_files], ignore_index=True)

        # Process 'Start' and 'End' columns
        df['Start'], df['End'] = zip(*df['Start'].apply(lambda x: (x.split(' - ')[0], x.split(' - ')[1]) if isinstance(x, str) and ' - ' in x else (x, '')))

        # Process 'Location' column
        df.iloc[:, location_column_index] = df.iloc[:, location_column_index].apply(lambda x: remove_duplicates_and_non_alphanumeric(x) if isinstance(x, str) else x)

        # Save the modified dataframe to output.csv
        df.to_csv(output_file, index=False)

        messagebox.showinfo("Success", "Files have been processed successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing files: {str(e)}")


root = tk.Tk()
root.title("Data Processor")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

input_files_label = tk.Label(frame, text="Input Files:")
input_files_label.grid(row=0, column=0, sticky="w")
input_files_entry = tk.Entry(frame, width=50)
input_files_entry.grid(row=0, column=1)
input_files_button = tk.Button(frame, text="Browse", command=browse_input_files)
input_files_button.grid(row=0, column=2)

output_file_label = tk.Label(frame, text="Output File:")
output_file_label.grid(row=1, column=0, sticky="w")
output_file_entry = tk.Entry(frame, width=50)
output_file_entry.grid(row=1, column=1)
output_file_button = tk.Button(frame, text="Browse", command=browse_output_file)
output_file_button.grid(row=1, column=2)

process_button = tk.Button(frame, text="Process Files", command=process_files)
process_button.grid(row=2, column=1, pady=10)

menu_bar = tk.Menu(root)
settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Settings", command=open_settings)
menu_bar.add_cascade(label="Options", menu=settings_menu)
root.config(menu=menu_bar)
location_column_index = 5


root.mainloop()