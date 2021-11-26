
from datetime import datetime
import psycopg2 as pgad

first_str = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
second_str ='2021-11-25-18:06:03'
datetime_object_first = datetime.strptime(first_str, '%Y-%m-%d-%H:%M:%S')
datetime_object_second = datetime.strptime(second_str, '%Y-%m-%d-%H:%M:%S')
datetime_object_first_dt = (datetime_object_first.time())
datetime_object_second_dt = (datetime_object_second.time())
print('-------')
print(type(datetime_object_second_dt))
print(type(datetime_object_first_dt))
c = datetime_object_first - datetime_object_second

print('Difference: ', c)
  
# returns (minutes, seconds)
minutes = divmod(c.total_seconds(), 60) 
print('Total difference in minutes: ', minutes[0], 'minutes',
                                 minutes[1], 'seconds')
                                 
if (minutes[0]>0 or minutes[1]>30):
    print("High")
#diff_time = datetime_object_first -  datetime_object_second
"""
if (int(diff_time.today().strftime('%S'))>4):
    print("High")

#print(int(datetime_object_first.time() - datetime_object_second.time()))
import time
now = time.time()
later = time.time()
difference = int(later - now)
print(difference)
"""

def checkwhethercorrupt(filename):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        single_quote="\'"
        sql="select upload_dt from \"public\".\"uploadhistory\" where filename="+single_quote+filename+single_quote+" order by upload_dt desc fetch first row only"
        cur.execute(sql)
        second_str = cur.fetchone()[0]
        first_str = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        datetime_object_first = datetime.strptime(first_str, '%Y-%m-%d-%H:%M:%S')
        datetime_object_second = datetime.strptime(second_str, '%Y-%m-%d-%H:%M:%S')
        c = datetime_object_first - datetime_object_second
        minutes = divmod(c.total_seconds(), 60) 
        if (minutes[0]>0 or minutes[1]>30):
            return True 
        return False
    except(Exception) as error:
        
        print("Exception while  checking file corruption"+str(error))
        return False

print(checkwhethercorrupt('C:\\Users\\jeffe\\Projects\\test-dir\\zrdk.waw'))

