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
            mylist.update({res['name']: res['source_category']})

mycourses = Counter(mylist.values())
# print(mylist)
for k,v in mycourses.items():
    if k == '0':
        second_list.update({"Website": v})
    elif k == '1':
        second_list.update({"Walk-ins": v})
    elif k == '2':
        second_list.update({"Highschool": v})
    elif k == '3':
        second_list.update({"Ambassador App": v})
    elif k == '7':
        second_list.update({"University": v})
    elif k == '8' or k == '9':
        second_list.update({"Attachment": v})

print(pd.DataFrame(second_list.items(), columns=['Source', 'Count']))