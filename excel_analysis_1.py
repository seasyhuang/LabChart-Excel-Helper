import numpy as np
import pandas as pd
import sys
from sys import argv

def average(df, sheetname, bool_round):
    print("\nExtracting average from sheet: ", sheetname)

    stats = []
    stats.append(df.columns[3:-1])                          # remove sel start, end, duration // and remove cmt text

    help = []
    for i in range(len(stats[0])):
        # try:
        #     f = df[stats[0][i]].mean()    # stats[0][i] == "Resp Rate" --> "HR"
        # except:
        #     f = df[stats[0][i]][df[stats[0][i]]!=" "].mean()    # fuck whitespace
        try:
            col = df[stats[0][i]].dropna()    # stats[0][i] == "Resp Rate" --> "HR"
            if bool_round: f = rounded_mean(col)
            else:          f = col.mean()
        except:
            col = df[stats[0][i]][df[stats[0][i]]!=" "].dropna()    # fuck whitespace
            if bool_round: f = rounded_mean(col)
            else:          f = col.mean()
        help.append(f)
    stats.append(help)

    for s in stats:
        print(s)

    df2 = pd.DataFrame(stats)
    df2.to_excel("../output/" + sheetname + "_average" + ".xlsx")

def selected_average(df, start_cmt, end_cmt, bool_round):
    print("\nExtracting average:\nFrom:\t" + start_cmt + " to " + end_cmt)

    start_idx = (df[df.columns[-1]].values == start_cmt).argmax()
    end_idx = (df[df.columns[-1]].values == end_cmt).argmax()
    print(start_idx, end_idx)

    sel_df = df[start_idx:end_idx+1]            # +1 to take the comment

    stats = []
    # stats.append(df.columns[3:-1])              # remove sel start, end, duration // and remove cmt text
    stats.append(df.columns[2:-1])              # remove sel start, end // and remove cmt text

    print(stats)

    help = []
    for i in range(len(stats[0])):
        col = sel_df[stats[0][i]].dropna()
        if bool_round: f = rounded_mean(col)
        else:          f = col.mean()
        help.append(f)
    stats.append(help)

    for s in stats:
        print(s)

    df2 = pd.DataFrame(stats)
    df2.to_excel("../output/" + start_cmt + "_" + end_cmt + ".xlsx")

def minute_averages(df, sheetname, bool_round):
    averages = []
    averages.append(['s_time', 'e_time', 's_idx', 'e_idx'])

    h = 0
    t_start = df['Sel Start'][0]
    int_t = int(t_start)

    print("///")

    while(True):
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

            # first minute
            # print(df[h:i])
            h = i
            int_t = next_t
            averages.append(t)

        except:
            break

    print()
    print('############################')

    # print(averages)
    for col in averages:
        print(col)

    # col2 = ['Resp Rate', 'MAP', 'SBP', 'DBP', 'HR']   == df.columns[3:-1]

    stats = []
    stats.append(df.columns[3:-1])

    for c in range(len(averages)+1):
        d = c+1
        try:
            help = []

            first = int(averages[d][2])
            next = int(averages[d][3])

            for i in range(len(stats[0])):
                col = df[first:next][stats[0][i]].dropna()
                if bool_round: f = rounded_mean(col)
                else:          f = col.mean()
                help.append(f)
            stats.append(help)
        except:
            break

    for s in stats:
        print(s)

    df1 = pd.DataFrame(averages)
    df2 = pd.DataFrame(stats)
    df_concat = pd.concat([df1, df2], axis=1)
    df_concat.to_excel("../output/" + sheetname + "_min" + ".xlsx")

def selected_min_averages(df, start_cmt, end_cmt, bool_round):

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
    while(int_t + 60 <= int_te):
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
    print('############################')

    # print(averages)
    for col in averages:
        print(col)

    stats = []
    # stats.append(df.columns[3:-1])
    stats.append(df.columns[2:-1])

    for c in range(len(averages)+1):
        d = c+1
        try:
            help = []

            first = int(averages[d][2])
            next = int(averages[d][3])

            for i in range(len(stats[0])):
                col = df[first:next][stats[0][i]].dropna()
                if bool_round: f = rounded_mean(col)
                else:          f = col.mean()
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

def rounded_mean(col):
    # print(col.name)
    if col.name == 'Resp Rate':
        rmean = col.mean().astype(np.double).round(1)
    if col.name == 'MAP' or col.name == 'SBP' or col.name == 'DBP' or col.name == 'HR':
        rmean = col.mean().astype(np.double).round(0).astype(np.int)                     # convert to double then round to nearest int, then truncate .0 with np.int
    return rmean

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

    # path = "../Pilot_EJ_edit_EJ.xlsx"
    path = "../Pilot_SB_FH_12-17-2020_clean.xlsx"
    sheetname = "Sheet1"
    # sheetname = "RESPprotpd"
    df = pd.read_excel(path)#, sheet_name=sheetname)

    try:
        sys1 = sys.argv[1]
    except:
        print("Missing first argument\n-h for help and list of accepted arguments")
        exit(1)

    df=df.dropna(axis=1,how='all')
    args = ['-c', '-v', '-a', '-sa', '-m', '-sm', '-h']

    if (sys.argv[1] not in args):
        print("Invalid argument\n-h for help and list of accepted arguments")
        exit(1)

    # print('Columns:' , df.columns)

    try:
        if sys.argv[1] == "-c":
            cmts = get_comments(df, True)
            exit(1)

        cmts = get_comments(df, False)

        if sys.argv[1] == "-v":
            try:
                view(df, cmts[int(sys.argv[2])], cmts[int(sys.argv[3])])
            except Exception as e:
                print(e)
            exit(1)

        if sys.argv[1] == "-h":
            print('''Valid arguments:
            c - get comments
            a - returns averages of entire range
            sa - returns averages of selected range [sa, comment start index, end index]
            m - returns average per minute of entire range
            sm - returns averages per minute of selected range [sm, comment start index, end index]\n''')
            exit(0)

        # bool_round = input("Round values (Resp Rate --> to 1 decimal place; MAP, SBP, DBP, HR --> integer)? [Y/N] \t")
        # if bool_round.lower() == 'y':   bool_round = True
        # else:                           bool_round = False
        bool_round = False

        if sys.argv[1] == "-a":
            average(df, sheetname, bool_round)

        if sys.argv[1] == "-sa":
            try:
                start_cmt = cmts[int(sys.argv[2])]
                end_cmt = cmts[int(sys.argv[3])]
            except:
                print("No argument provided for start and/or end comment")
                exit(1)
            selected_average(df, start_cmt, end_cmt, bool_round)

        if sys.argv[1] == "-m":
            minute_averages(df, sheetname, bool_round)

        if sys.argv[1] == "-sm":
            try:
                start_cmt = cmts[int(sys.argv[2])]
                end_cmt = cmts[int(sys.argv[3])]
            except:
                print("No argument provided for start and/or end comment")
                exit(1)
            selected_min_averages(df, start_cmt, end_cmt, bool_round)


    except Exception as e:
        print("Error:", e)

        print("-h for help and list of accepted arguments")
        pass


if __name__ == '__main__':
    sys.exit(main())
