from django.utils import timezone
from . import jalali
def persian_number_converter(num):
    numbers = {
        "0" : "۰",
        "1" : "۱",
        "2" : "۲",
        "3" : "۳",
        "4" : "۴",
        "5" : "۵",
        "6" : "۶",
        "7" : "۷",
        "8" : "۸",
        "9" : "۹"
    }
    for en, fa in numbers.items():
        num = num.replace(en,fa)
    return num
def jalali_time(time):
    month = ['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']
    time = timezone.localtime(time)
    string_of_time = '{},{},{}'.format(time.year,time.month,time.day)
    tuple_of_time = jalali.Gregorian(string_of_time).persian_tuple()
    
    list_of_time = list(tuple_of_time)
    for index,value in enumerate(month):
        if index+1 == list_of_time[1]:
            list_of_time[1]= value
            break
    outer = ' {} {} {} , ساعت {}:{} '.format(
        list_of_time[2],
        list_of_time[1],
        list_of_time[0],
        time.hour,
        time.minute,
    )
    return persian_number_converter(outer)