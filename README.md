# Medical Scan Analyzer Guide
# Code Authors: Ian Kratzinger, Ronald Zambrano, Jhansi Bhaskarla

Medical Scan Analyzer is a Python GUI that can be used to upload medical images.
Users can then rate these images and view the ratings that other users have left.

## Installation
1. Install the most recent version of [Python](https://www.python.org/downloads/)
2. The following modules in the standard Python library are used:
   * **os** (operating system interfacing)
   * **sys** (system-specific functions)
   * **shutil** (file management)
   * **tkinter** (GUI building)
   * **sqlite3** (database management)
3. This app also makes use of the **pillow** (PIL) module for image management
   * To install pillow, run the bmes.py file contained in this folder
4. If you want to view the database contents, install [SQLiteStudio](https://github.com/pawelsalawa/sqlitestudio/releases/tag/3.3.3)

## Functions

* **main.py**: Runs the application and builds the base GUI
* **tab1\_upload\_gui.py**: GUI for creating the Scan Upload tab and submitting scan form
* **tab2\_rate\_gui.py**: GUI for creating the Rate Scans tab and submitting the rating form
* **tab3\_feedback\_gui.py**: GUI for creating the View Ratings tab
* **tab4\_help\_gui.py**: GUI for creating the help tab
* **scan\_save.py**: Takes an uploaded scan and stores its information in the database
* **rating\_save.py**: Takes a completed rating form and stores the submission in the database
* **bmes.py**: Installs pillow module
