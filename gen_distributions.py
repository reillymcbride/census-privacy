import io
import pandas as pd
import numpy as np
import re
import csv

# maybe: generate a dict of blocks? or create a csv that has


# for every block in cook county illinois:
# - total pop
# - number of people in each age bucket for each sex
#   - will have to randomly generate w/i age bucket
# - number of people for each race option


# when the csv is read back in main script...
# for every block:
#   create a sample set, then a guessed set as follows:
#   do the following n times, where n is # of people in block:
#       - randomly pick gender-age pairing (with each pairing having a certain probability?)
#       - randomly pick race info (with each race option having a certain probability)
#   count matches between sampled and guessed sets
#
# determine avg # of matches?
# see if there are relationships between tightness of distribution and number of matches
#   variance and no. of matches? may not rlly make sense tho..  want a measure of like... number of diff
#   categories w/ significant prob.
#   maybe # of categories above 0.1 prob or something like that??
#   can also do as a function of block size
#
# also comp. to ruggles ofc




# Calculate age & sex distributions

def calc_distributions(dict, n):
    result = {}
    result["N"] = n
    for i in range(n):
        count = 0 # we want to skip first two cols, geo id and total pop
        for key in dict:
            if count < 2:
                count += 1
                continue
            else:
                result[key] = float(dict[key]) / n   # float div in python 3
                count += 1

    return result



def generate_distributions():
    # open both files
    # blocks should line up so
    # get next row from age_sex
    # get next row from race
    # call calc_age_and_sex on age_sex row
    # call calc_race on race row
    # write out a new line to csv that's like: race info, age sex info (no real need to keep block number)
    #   - store info as probabilities out of 1

    with open('age_sex_data_2010_cook_county/2010_P12_short_headers.csv', 'r') as age_sex_csv, \
            open('race_data_2010_cook_county/2010_P1_short_headers.csv', 'r') as race_csv, \
            open('output.csv', 'w') as output:
        age_sex_reader = list(csv.DictReader(age_sex_csv, delimiter=','))
        race_reader = list(csv.DictReader(race_csv, delimiter=','))
        csv_writer = None

        for age_sex_row, race_row in zip(age_sex_reader, race_reader):
            try:
                n_age_sex = int(age_sex_row["P012001"])  # total pop count for block
                n_race = int(race_row["P001001"])  # total pop count for block
            except ValueError:
                n_age_sex = int(age_sex_row["P012001"].split("(")[0])
                n_race = int(race_row["P001001"].split("(")[0])

            if n_race == 0 or n_age_sex == 0:
                continue

            age_sex_probs = calc_distributions(age_sex_row, n_age_sex)
            race_probs = calc_distributions(race_row, n_race)

            to_discard = ["P001002", "P001009", "P001026", "P001047", "P001063", "P001070", "P012002", "P012026"]
            # ^^ total of one race, 2+ race, 3 races, 4 races, 5 races, 6 races, total male, total female

            if csv_writer is None:
                headers = ["N"]
                headers.extend(list(age_sex_row.keys())[2:])
                headers.extend(list(race_row.keys())[2:])
                for item in to_discard:
                    headers.remove(item)
                csv_writer = csv.DictWriter(output, fieldnames=headers)
                csv_writer.writeheader()

            combo = {}
            combo.update(age_sex_probs)
            combo.update(race_probs)

            for item in to_discard:
                del combo[item]

            csv_writer.writerow(combo)


generate_distributions()