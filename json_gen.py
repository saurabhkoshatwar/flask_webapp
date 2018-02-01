import dbconn


def generate(date, shift, batch):
    print('date:' + date)
    print('shift:' + shift)
    print('batch:' + batch)
    generated_json = dbconn.get_tt(date, shift, batch)
    return generated_json