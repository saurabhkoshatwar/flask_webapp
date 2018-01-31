import redis, os, dbconn
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']


def cache_to_redis(date):
    r = redis.StrictRedis(host="redis-18388.c1.ap-southeast-1-1.ec2.cloud.redislabs.com", port="18388",
                          decode_responses=True, password=REDIS_PASSWORD, socket_timeout=30, connection_pool=None)
    shifts = ['I', 'II']
    batches = ['A', 'B', 'C', 'D']
    for shift in shifts:
        for batch in batches:
            time_table, status = dbconn.get_tt('2018-01-29', 'I', 'A')
            if status:
                final_json = {"status": status, "result_set": time_table}
                r.set(str(date)+shift+batch, final_json)
                r.expire(name=str(date)+shift+batch, time=90000)



#cache_to_redis('2018-01-29')
'''time_table, status = dbconn.get_tt('2018-01-29', 'I', 'A')
final_json = {"status":status, "result_set":time_table}
print("\n\n-----------------------------------\n"+str(final_json))'''