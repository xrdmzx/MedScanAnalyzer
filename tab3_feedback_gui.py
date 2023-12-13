import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

def rating_display(image_label,a):
      conn = sqlite3.connect('msa.sqlite');
      cur = conn.cursor();
      conn.execute("""CREATE TABLE   IF NOT EXISTS   ratings (
                   rating_id INTEGER PRIMARY KEY,
                   rater VARCHAR(20),
                   quality INTEGER, 
                   disease INTEGER,
                   comment TEXT,
                   scan_id INTEGER,
                   FOREIGN KEY(scan_id) REFERENCES scans(scan_id));
                   """);
      conn.commit();
      cur.execute("SELECT * FROM scans s, ratings r WHERE r.scan_id = s.scan_id;");
      rows = cur.fetchall()
      if rows:
               if a < 0:
                    a = len(rows)-1
               if a > len(rows)-1:
                    a = 0   
               file_path = rows[a][2]
               basewidth = 300
               img = Image.open(file_path)
               wpercent = (basewidth / float(img.size[0]))
               hsize = int((float(img.size[1])*float(wpercent)))
               img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)  # Image size 
               img = ImageTk.PhotoImage(img)
               image_label.pack(padx=10, pady=10)
               image_label.config(image=img)
               image_label.image = img
               
               uploader = str(rows[a][1])
               scan_type = str(rows[a][3])
               category = str(rows[a][4])
               rater = str(rows[a][7])
               quality = str(rows[a][8])
               disease = str(rows[a][9])
               comment = str(rows[a][10])
               return (uploader, scan_type, category, rater, quality, disease, comment)

def next_command(feedback_tab,feedback_tab_frame,a):
     for child in feedback_tab_frame.winfo_children():
          child.destroy()
     feedback_tab_frame.destroy()
     a = a+1
     print(a)
     feedback_gui(feedback_tab,a)

def back_command(feedback_tab,feedback_tab_frame,a):
     for child in feedback_tab_frame.winfo_children():
          child.destroy()
     feedback_tab_frame.destroy()
     print(a)
     a = a-1
     feedback_gui(feedback_tab,a)

def feedback_gui(feedback_tab,a=0):
    feedback_tab_frame = ttk.Frame(feedback_tab)
    feedback_tab_frame.pack(fill='both', expand=True)

    left_frame = ttk.Frame(feedback_tab_frame)
    left_frame.place(relx = 0.02, rely=0.02)

    right_frame = ttk.Frame(feedback_tab_frame)
    right_frame.place(relx=0.4, rely=0.02)

    info_frame = right_frame

    uploader_label = tk.Label(info_frame, text="Uploader: ", font=('Helvetica', 14))
    uploader_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    uploader_var = tk.StringVar()
    uploader_entry = tk.Entry(info_frame, textvariable=uploader_var, state='disabled', font=('Helvetica', 14))
    uploader_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    rater_label = tk.Label(info_frame,text="Rater: ", font=('Helvetica', 14))
    rater_label.grid(row=1,column=0,padx=10,pady=5,sticky='w')
    rater_var = tk.StringVar()
    rater_entry = tk.Entry(info_frame, textvariable=rater_var, state='disabled', font=('Helvetica', 14))
    rater_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    scan_type_label = tk.Label(info_frame, text="Scan Type: ", font=('Helvetica', 14))
    scan_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    scan_type_var = tk.StringVar()
    scan_type_entry = tk.Entry(info_frame, textvariable=scan_type_var, state='disabled', font=('Helvetica', 14))
    scan_type_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    category_label = tk.Label(info_frame, text="Category: ", font=('Helvetica', 14))
    category_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    category_var = tk.StringVar()
    category_entry = tk.Entry(info_frame, text=category_var, state='disabled', font=('Helvetica', 14))
    category_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    quality_label = tk.Label(info_frame, text="Quality: ", font=('Helvetica', 14))
    quality_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    quality_var = tk.StringVar()
    quality_dropdown = tk.Entry(info_frame, textvariable=quality_var, state='disabled', font=('Helvetica', 14))
    quality_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    disease_label = tk.Label(info_frame, text="Disease: ", font=('Helvetica', 14))
    disease_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    disease_var = tk.StringVar()
    disease_dropdown = tk.Entry(info_frame, textvariable=disease_var, state='disabled', font=('Helvetica', 14))
    disease_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    comments_label = tk.Label(info_frame, text="Comments: ", font=('Helvetica', 14))
    comments_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    comments_entry = tk.Text(info_frame, state='normal', height=5, width=30, font=('Helvetica', 14))
    comments_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    image_label = tk.Label(left_frame)
    image_label.pack(padx=10, pady=10)
    scan_data = rating_display(image_label,a)
    if scan_data:
        uploader_var.set(scan_data[0])
        scan_type_var.set(scan_data[1])
        category_var.set(scan_data[2])
        rater_var.set(scan_data[3])
        quality_var.set(scan_data[4])
        disease_var.set(scan_data[5])
        comments_entry.insert(tk.END,scan_data[6])

    next_button = tk.Button(feedback_tab, text="Next", command=lambda: next_command(feedback_tab,feedback_tab_frame,a), font=('Helvetica', 14))
    next_button.place(relx=0.55,rely=0.85)

    back_button = tk.Button(feedback_tab, text="Back", command=lambda: back_command(feedback_tab,feedback_tab_frame,a), font=('Helvetica', 14))
    back_button.place(relx=0.45,rely=0.85)