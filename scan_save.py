import tkinter as tk
from tkinter import ttk
import sqlite3

# Function to create and connect to the SQLite3 database
def scan_save(uploader, newpath, scan_type="N/A", category="N/A", comment="N/A"):
    # Connect to the SQLite3 database (or create it if it doesn't exist)
    conn = sqlite3.connect('msa.sqlite');
    cur = conn.cursor();

    conn.execute("""CREATE TABLE   IF NOT EXISTS   scans (
    scan_id INTEGER PRIMARY KEY,
    uploader VARCHAR(20) NOT NULL, 
    filepath TEXT NOT NULL,
    scan_type TEXT,
    category TEXT,
    comment TEXT);
    """);
    conn.commit();
    conn.commit()
    conn.execute("INSERT INTO scans(uploader, filepath, scan_type, category, comment) \
                 VALUES (?, ?, ?, ?, ?)",
                 (uploader, newpath, scan_type, category, comment));

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Scan uploaded successfully!")

