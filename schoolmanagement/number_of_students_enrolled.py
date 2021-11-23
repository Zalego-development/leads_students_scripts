import mysql.connector
import datetime
import pandas as pd
import json

schoolmanagement_db = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    db="",
    charset="utf8",
)


school_cursor = schoolmanagement_db.cursor()
# schoolquery = (
#     "SELECT id, students_account_id, firstname, lastname, email, phonenumber, cohort_id, amount_to_pay,  finalprice, discount, created_at \
#     FROM student_enrollments \
#     INNER JOIN \
#     (SELECT id AS student_acc_id, firstname, lastname, email,phonenumber \
#     FROM student_accounts GROUP BY student_acc_id) student \
#     ON student.student_acc_id = students_account_id"
#     )
schoolquery = (
    "SELECT id, students_account_id, firstname, lastname, email, phonenumber, cohort_id, amount_to_pay,  finalprice, discount,start_date, created_at\
    FROM student_enrollments\
    INNER JOIN\
    (SELECT id AS student_acc_id, firstname, lastname, email,phonenumber\
    FROM student_accounts GROUP BY student_acc_id) student\
    ON student.student_acc_id = students_account_id\
    INNER JOIN\
    (SELECT id AS cohortid, start_date FROM cohorts) cohort \
    ON cohortid = student_enrollments.cohort_id"
    )
school_cursor.execute(schoolquery)
result = school_cursor.fetchall()

mylist = []

our_keys = (
    'id', 'student_account_id', 'firstname', 'lastname', 'email', \
        'phonenumber', 'cohort_id',\
            'amount_to_pay', 'finalprice', 'discount', 'start_date', 'created_at')
for ree in result:
    if len(our_keys) == len(ree):
        res = dict(zip(our_keys, ree))
        if res['start_date'] is not None:
            new_date_complete = res['start_date'].strftime('%B')
            if new_date_complete == 'October':
                mylist.append(res)

print(f"October enrollment has {len(mylist)} enrollments")
print(f"October total registration fees = {len(mylist) * 1500}")