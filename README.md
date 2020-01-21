# LabChart-Excel-Helper
for SB data analysis

Cleaning excel from LabChart Datapad:
- Copy to excel sheet from datapad 
- Delete units (s, mean, etc)
- First row should be header (ex. Sel Start	Sel End	Sel Duration	MAP	SBP	DBP	HR	Cmt Text)
- Select all --> Filter
- Filter by comment 
-- Remove all ROWS associated with CAL comments
-- Remove all COMMENTS (not data) associated with TEMP comments (optional, this is just so comment list is shorter during use)
- Change path to excel file and sheetname in main (inside excel_analysis_1.py)
- *if there time ever restarts,* separate the new times into new sheets 

Use:
- > excel_analysis_1.py c
- h for help and list of accepted arguments (ignore the rounding prompt)
- change the path to excel INSIDE python file (bad practice I know)
- *** potential error in SM: can't find the associated time (start time) because it was deleted (CAL wave) --> need to manually fix this in excel input 

> excel_analysis_1.py [options]

Output:
- outputs to excel file in ../output
- output file name changes based on [option]
