# LabChart-Excel-Helper
for SB data analysis

### Excel Sheet Setup:
- Get data from LabChart datapad - select all data, and select data points by event marker (BP)
- Copy to excel sheet from datapad
- Delete units (s, mean, etc)
- First row should be header (ex. Sel Start	Sel End	Sel Duration	MAP	SBP	DBP	HR	Cmt Text)
- Select all --> Filter
- Filter by comment:
  - Remove all BP VALUES (MAP	SBP	DBP) associated with PHYSIO/CAL comments
  - Remove all COMMENTS (not data) associated with TEMP comments (optional, this is just so comment list is shorter during use)
- Change path to excel file and sheetname in main (inside excel_analysis_1.py)
- *if the time ever restarts,* separate the new times into new sheets

### General Usage:
- In terminal, go to the folder (`cd`) containing `excel_analysis.py`
- Run the script using `python excel_analysis.py [excel file name] [option]`
- using the `-h` option will show list of accepted arguments
- example: `python excel_analysis.py SB_test_file.xlsx -h`

### Example Usage:
- Start by getting a numbered list of comments: `python excel_analysis.py SB_test_file.xlsx -c`

### Output:
- outputs to excel file in ../output
- output file name changes based on `[option]`

### Etc
- *** potential error in SM: can't find the associated time (start time) because it was deleted (CAL wave) --> need to manually fix this in excel input
