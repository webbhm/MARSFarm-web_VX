'''
create dummy data for test charting
'''
from random import randint

# dummy trial days
tm = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


def get_random_values(min, max, numbers):
    #print("Min", min, "Max", max, "Iter", numbers)
    result = map(lambda x: randint(min, max), numbers)
    return list(result)

def get_test_data():
    # create a json structure of pivoted data - what get back from MongoDB
    # build set with two trials
    values = get_random_values(10, 30, tm)
    values2 = get_random_values(10, 30, tm)
    data = []
    for x in range(len(values)):
        rec = {"Trial_Id":123, 'trial_day':x, 'temp':values[x]}
        data.append(rec)
        rec2 = {"Trial_Id":456, 'trial_day':x, 'temp':values2[x]}
        data.append(rec2)
    return data

if __name__ == '__main__':
    f = get_test_data()
    print(f)
    