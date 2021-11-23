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
    charset="",
)

mylist = {}

zalego_cursor = zalegohrms_db.cursor()
# zalegoquery = (
#     "SELECT leadid, customer, handler, status, completeness, dateComplete \
#     FROM leads WHERE completeness=15"
#     )
zalegoquery = (
    "SELECT leadid, customer, name, intake, form, school, source_category, status, completeness, dateComplete \
    FROM leads \
    inner join \
    (select id as appid, name, intake, form, school, source_category from applications group by appid, name, intake, \
        form, school, source_category) app \
    on appid = leads.customer WHERE leads.completeness=15"
    )
zalego_cursor.execute(zalegoquery)
result = zalego_cursor.fetchall()
# our_keys = ('leadid', 'customer', 'handler', 'status', 'completeness', 'dateComplete')
our_keys = ('leadid', 'customer', 'name', 'intake', 'form', 'school', 'source_category', 'status', 'completeness', 'dateComplete')
for ree in result:
    if len(our_keys) == len(ree):
        res = dict(zip(our_keys, ree))
        new_time = datetime.datetime.strptime(res['dateComplete'], '%Y-%m-%d %H:%M:%S %p')
        new_date_complete = new_time.strftime('%B')
        if new_date_complete == 'October':
            mylist.update({res['leadid']: new_date_complete})

mycourses = Counter(mylist.values())

for k,v in mycourses.items():
    print(k ,f"- {v} Completed Leads")