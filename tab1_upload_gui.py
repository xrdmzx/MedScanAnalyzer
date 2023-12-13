import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil
import scan_save
import sqlite3

def open_file(image_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        destination_folder = "scans_folder"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_path = os.path.join(destination_folder, os.path.basename(file_path))
        global newpath
        newpath = shutil.copy(file_path, destination_path)

        # Image
        basewidth = 300
        img = Image.open(file_path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)  # Image size 
        img = ImageTk.PhotoImage(img)
        image_label.pack(padx=10, pady=10)
        image_label.config(image=img)
        image_label.image = img


def upload_gui(upload_tab):
    scan_upload_tab_frame = ttk.Frame(upload_tab)
    scan_upload_tab_frame.pack(fill='both', expand=True)

    left_frame = ttk.Frame(scan_upload_tab_frame)
    left_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20)

    right_frame = ttk.Frame(scan_upload_tab_frame)
    right_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)

    image_label = tk.Label(left_frame)
    image_label.pack(padx=10, pady=10)

    upload_button = tk.Button(left_frame, text="Upload Scan File", command=lambda: open_file(image_label))
    upload_button.pack(padx=10, pady=10)

    info_frame = tk.Frame(right_frame)
    info_frame.pack(padx=30, pady=10)

    username_label = tk.Label(info_frame, text="Username: ", font=('Helvetica', 14))
    username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    username_entry = tk.Entry(info_frame, font=('Helvetica', 14))
    username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    scan_type_label = tk.Label(info_frame, text="Scan Type: ", font=('Helvetica', 14))
    scan_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    scan_type_entry = ttk.Entry(info_frame, font=('Helvetica', 14))
    scan_type_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    category_label = tk.Label(info_frame, text="Category: ", font=('Helvetica', 14))
    category_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    category_entry = ttk.Entry(info_frame, font=('Helvetica', 14))
    category_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    comments_label = tk.Label(info_frame, text="Comments: ", font=('Helvetica', 14))
    comments_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    comments_entry = tk.Text(info_frame, height=5, width=30, font=('Helvetica', 14))
    comments_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    conn = sqlite3.connect('msa.sqlite');
    conn.execute("""CREATE TABLE   IF NOT EXISTS   scans (
                     scan_id INTEGER PRIMARY KEY,
                     uploader VARCHAR(20) NOT NULL, 
                     filepath TEXT NOT NULL,
                     scan_type TEXT,
                     category TEXT,
                     comment TEXT);
                     """);
    conn.commit();

    save_button = tk.Button(info_frame, text="Save", 
                            command=lambda: scan_save.scan_save(username_entry.get(),newpath, scan_type_entry.get(),category_entry.get(), comments_entry.get("1.0", tk.END), 
                                                                ))
    save_button.grid(row=4, columnspan=2, padx=10, pady=10, sticky="s")
