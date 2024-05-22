# input csv or xlsx file, adds column with gender guess
# F, M, both, X

import time, sys, os
import pandas as pd
from tqdm import tqdm
from utils.strings import replaceMultiple

boynamez = 'names/A_males.csv'
girlnamez = 'names/non-A_females.csv'
output_folder_name = 'gender-guessed'
input_file = sys.argv[1]
name_col = sys.argv[2]

start_time = time.time()

folder = os.path.dirname(input_file)

# create output folder if it doesn't exist
if not os.path.exists(folder + '/' + output_folder_name):
    os.makedirs(folder + '/' + output_folder_name)

# Determine the output file name
output_file = folder + '/' + output_folder_name + '/' + os.path.splitext(os.path.basename(input_file))[0] + '+gen.xlsx'

# Read the input file based on its extension
if input_file.endswith('.csv'):
    input_data = pd.read_csv(input_file)
elif input_file.endswith('.xlsx'):
    input_data = pd.read_excel(input_file)
else:
    raise ValueError("Unsupported file format. Please use a CSV or XLSX file.")

# Read the boys and girls names files
boys = pd.read_csv(boynamez)
girls = pd.read_csv(girlnamez)

# Process each row in the input data
pbar = tqdm(total=len(input_data))
for index, row in input_data.iterrows():
    firstnames = row[name_col]
    firstnames = replaceMultiple(firstnames, ['-', '–'], ' ')
    firstnamez = firstnames.split()
    
    genders = set()
    for name in firstnamez:
        name = name.lower()

        iz_boy = (boys['prenume'].str.lower() == name).any()
        iz_girl = (girls['prenume'].str.lower() == name).any()

        if not (iz_boy or iz_girl):
            last_char = name[-1]
            iz_boy = last_char != 'a'
            iz_girl = last_char == 'a'

        if iz_boy and iz_girl:
            genders.add('both')
        elif iz_girl:
            genders.add('F')
        elif iz_boy:
            genders.add('M')
        else:
            genders.add('X')

    if 'both' in genders or len(genders) > 1:
        gender = 'X'
    else:
        gender = genders.pop() if genders else 'X'

    input_data.loc[index, 'gen'] = gender

    pbar.update(1)

# Save the output data to an Excel file
input_data.to_excel(output_file, index=False)

elapsed = round(time.time() - start_time)
tqdm.write("output -> " + output_file)
tqdm.write("elapsed time: " + str(elapsed) + " seconds")
