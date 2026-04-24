import csv
from datetime import timedelta, datetime

def lms_time_to_td(duration):
    hrs, mins, secs = duration.split(':') 
    return timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))

'''
___key terms___
stat_key = the group
goal_total = number of summed seconds of goal times for the group
actual_total = number of summed actuals for the group
perf = goal_total / actual_total
weight = percentage or ratio of assignments for this group vs the whole.

The perf and weight can be used to calculate the same total performance as adding up all the groups total goals/actuals together.
By using weighted average we can see how each group contributes to that total - Averaging either way gives you the same number.

'''

# initializing starting data and vars
records = []
with open('everyone30.csv', newline='') as csvFile: # move a csv file into records array
    reader = csv.reader(csvFile, delimiter=',')
    for row in reader:
        this_record = row
        records.append(this_record)

all_goal = 0 # named this all_goals and all_goal because we are talking about all groups where as goal_total describes only the total within a group.
all_actual = 0
all_cnt = 0

stats_dictionary = {} # {stat_key: {'goal_total':number, 'actual_total':number, 'perf':number, 'weight':number}} # how we implement the key terms

for record in records: # now that the record is in the records array we can select which field we want using record[nth_field] and just count the number of columns to the field u want in the excel sheet
    r_goal = lms_time_to_td(record[8])
    r_actual = lms_time_to_td(record[9])
    id_num = int(record[0][3:])
    r_start = record[5]
    size = float(record[31].split(' ')[0])
    pounds = float(record[32].split(' ')[0])
    size_lb_factor = None
    density = None
    if size != 0 and pounds != 0:
        density = pounds/size
        size_lb_factor = size * pounds
    
    #                                       filtering examples

    #if '3/23' not in r_start: continue  # example 1 of only pulling from what is actually 23rd not 24th
    #if ' 14:' not in r_start: continue # example 2 pulling from 14th hours
    #if r_goal.seconds != 5: continue # example 3 only assignments having 5 second goal times
    #if size == 0 or pounds == 0: continue

    #                                       stat key example - the stat_key defines the groups
    #stat_key = r_actual.seconds
    #stat_key = r_goal.seconds
    #stat_key = int(size_lb_factor) # these types of groups will need a filter like 'if size == 0 or pounds == 0: continue' so that we do not divide by 0
    #stat_key = round(pounds, 0)
    #stat_key = round(size, 1)
    #stat_key = round(density,-1) 

    # setting the group with stat_key
    stat_key = r_goal.seconds # plug another example in here
    stat_key_name = 'goal_seconds: ' # this string will print with the stat_key

    if stat_key not in stats_dictionary:
        stats_dictionary[stat_key] = {'goal_total': r_goal.seconds, 'actual_total': r_actual.seconds}
    else:
        stats_dictionary[stat_key]['goal_total'] += r_goal.seconds
        stats_dictionary[stat_key]['actual_total'] += r_actual.seconds
    all_goal += r_goal.seconds
    all_actual += r_actual.seconds
    all_cnt += 1

# calc the weights and performances - I think this loop has to be separate from the one that populates goals and actuals.
for stat_key, stats in stats_dictionary.items():
    goal_total = stats['goal_total']
    actual_total = stats['actual_total']
    if actual_total == 0: perf = 'na' # this covers perf 999% situations by ignoring them. why doesn't cause a division by string error?
    else: perf = goal_total/actual_total # calc perf
    weight = actual_total/all_actual # calc weight
    stats['perf'] = perf
    stats['weight'] = weight


# sort dictionary before displaying
sorted_seconds = dict(sorted(stats_dictionary.items()))
for key, item in sorted_seconds.items():
    print(stat_key_name + str(key), item)
print(all_goal, all_actual) # print out the "all" vars to verify and review our math
print(all_goal/all_actual) # all groups performance

