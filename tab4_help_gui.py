import tkinter as tk
import webbrowser

def open_github_readme():
    url = 'https://github.com/xrdmzx/MedScanAnalyzer'
    webbrowser.open_new(url)

def help_gui(help_tab):
    open_readme_button = tk.Button(help_tab, text="Open GitHub README", command=open_github_readme)
    open_readme_button.pack(padx=20, pady=20)
