import dbconn


def generate(date, shift, batch):
    print('date:'+date)
    print('shift:' + shift)
    print('batch:' + batch)
    dbconn.get_tt(date, shift, batch)
    pass
