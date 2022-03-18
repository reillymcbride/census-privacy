import numpy as np
import csv
from random import choices, randint
import matplotlib.pyplot as plt

def fill_age_opts():
    age_sex_options = {}
    with open("age_sex_data_2010_cook_county/age_sex_buckets.csv", "r") as age_sex_buckets:
        reader = csv.DictReader(age_sex_buckets, delimiter=',')
        for row in reader:
            stat = row['ID']
            age_sex_options[stat] = (row['Sex'], int(row['MinAge']))
    return age_sex_options


# take in distribution dictionary & num records that need to be generated.
# file is age headings first then race headings
def gen_block(dist_dict, age_sex_encodings, calc_stats):
    all_headers = list(dist_dict.keys())
    all_weights = list(dist_dict.values())
    num_age_opts = len(age_sex_encodings.keys())

    n = int(all_weights[0])
    age_sex_pop = all_headers[1:(num_age_opts + 1)]
    age_sex_weights = list(map(float, all_weights[1:(num_age_opts + 1)]))
    race_pop = all_headers[(num_age_opts + 1):]
    race_weights = list(map(float, all_weights[(num_age_opts + 1):]))

    result = []
    stats = None

    if calc_stats:
        stats = {}
        count = 0
        for w in all_weights:
            if float(w) > 0.05:
                count += 1
        stats["block_size"] = n
        stats['num_stats_with_prob_above_0.05'] = count

    for i in range(n):
        record = {}
        age_sex_header = choices(age_sex_pop, age_sex_weights)[0]
        age_sex_details = age_sex_encodings[age_sex_header]
        record['sex'] = age_sex_details[0]
        min_age = age_sex_details[1]
        record['age'] = randint(min_age, min_age + 5)
        record['race'] = choices(race_pop, race_weights)[0]
        result.append(record)

    return result, stats


def count_matches(guessed_block, sample_block):
    possible_combos = {}
    for record in sample_block:
        combo_key = str(record['sex'][0]) + str(record['age']) + str(record['race'])
        if combo_key in possible_combos:
            possible_combos[combo_key][0] += 1
        else:
            possible_combos[combo_key] = [1, 0]

    for record in guessed_block:
        combo_key = str(record['sex'][0]) + str(record['age']) + str(record['race'])
        if combo_key in possible_combos:
            possible_combos[combo_key][1] += 1
        else:
            possible_combos[combo_key] = [0, 1]

    count = 0
    for v in possible_combos.values():
        count += min(v)

    return count


def main():
    age_sex_options = fill_age_opts()

    count = 0

    block_sizes = []
    matches = []
    prop_matches = []
    percent_above_thresh = []
    with open("output.csv", "r") as distributions:
        reader = csv.DictReader(distributions, delimiter=',')
        # for every block distribution summary:
        for row in reader:
            count += 1
            if count % 1000 == 0:
                # print(count) #lets you somewhat keep track of progress as it runs

            #generate sample pop records
            size = int(row["N"])
            if size > 4000 or size <= 1: #there was one random huge block og size 10,000
                continue
            sample_block, stats = gen_block(row, age_sex_options, True)
            #generate guessed pop records
            guessed_block = gen_block(row, age_sex_options, False)[0]
            #count matches in sample & guessed
            num_matches = count_matches(sample_block, guessed_block)
            stats["num_matches"] = num_matches

            #track stats for graphing
            matches_rel_to_size = num_matches/size
            #print("block size: " + str(size) + " , num matches: " + str(num_matches) + " , rel matches: " + str(matches_rel_to_size))
            block_sizes.append(size)
            matches.append(num_matches)
            prop_matches.append(matches_rel_to_size)
            num_above_thresh = stats["num_stats_with_prob_above_0.05"]
            num_stats = len(row.keys()) - 1
            percent_above_thresh.append(num_above_thresh/num_stats)

    sizes_np = np.array(block_sizes)
    prop_matches_np = np.array(prop_matches)
    probs_np = np.array(percent_above_thresh)

    plt.plot(sizes_np, prop_matches_np, 'o')
    res = np.polyfit(sizes_np, prop_matches_np, 1)
    m = res[0]
    b = res[1]
    plt.plot(sizes_np, m * sizes_np + b)
    plt.xlabel('block sizes')
    plt.ylabel('matches as a % of block size')
    plt.ylim([0, 1])
    plt.show()

    plt.plot(probs_np, prop_matches_np, 'o')
    res = np.polyfit(probs_np, prop_matches_np, 1)
    plt.xlabel('% of stats with prob > 0.05')
    plt.ylabel('matches as a % of block size')
    m = res[0]
    b = res[1]
    plt.plot(probs_np, m * probs_np + b)
    plt.ylim([0, 1])
    plt.show()


    #summary statistics on proportional matches
    mean = np.mean(prop_matches_np)
    median = np.median(prop_matches_np)
    stddev = np.std(prop_matches_np)
    print()
    print("MEAN: " + str(mean) + "  MEDIAN: " + str(median) + "  STDDEV: " + str(stddev))



main()