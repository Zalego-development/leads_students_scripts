import mysql.connector
import datetime
import pandas as pd
import json
from collections import Counter

zalegohrms_db = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    db="",
    charset="utf8",
)

mylist = {}
second_list = {}

zalego_cursor = zalegohrms_db.cursor()
zalegoquery = (
    "select customer, dr.reasonId, ld.reason, dateComplete from leads\
    inner join \
    (select dealId, customer as dcustomer, reasonId from deal_reasons) dr\
    on dr.dealId=leads.customer\
    inner join\
    (select reasonId, reason from lead_reasons) ld\
    on ld.reasonId=dr.reasonId"
    )
zalego_cursor.execute(zalegoquery)
result = zalego_cursor.fetchall()
our_keys = ('customer', 'reasonId', 'reason', 'dateComplete')

for ree in result:
    if len(our_keys) == len(ree):
        res = dict(zip(our_keys, ree))
        if res['dateComplete'] is not None:
            new_time = datetime.datetime.strptime(res['dateComplete'], '%Y-%m-%d %H:%M:%S %p')
            new_date_complete = new_time.strftime('%B')
            if new_date_complete == 'October':
                mylist.update({res['customer']: res['reason']})

mycourses = Counter(mylist.values())

for k,v in mycourses.items():
    second_list.update({k: v})

print(pd.DataFrame(second_list.items(), columns=['Customer', 'Count']))