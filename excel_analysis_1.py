import numpy as np
import pandas as pd
import sys
from sys import argv

def average(df):
    print("average method is not done yet")

def selected_average(df, start_cmt, end_cmt):
    print("\nExtracting average:\nFrom:\t" + start_cmt + " to " + end_cmt)

    start_idx = (df[df.columns[-1]].values == start_cmt).argmax()
    end_idx = (df[df.columns[-1]].values == end_cmt).argmax()
    print(start_idx, end_idx)

    sel_df = df[start_idx:end_idx+1]            # +1 to take the comment
    # print(sel_df)

    stats = []
    stats.append(df.columns[3:-1])              # remove sel start, end, duration // and remove cmt text

    help = []
    for i in range(len(stats[0])):
        f = sel_df[stats[0][i]].mean()
        help.append(f)
    stats.append(help)

    for s in stats:
        print(s)

    df2 = pd.DataFrame(stats)
    df2.to_excel("../output/" + start_cmt + "_" + end_cmt + ".xlsx")


def minute_averages(df):
    averages = []
    averages.append(['s_time', 'e_time', 's_idx', 'e_idx'])

    h = 0
    t_start = df['Sel Start'][0]
    int_t = int(t_start)

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
                f = df[first:next][stats[0][i]].mean()
                help.append(f)
            stats.append(help)
        except:
            break

    for s in stats:
        print(s)

    df1 = pd.DataFrame(averages)
    df2 = pd.DataFrame(stats)
    df_concat = pd.concat([df1, df2], axis=1)
    df_concat.to_excel("../output/output_averages.xlsx")

def selected_min_averages(df, start_cmt, end_cmt):

    averages = []
    averages.append(['s_time', 'e_time', 's_idx', 'e_idx'])

    # find index corresponding to first instance of start and end comments
    start_idx = (df[df.columns[-1]].values == start_cmt).argmax()
    end_idx = (df[df.columns[-1]].values == end_cmt).argmax()

    # change df size with indices
    df = df[start_idx:end_idx+1].copy()

    h = 0
    t_start = df[df.columns[0]][start_idx]      # df.columns[0] should be sel start
    int_t = int(t_start)


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
                f = df[first:next][stats[0][i]].mean()
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

    path = "../SB8_data_resp.xlsx"
    # df = pd.read_excel(path, sheet_name="RESPpd")
    df = pd.read_excel(path, sheet_name="rest of data")

    df=df.dropna(axis=1,how='all')

    print('Columns:' , df.columns)

    try:
        if sys.argv[1] == "c":
            cmts = get_comments(df, True)
            exit(1)

        cmts = get_comments(df, False)

        if sys.argv[1] == "v":
            try:
                view(df, cmts[int(sys.argv[2])], cmts[int(sys.argv[3])])
            except Exception as e:
                print(e)
            exit(1)

        if sys.argv[1] == "a":
            average(df)

        if sys.argv[1] == "sa":
            try:
                start_cmt = cmts[int(sys.argv[2])]
                end_cmt = cmts[int(sys.argv[3])]
            except:
                print("No argument provided for start and/or end comment")
                exit(1)
            selected_average(df, start_cmt, end_cmt)

        if sys.argv[1] == "m":
            minute_averages(df)

        if sys.argv[1] == "sm":
            try:
                start_cmt = cmts[int(sys.argv[2])]
                end_cmt = cmts[int(sys.argv[3])]
            except:
                print("No argument provided for start and/or end comment")
                exit(1)
            selected_min_averages(df, start_cmt, end_cmt)

        if sys.argv[1] == "h":
            print('''Valid arguments:
            c - get comments
            a - returns averages of entire range
            sa - returns averages of selected range (sa, start index, end index)
            m - returns average per minute of entire range
            sm - returns averages per minute of selected range (sm, start index, end index)\n''')
            exit(0)

    except Exception as e:
        print("Error:", e)

        print("-h for help and list of accepted arguments")
        pass


if __name__ == '__main__':
    sys.exit(main())
