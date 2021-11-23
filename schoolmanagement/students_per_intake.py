import mysql.connector
import datetime
import pandas as pd
import json
from collections import Counter

schoolmanagement_db = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    db="",
    charset="utf8",
)

school_cursor = schoolmanagement_db.cursor()
schoolquery = (
    "SELECT id, students_account_id, cohort_id, cohort_name, start_date, amount_to_pay, created_at \
    FROM student_enrollments \
    INNER JOIN \
    (SELECT id as cohortid, cohort_name, start_date \
    FROM cohorts GROUP BY cohortid, cohort_name, start_date) intake \
    on intake.cohortid = cohort_id"
    )
school_cursor.execute(schoolquery)
result = school_cursor.fetchall()

mylist = {}
second_list = {}
our_keys = ('id', 'student_account_id', 'cohort_id', 'cohort_name', 'start_date', 'amount_to_pay', 'created_at')

for ree in result:
    if len(our_keys) == len(ree):
        res = dict(zip(our_keys, ree))
        mylist.update({res['student_account_id']: res['start_date'].strftime('%B')})

mycourses = Counter(mylist.values())

for k,v in mycourses.items():
    if k == 'October':
        second_list.update({k: v})

print(pd.DataFrame(second_list.items(), columns=['Intake', 'Count']))
