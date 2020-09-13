# input csv file, adds column with gender guess
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
# name_col = 6

start_time = time.time()

folder = os.path.dirname(input_file)

# create output folder if it doesn;t exist
if not os.path.exists(folder + '/' + output_folder_name):
    os.makedirs(folder + '/' + output_folder_name)

# save to <path>/<$output_folder>/<$input_filename>+gen.csv
output_file = folder + '/' + output_folder_name + '/' + os.path.splitext(os.path.basename(input_file))[0] + '+gen.csv'

input_data = pd.read_csv(input_file)
boys = pd.read_csv(boynamez)
girls = pd.read_csv(girlnamez)

pbar = tqdm(total=len(input_data))
for index, row in input_data.iterrows():
    firstnames = row[name_col]
    # break intro single words, by ' ', '-', '–'
    firstnames = replaceMultiple(firstnames, ['-', '–'], ' ')
    firstnamez = firstnames.split()
    for name in firstnamez:
        name = name.lower()

        iz_boy = (boys['prenume'].str.lower()==name).any().sum()
        iz_girl = (girls['prenume'].str.lower()==name).any().sum()

        #  if not found check last letter if 'A'
        if not (iz_boy or iz_girl):
            last_char = name[len(name) - 1]
            iz_boy = 1 if last_char != 'a' else 0
            iz_girl = 1 if last_char == 'a' else 0
        if iz_boy and iz_girl:
            gender = 'both'
        elif iz_girl:
            gender = 'F'
        elif iz_boy:
            gender = 'M'
        else:
            gender = 'X'

        # FIXME: properly deal w multiple names
        # this just gets the last named checked
        input_data.loc[index, 'gen'] = gender

    pbar.update(1)


input_data.to_csv(output_file)

elapsed = round(time.time() - start_time)
tqdm.write("ouput -> " + output_file + " --- %s secunde ---" % elapsed)