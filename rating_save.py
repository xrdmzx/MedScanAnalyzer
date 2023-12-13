import tkinter as tk
from tkinter import ttk
import sqlite3

# Function to create and connect to the SQLite3 database
def rating_save(rater, quality, disease, comment, scan_id):
    # Connect to the SQLite3 database (or create it if it doesn't exist)
    conn = sqlite3.connect('msa.sqlite');
    cur = conn.cursor();

    conn.execute("""CREATE TABLE   IF NOT EXISTS   ratings (
    rating_id INTEGER PRIMARY KEY,
    rater VARCHAR(20),
    quality VARCHAR(20), 
    disease VARCHAR(20),
    comment TEXT,
    scan_id INTEGER,
    FOREIGN KEY(scan_id) REFERENCES scans(scan_id));
    """);
    conn.commit();
    conn.commit()
    conn.execute("INSERT INTO ratings(rater, quality, disease, comment, scan_id) \
                 VALUES (?, ?, ?, ?, ?)",
                 (rater, quality, disease, comment, scan_id));

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Rating submitted to database successfully!")

