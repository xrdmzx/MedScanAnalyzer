import tkinter as tk
from tkinter import ttk
import tab4_help_gui
import tab1_upload_gui
import tab2_rate_gui
import tab3_feedback_gui

root = tk.Tk()
root.title("Medical Scan Analyzer")
root.geometry("900x550")  # Size of the main window

title_label = tk.Label(root, text="MEDICAL SCAN ANALYZER", font=('Helvetica', 16))
title_label.pack()

tab_control = ttk.Notebook(root)

scan_upload_tab = ttk.Frame(tab_control)
rate_scans_tab = ttk.Frame(tab_control)
view_ratings_tab = ttk.Frame(tab_control)
help_tab = ttk.Frame(tab_control)

tab_control.add(scan_upload_tab, text='Scan Upload')
tab_control.add(rate_scans_tab, text='Rate Scans')
tab_control.add(view_ratings_tab, text='View Ratings')
tab_control.add(help_tab, text='Help')

tab_control.pack(fill='both', expand=True)

tab1_upload_gui.upload_gui(scan_upload_tab)
tab2_rate_gui.rate_gui(rate_scans_tab)
tab3_feedback_gui.feedback_gui(view_ratings_tab)
tab4_help_gui.help_gui(help_tab)

root.mainloop()

