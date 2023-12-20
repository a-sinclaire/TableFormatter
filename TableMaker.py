# Amelia Sinclaire 2023
# openpyxl
# pandas
# pysimplegui
import pandas as pd
import re
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import PySimpleGUI as sg
import os
script_path = os.path.dirname(__file__)

test_input = '''# A tibble: 11 × 7
     age risk_set event censored fail_density  hazard survivor
   <dbl>    <dbl> <dbl>    <dbl>        <dbl>   <dbl>    <dbl>
 1    12    19790    25     1975       0.0627 0.00126    0.999
 2    13    17790    23     1952       0.0576 0.00129    0.997
 3    14    15815    39     1913       0.0977 0.00247    0.995
 4    15    13863    59     1854       0.148  0.00426    0.991
 5    16    11950    53     1801       0.133  0.00444    0.986
 6    17    10096    51     1750       0.128  0.00505    0.981
 7    18     8295    77     1673       0.193  0.00928    0.972
 8    19     6545    26     1647       0.0652 0.00397    0.968
 9    20     4872    28     1619       0.0702 0.00575    0.963
10    21     3225    13     1606       0.0326 0.00403    0.959
11    22     1606     5     1601       0.0125 0.00311    0.956'''


def generate_df(input_string):
    new_input = '\n'.join([x.strip() for x in input_string.split('\n')])
    new_input = re.sub(r'[ \t]+', ',', new_input).strip().split('\n')
    cleaned = []
    for line in new_input:
        if line.strip()[0] == '#':  # ignore first line
            continue
        if line.strip()[0] == "<":  # ignore data type line
            continue
        # remove line numbers (first occurrence of digit)
        line = re.sub(r'\d+,', '', line, 1).strip()
        cleaned.append(line)
    clean_str = '\n'.join(cleaned)
    df = pd.read_csv(StringIO(clean_str))
    return df


def main():
    sg.theme('DarkAmber')
    layout = [[sg.Text('Enter data string:'), sg.InputText()],
              [sg.Button('Generate')]]
    window = sg.Window('Table Maker', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Generate':
            df = generate_df(values[0])
            print(df)
            filename = sg.tk.filedialog.asksaveasfilename(
                defaultextension='xlsx',
                initialdir=script_path,
                initialfile='unnamed.xlsx',
                parent=window.TKroot,
                title='Save As'
            )
            df.to_excel(filename, index=False)
    window.close()


if __name__ == '__main__':
    main()
