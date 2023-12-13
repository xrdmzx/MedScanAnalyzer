import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import rating_save

def img_display(image_label,a):
        conn = sqlite3.connect('msa.sqlite');
        cur = conn.cursor()
        cur.execute("SELECT * FROM scans;");
        rows = cur.fetchall()
        if rows:
          if a < 0:
               a = len(rows)-1
          if a > len(rows)-1:
               a = 0
          file_path = str(rows[a][2])
          basewidth = 300
          img = Image.open(file_path)
          wpercent = (basewidth / float(img.size[0]))
          hsize = int((float(img.size[1])*float(wpercent)))
          img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS) 
          img = ImageTk.PhotoImage(img)
          image_label.pack(padx=10, pady=10)
          image_label.config(image=img)
          image_label.image = img
          # Set uploader
          uploader = str(rows[a][1])
          scan_type = str(rows[a][3])
          category = str(rows[a][4])
          scan_id = rows[a][0]
          return (uploader, scan_type, category, scan_id)
        
def next_command(rate_tab,rate_tab_frame,a):
     for child in rate_tab_frame.winfo_children():
          child.destroy()
     rate_tab_frame.destroy()
     a = a+1
     print(a)
     rate_gui(rate_tab,a)

def back_command(rate_tab,rate_tab_frame,a):
     for child in rate_tab_frame.winfo_children():
          child.destroy()
     rate_tab_frame.destroy()
     print(a)
     a = a-1
     rate_gui(rate_tab,a)

def rate_gui(rate_tab,a=0):

    rate_tab_frame = ttk.Frame(rate_tab)
    rate_tab_frame.pack(fill='both', expand=True)

    left_frame = ttk.Frame(rate_tab_frame)
    left_frame.place(relx = 0.02, rely= 0.02)

    right_frame = ttk.Frame(rate_tab_frame)
    right_frame.place(relx=0.4,rely=0.02)
    
    info_frame = right_frame

    uploader_label = tk.Label(info_frame, text="Uploader: ", font=('Helvetica', 14))
    uploader_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    uploader_var = tk.StringVar()
    uploader_entry = tk.Entry(info_frame, textvariable=uploader_var, state='disabled', font=('Helvetica', 14))
    uploader_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    rater_label = tk.Label(info_frame,text="Rater: ", font=('Helvetica', 14))
    rater_label.grid(row=1,column=0,padx=10,pady=5,sticky='w')
    rater_entry = tk.Entry(info_frame, font=('Helvetica', 14))
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
    quality_dropdown = ttk.Combobox(info_frame, textvariable=quality_var, values=["Very Good", "Good", "Fair","Poor","Very Poor"], state='readonly', font=('Helvetica', 14))
    quality_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    disease_label = tk.Label(info_frame, text="Disease: ", font=('Helvetica', 14))
    disease_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    disease_var = tk.StringVar()
    disease_dropdown = ttk.Combobox(info_frame, textvariable=disease_var, values=["Present", "Likely Present", "Unclear","Likely Abesnt","Absent"], state='readonly', font=('Helvetica', 14))
    disease_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    comments_label = tk.Label(info_frame, text="Comments: ", font=('Helvetica', 14))
    comments_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    comments_entry = tk.Text(info_frame, height=5, width=30, font=('Helvetica', 14))
    comments_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    image_label = tk.Label(left_frame)
    image_label.pack(padx=10, pady=10)

    scan_data = img_display(image_label,a)
    if scan_data:
         uploader_var.set(scan_data[0])
         scan_type_var.set(scan_data[1])
         category_var.set(scan_data[2])
         scan_id = scan_data[3]
    
    save_button = tk.Button(rate_tab, text="Save", font=('Helvetica', 14),
                            command=lambda: rating_save.rating_save(rater_entry.get(),quality_var.get(),disease_var.get(),comments_entry.get("1.0", tk.END),scan_id))
    save_button.place(relx=0.5,rely=0.85)

    next_button = tk.Button(rate_tab, text="Next", command=lambda: next_command(rate_tab,rate_tab_frame,a), font=('Helvetica', 14))
    next_button.place(relx=0.6,rely=0.85)

    back_button = tk.Button(rate_tab, text="Back", command=lambda: back_command(rate_tab,rate_tab_frame,a), font=('Helvetica', 14))
    back_button.place(relx=0.4,rely=0.85)