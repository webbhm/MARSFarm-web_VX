'''
create dummy data for charting
'''
from random import randint
from pandas import DataFrame

def get_values(min, max, numbers):
    print("Min", min, "Max", max, "Iter", numbers)
    result = map(lambda x: randint(min, max), numbers)
    return list(result)

def build_frame(times, values, attribute):
    gp = []
    ts = []
    value = []
    for x in range(len(times)):
        #print(start_time, doc[TIME][TIMESTAMP], end_time)
        print(x)
        gp.append('123_x')
        ts.append(times[x])
        value.append(values[x])    
    return DataFrame({'mf_id':gp,'day':ts, attribute:value})

def get_data(time, attribute):
    values = get_values(10, 30, time)
    return build_frame(time, values, attribute)

def get_test_data(attribute):
    tm = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    values = get_values(10, 30, tm)
    return build_frame(tm, values, attribute)

    
if __name__ == '__main__':
    tm = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    f = get_test_data('temp')
    print(f)
    