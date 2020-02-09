# -*- encoding: utf-8 -*-
import time

'''
    比较时间是否在一个区间上
    l_time:待比较时间
    start_t:开始时间
    end_t:结束时间
'''
def compare_time(l_time, start_t, end_t):
    s_time = time.mktime(time.strptime(start_t, '%Y/%m/%d %H:%M'))  # get the seconds for specify date

    e_time = time.mktime(time.strptime(end_t, '%Y/%m/%d %H:%M'))

    log_time = time.mktime(time.strptime(l_time, '%Y/%m/%d %H:%M'))

    if (float(log_time) >= float(s_time)) and (float(log_time) <= float(e_time)):
        return True

    return False