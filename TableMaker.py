# Amelia Sinclaire 2023
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

test_stargazer = '''
==================================================
                        Dependent variable:       
                  --------------------------------
                     Age of First Cigarette Use   
                     (1)        (2)        (3)    
--------------------------------------------------
factor(period)12  -4.369***                       
                    (.201)                        
factor(period)13  -4.441***                       
                    (.210)                        
factor(period)14  -3.893***                       
                    (.162)                        
factor(period)15  -3.448***                       
                    (.132)                        
factor(period)16  -3.526***                       
                    (.139)                        
factor(period)17  -3.536***                       
                    (.142)                        
factor(period)18  -3.079***                       
                    (.117)                        
factor(period)19  -4.149***                       
                    (.198)                        
factor(period)20  -4.057***                       
                    (.191)                        
factor(period)21  -4.817***                       
                    (.278)                        
factor(period)22  -5.769***                       
                    (.448)                        
period_center                  -.030      -.034   
                               (.016)     (.021)  
I(period_center2)                        -.068*** 
                                          (.008)  
Constant                     -3.888***  -3.367*** 
                               (.051)     (.067)  
--------------------------------------------------
Observations        19,790     19,790     19,790  
Log Likelihood    -1,888.145 -1,950.887 -1,900.639
Akaike Inf. Crit. 3,798.291  3,905.773  3,807.278 
==================================================
Note:                *p<0.05; **p<0.01; ***p<0.001'''


test_glm = '''
Call:
glm(formula = event ~ factor(period) - 1 + poor_health + sb + 
    race_ethnicity + ses + risk_kick + county_urbanrural, family = binomial(link = "logit"), 
    data = cig_pp)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
-0.7409  -0.2250  -0.1672  -0.1220   3.6596  

Coefficients:
                  Estimate Std. Error z value Pr(>|z|)    
factor(period)12  -5.88852    0.36038 -16.340  < 2e-16 ***
factor(period)13  -5.95223    0.36445 -16.332  < 2e-16 ***
factor(period)14  -5.39235    0.33860 -15.925  < 2e-16 ***
factor(period)15  -4.93494    0.32476 -15.196  < 2e-16 ***
factor(period)16  -4.99274    0.32682 -15.277  < 2e-16 ***
factor(period)17  -4.98868    0.32756 -15.230  < 2e-16 ***
factor(period)18  -4.50855    0.31596 -14.269  < 2e-16 ***
factor(period)19  -5.57171    0.35426 -15.728  < 2e-16 ***
factor(period)20  -5.47150    0.35037 -15.616  < 2e-16 ***
factor(period)21  -6.23010    0.40549 -15.364  < 2e-16 ***
factor(period)22  -7.18342    0.53627 -13.395  < 2e-16 ***
poor_health        0.33741    0.05726   5.892 3.81e-09 ***
sb                 0.01280    0.10313   0.124 0.901213    
race_ethnicity    -0.05628    0.04281  -1.314 0.188684    
ses               -0.26116    0.06074  -4.299 1.71e-05 ***
risk_kick          0.48191    0.05513   8.742  < 2e-16 ***
county_urbanrural  0.24796    0.06782   3.656 0.000256 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

(Dispersion parameter for binomial family taken to be 1)

    Null deviance: 27434.8  on 19790  degrees of freedom
Residual deviance:  3618.3  on 19773  degrees of freedom
AIC: 3652.3

Number of Fisher Scoring iterations: 8'''


test_cox = '''Call:
coxph(formula = cleared_surv ~ vic_age + I(vic_age^2) + vic_female + 
    vic_white, data = conttime, ties = "efron")

  n= 384, number of events= 153 

                   coef  exp(coef)   se(coef)      z Pr(>|z|)   
vic_age      -0.0465757  0.9544923  0.0158531 -2.938  0.00330 
I(vic_age^2)  0.0005639  1.0005641  0.0001910  2.953  0.00315 
vic_female    0.3380500  1.4022106  0.1824076  1.853  0.06384 . 
vic_white     0.4913339  1.6344951  0.1776549  2.766  0.00568 
---
Signif. codes:  0 ‘***’ 0.001 ‘’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

             exp(coef) exp(-coef) lower .95 upper .95
vic_age         0.9545     1.0477    0.9253    0.9846
I(vic_age^2)    1.0006     0.9994    1.0002    1.0009
vic_female      1.4022     0.7132    0.9807    2.0048
vic_white       1.6345     0.6118    1.1539    2.3153

Concordance= 0.599  (se = 0.025 )
Likelihood ratio test= 23.99  on 4 df,   p=8e-05
Wald test            = 26.11  on 4 df,   p=3e-05
Score (logrank) test = 27.05  on 4 df,   p=2e-05'''


test_ph = '''                     chisq df       p
vic_age              1.938  1  0.1639
I(vic_age^2)         2.054  1  0.1518
vic_female           2.405  1  0.1210
vic_white           20.728  1 5.3e-06
firearm              3.392  1  0.0655
loc_outdoor          0.471  1  0.4926
loc_other            0.016  1  0.8995
nonargument          1.052  1  0.3050
unknown_circum       0.179  1  0.6720
off_under_influence  2.240  1  0.1345
business_hours       0.505  1  0.4774
GLOBAL              30.757 11  0.0012'''


def generate_df_stargazer(input_string):
    lines = input_string.split('\n')
    i = 0
    num_variables = 0
    data = []
    while i < len(lines):
        if lines[i] == '':
            i += 1
            continue
        if lines[i][0] == '=':  # skip first and last line
            i += 1
            continue
        if lines[i].strip() == 'Dependent variable:':  # found dependant variable
            i += 2
            variable = lines[i].strip()
            i += 1
            var_vals = re.findall(r'\(.\)', lines[i])
            num_variables = len(var_vals)
            labels = ['Label']
            labels.extend([variable + ' ' + x for x in var_vals])
            data.append(labels)
        if lines[i][0] == '-':  # now entering data
            i += 1
            while lines[i][0] != '=':
                if lines[i][0] == '-':
                    i += 1
                    continue
                split = lines[i].split()
                breaking_point = 0
                for idx, d in enumerate(split):
                    if re.search('^\s*-*\.*\(*\d+', d) is not None:
                        breaking_point = idx
                        break
                label = ''.join(split[:breaking_point])
                line_info = [label]
                # we know we have x variables, look at each data point and see which it corresponds to
                line_data = split[breaking_point:]
                for idx, d in enumerate(line_data):
                    r = d.replace('*', '\\*').replace('.', '\\.')
                    # if re.match(r'\d+', r) is None:
                    #     continue
                    start = re.search(r, lines[i]).start()
                    if start < 25:
                        line_info.append(d)
                    elif start < 35:
                        while len(line_info) < 2:
                            line_info.append('')
                        line_info.append(d)
                    elif start > 35:
                        while len(line_info) < 3:
                            line_info.append('')
                        line_info.append(d)
                    else:
                        line_info.append('')
                while len(line_info) < num_variables+1:
                    line_info.append('')
                data.append(line_info)
                i += 1
        i += 1
    data_lines = [';'.join(x) for x in data]
    df = pd.read_csv(StringIO('\n'.join(data_lines)), delimiter=';')
    return df


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


def generate_glm(input_string):
    data_lines = input_string.split('\n')
    data = []
    i = 0
    while i < len(data_lines):
        if data_lines[i].strip() == 'Coefficients:':  # in main data
            i += 1
            labels = ["Label", 'Estimate', 'Std.Error', 'z-value', 'Pr(>|z|)']
            data.append(labels)
            i += 1
            break
        i += 1
    while i < len(data_lines):
        if data_lines[i][0] == '-':
            break
        line = data_lines[i].split()
        end = ''.join(line[4:])
        data.append([line[0], line[1], line[2], line[3], end])
        i += 1
    data_lines = [';'.join(x) for x in data]
    df = pd.read_csv(StringIO('\n'.join(data_lines)), delimiter=';')
    return df


def main():
    sg.theme('DarkAmber')
    layout = [[sg.Text('Enter data string:'), sg.InputText()],
              [sg.Button('Generate'), sg.Button('Generate Stargazer'), sg.Button('Generate GLM')]]
    window = sg.Window('Table Maker', layout)
    df = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Generate':
            df = generate_df(values[0])
        if event == 'Generate Stargazer':
            df = generate_df_stargazer(values[0])
        if event == 'Generate GLM':
            df = generate_glm(values[0])
        if df is not None:
            print(df)
            filename = sg.tk.filedialog.asksaveasfilename(
                defaultextension='csv',
                initialdir=script_path,
                initialfile='unnamed.csv',
                parent=window.TKroot,
                title='Save As'
            )
            extension = filename.split('.')[-1]
            if extension == 'csv':
                df.to_csv(filename, index=False)
            elif extension == 'xlsx':
                df.to_excel(filename, index=False)
    window.close()


if __name__ == '__main__':
    main()