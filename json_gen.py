import dbconn


def generate(date, shift, batch):
    print('date:' + date)
    print('shift:' + shift)
    print('batch:' + batch)
    generated_json = dbconn.get_tt(date, shift, batch)
    return generated_json


def get_timetable_today(initial):
    timetable = dbconn.get_tt_today(initial)
    return timetable
