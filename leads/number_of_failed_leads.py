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

zalego_cursor = zalegohrms_db.cursor()
# zalegoquery = (
#     "SELECT leadid, customer, handler, status, completeness, dateComplete \
#     FROM leads WHERE completeness=2 OR completeness=0"
#     )
zalegoquery = (
    "SELECT leadid, customer, name, intake, form, school, source_category, status, completeness, dateComplete \
    FROM leads \
    inner join \
    (select id as appid, name, intake, form, school, source_category from applications group by appid, name, \
        intake, form, school, source_category) app\
    on appid = leads.customer WHERE leads.completeness=0"
)
zalego_cursor.execute(zalegoquery)
result = zalego_cursor.fetchall()
# our_keys = ('leadid', 'customer', 'handler', 'status', 'completeness', 'dateComplete')
our_keys = ('leadid', 'customer', 'name', 'intake', 'form', 'school', 'source_category', 'status', 'completeness', 'dateComplete')

for ree in result:
    if len(our_keys) == len(ree):
        res = dict(zip(our_keys, ree))
        if res['dateComplete'] is not None:
            new_time = datetime.datetime.strptime(res['dateComplete'], '%Y-%m-%d %H:%M:%S %p')
            new_date_complete = new_time.strftime('%B')
            if new_date_complete == 'October':
                mylist.update({res['leadid']: new_date_complete})
        # if res['intake'] is not None:
            # new_time = datetime.datetime.strptime(res['dateComplete'], '%Y-%m-%d %H:%M:%S %p')
            # new_date_complete = new_time.strftime('%B')
            # new_intake = res['intake'].title()
            # if new_intake == 'October':
            #     mylist.update({res['leadid']: new_intake})

mycourses = Counter(mylist.values())

for k,v in mycourses.items():
    print(k ,f"- {v} Failed Leads")