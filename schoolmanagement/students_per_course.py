import mysql.connector
import datetime
import pandas as pd
from collections import Counter

schoolmanagement_db = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    db="",
    charset="utf8",
)

school_cursor = schoolmanagement_db.cursor()
# schoolquery = (
#     "SELECT id, students_account_id, course_id, course_name, course_code, amount_to_pay,  finalprice, discount, created_at\
#     FROM student_enrollments\
#     INNER JOIN\
#     (SELECT id AS coursetable_id, course_name, course_code\
#     FROM courses GROUP BY coursetable_id, course_name, course_code ) course\
#     ON course.coursetable_id = course_id"
#     )
schoolquery = (
    "SELECT id, students_account_id, course_id, course_name, course_code, amount_to_pay,  finalprice, discount, start_date, created_at\
    FROM student_enrollments\
    INNER JOIN\
    (SELECT id AS coursetable_id, course_name, course_code\
    FROM courses GROUP BY coursetable_id, course_name, course_code ) course\
    ON course.coursetable_id = course_id\
    INNER JOIN\
    (SELECT id AS cohortid, start_date FROM cohorts) cohort\
    ON cohortid= student_enrollments.cohort_id"
    )
school_cursor.execute(schoolquery)
result = school_cursor.fetchall()

mylist = {}
second_list = {}
our_keys = (
    'id', 'student_account_id', 'course_id', 'course_name', 'course_code', 'amount_to_pay', 'finalprice', 'discount', 'start_date', 'created_at')

for ree in result:
    if len(our_keys) == len(ree):
        res = dict(zip(our_keys, ree))
        if res['start_date'] is not None:
            new_start_date = res['start_date'].strftime("%B")
            if new_start_date == 'October':
                mylist.update({res['student_account_id']: res['course_name']})

mycourses = Counter(mylist.values())
for k,v in mycourses.items():
    second_list.update({k: v})

print(pd.DataFrame(second_list.items(), columns=['Course Name', 'Count']))

