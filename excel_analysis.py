import numpy as np
import pandas as pd
import sys
from sys import argv
import os
from pathlib import Path

def selected_average(df, start_cmt, end_cmt, path):
    print("\nExtracting average:\nFrom:\t".upper() + start_cmt + " to " + end_cmt)

    start_idx = (df[df.columns[-1]].values == start_cmt).argmax()
    end_idx = (df[df.columns[-1]].values == end_cmt).argmax()
    print("Start, end index:".upper(), start_idx, end_idx)
    print("################################################")

    sel_df = df[start_idx:end_idx+1]            # +1 to take the comment

    stats = []
    # stats.append(df.columns[3:-1])
    stats.append(df.columns[4:-1])              # remove first 4 columns // and remove cmt text

    help = []
    for i in range(len(stats[0])):
        col = sel_df[stats[0][i]].dropna()
        f = col.mean()
        help.append(f)
    stats.append(help)

    for s in stats:
        print(s)

    df2 = pd.DataFrame(stats)
    # Printing to excel:
    # df2.to_excel("../output/" + start_cmt + "_" + end_cmt + ".xlsx")

    # Creating/appending to csv
    df2.insert(0, '', start_cmt + " " + end_cmt)        # inserts name of section to start of df

    # if file doesn't exist, add the header then save
    output = Path(path + "_output.csv")
    if output.is_file():
        print(output, "exists, appending to end of file")
        df2.iloc[[1]].to_csv(output, mode = 'a', index = False, header = None)
    # otherwise, append to end of file
    else:
        print("Creating new file: ", output)
        df2.to_csv(output, mode = 'a', index = False, header = None)

def save():
    print()

def selected_min_averages(df, start_cmt, end_cmt):

    averages = []
    averages.append(['s_time', 'e_time', 's_idx', 'e_idx'])

    # find index corresponding to first instance of start and end comments
    start_idx = (df[df.columns[-1]].values == start_cmt).argmax()
    end_idx = (df[df.columns[-1]].values == end_cmt).argmax()

    h = start_idx
    t_start = df[df.columns[0]][start_idx]      # df.columns[0] should be sel start
    t_end = df[df.columns[0]][end_idx]
    int_t = int(t_start)                        # time (in s) of start comment
    int_te = int(t_end)                         # time (in s) of end comment

    # gets the times and indices associated with comment
    while(int_t + 60 <= int_te+1):
        try:
            t = []

            t.append(int_t)
            print('Time: ', int_t, end=" - ")

            next_t = int_t + 60
            inext_t = str(next_t)
            t.append(inext_t)
            print(inext_t, end=" at i = ")

            t.append(h)

            # convert sel start column to all string (number --> string)
            str_t = df['Sel Start'].apply(str)
            idx = df[str_t.astype(str).str.startswith(inext_t)]

            i = idx.index[0]
            t.append(i)
            print(i)

            h = i
            int_t = next_t
            averages.append(t)

        except:
            # includes the last section (non-full minute)
            t.append(end_idx)
            averages.append(t)
            break

    print()
    print(int_te)
    print('############################')

    # print(averages)
    for col in averages:
        print(col)

    stats = []
    # stats.append(df.columns[3:-1])
    stats.append(df.columns[4:-1])

    for c in range(len(averages)+1):
        d = c+1
        try:
            help = []

            first = int(averages[d][2])
            next = int(averages[d][3])

            for i in range(len(stats[0])):
                col = df[first:next][stats[0][i]].dropna()
                f = col.mean()
                help.append(f)
            stats.append(help)
        except:
            break

    for s in stats:
        print(s)

    df1 = pd.DataFrame(averages)
    df2 = pd.DataFrame(stats)
    df_concat = pd.concat([df1, df2], axis=1)
    df_concat.to_excel("../output/" + start_cmt + "_" + end_cmt + "_min" + ".xlsx")

def get_comments(df, show_comments):
    cmts = df[df.columns[-1]].unique()

    if show_comments:
        for i, cmt in enumerate(cmts):
            print(i, end="\t")
            print(cmt)

    return(cmts)

def view(df, s, e):
    t_start = (df[df.columns[-1]].values == s).argmax()
    t_end = (df[df.columns[-1]].values == e).argmax()
    print(t_start, t_end)

    range = df[t_start:t_end+1]
    print(range)

def main():
    try:
        path = sys.argv[1]
        print("Analysing:".upper(), path)
        sheetname = "Sheet1"
        df = pd.read_excel(path, sheet_name="Sheet2")
        path = os.path.splitext(path)[0]
    except:
        print("First argument must be valid path to excel file.")
        exit(1)

    try:
        opt = sys.argv[2]
    except:
        print("Missing option argument\n-h for help and list of accepted arguments")
        exit(1)

    df=df.dropna(axis=1,how='all')
    args = ['-c', '-v', '-a', '-sa', '-m', '-sm', '-h']

    if (opt not in args):
        print("Invalid argument\n-h for help and list of accepted arguments")
        exit(1)

    try:
        if opt == "-c":
            cmts = get_comments(df, True)
            exit(1)

        cmts = get_comments(df, False)

        if opt == "-v":
            try:                        view(df, cmts[int(sys.argv[3])], cmts[int(sys.argv[4])])
            except Exception as e:
                print(e)
                print("Usage: excel_analysis.py [sheet name] -v [start comment index] [end comment index]")
            exit(1)

        if opt == "-h":
            print('''Valid arguments:
            c - get comments: -c
            v - view section: -v [comment start index] [end index]
            sa - returns averages of selected range: -sa [comment start index] [end index]
            sm - returns averages per minute of selected range: -sm [comment start index] [end index]\n''')
            exit(0)

        if opt == "-sa":
            try:
                start_cmt = cmts[int(sys.argv[3])]
                end_cmt = cmts[int(sys.argv[4])]
            except:
                print("No argument provided for start and/or end comment")
                exit(1)
            selected_average(df, start_cmt, end_cmt, path)

        if opt == "-sm":
            try:
                start_cmt = cmts[int(sys.argv[3])]
                end_cmt = cmts[int(sys.argv[4])]
            except:
                print("No argument provided for start and/or end comment")
                exit(1)
            selected_min_averages(df, start_cmt, end_cmt)


    except Exception as e:
        print("Error:", e)
        print("-h for help and list of accepted arguments")
        pass


if __name__ == '__main__':
    sys.exit(main())
