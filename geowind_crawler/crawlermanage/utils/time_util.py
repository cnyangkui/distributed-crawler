# -*- encoding: utf-8 -*-
import time

import datetime

'''
    比较时间是否在一个区间上
    l_time:待比较时间
    start_t:开始时间
    end_t:结束时间
'''


def compare_time(l_time, start_t, end_t):
    s_time = time.mktime(time.strptime(start_t, '%Y/%m/%d'))  # get the seconds for specify date
    e_time = time.mktime(time.strptime(end_t, '%Y/%m/%d'))
    log_time = time.mktime(time.strptime(l_time, '%Y/%m/%d'))
    if (float(log_time) >= float(s_time)) and (float(log_time) <= float(e_time)):
        return True
    return False


def get_now_weekday():
    d = datetime.datetime.now()
    return d.weekday()


def get_weekday(mydate):
    date = datetime.datetime.strptime(mydate, "%Y/%m/%d").date()
    day = date.weekday()
    return day

'''mydate:YYYY/MM/DD'''


def after_n_days(mydate, n):
    arr = mydate.split('/')
    date = datetime.datetime(int(arr[0]), int(arr[1]), int(arr[2])) + datetime.timedelta(days=n)  # 2015-10-29 00:00:00
    time_format = date.strftime('%Y/%m/%d')  # '20151029'
    return time_format


'''mydate:YYYY/MM/DD'''


def before_n_days(mydate, n):
    arr = mydate.split('/')
    date = datetime.datetime(int(arr[0]), int(arr[1]), int(arr[2])) - datetime.timedelta(days=n)  # 2015-10-29 00:00:00
    time_format = date.strftime('%Y/%m/%d')  # '20151029'
    return time_format


'''mydate:YYYY/MM/DD'''


def in_latest_weekend(mydate):
    now = time.strftime("%Y/%m/%d")
    weekday = get_now_weekday()
    monday = before_n_days(now, weekday)
    sunday = after_n_days(now, (7 - 1 - weekday))
    print(monday+" "+sunday)
    return compare_time(mydate, monday, sunday)


if __name__ == '__main__':
    print(time.strftime("%Y/%m/%d"))
    print(get_now_weekday())
    print(compare_time('2017/06/29', '2017/06/29', '2017/06/28'))
    print(after_n_days('2017/06/29', 6))
    now = time.strftime("%Y/%m/%d")
    flag = in_latest_weekend('2017/07/03')
    print(flag)
    print(get_weekday('2017/06/29'))
