import dbconn
from flask import jsonify
import datetime


def change(shift,date,subject,teacher,room,start_time,batch):
    #more variables to be added
    week = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY',
            'THURSDAY', 'FRIDAY', 'SATURDAY']
    weekday_num = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
    day = week[(weekday_num + 1) % 7]
    #print(day)
    if date is None or teacher is None or subject is None:
        res = jsonify(status=0, message='Missing fields!'), 400
        return res
    else:
        id_ptr = dbconn.get_id_ptr(shift, day, start_time, batch)
        if id_ptr == -1:
            res = jsonify(status=0, message='Invalid ID_POIINTER(Incorrect fields)'), 400
            return res
        #print(id_ptr)
        previous_change = dbconn.find_previous_change(id_ptr, date)
        if previous_change == -1:
            res = jsonify(status=0, message='FIND Previous change failed'), 400
            return res
        if previous_change:
            print(previous_change[0][0])
            status = dbconn.delete_previous_change(previous_change[0][0])
            if status == -1:
                res = jsonify(status=0, message='Delete Failed'), 400
                return res
        status = dbconn.insert_new_change(id_ptr, date, subject, teacher, room)
        if status == -1:
            res = jsonify(status=0, message='Insert Failed'), 400
            return res
    return jsonify(status=1, message="successful")



