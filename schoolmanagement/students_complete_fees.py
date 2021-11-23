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

schoolquery = (
    "SELECT id, students_account_id, firstname, lastname, email, phonenumber, cohort_id, amount_to_pay,  finalprice, discount, created_at \
    FROM student_enrollments \
    INNER JOIN \
    (SELECT id AS student_acc_id, firstname, lastname, email,phonenumber \
    FROM student_accounts GROUP BY student_acc_id) student \
    ON student.student_acc_id = students_account_id"
    )
school_cursor.execute(schoolquery)
result = school_cursor.fetchall()

our_keys = (
    'id', 'student_account_id', 'firstname', 'lastname', 'email', \
        'phonenumber', 'student_email', 'student_phonenumber', 'cohort_id', \
            'amount_to_pay', 'finalprice', 'discount', 'created_at')

# for res in result:
#     if len(our_keys) == len(res):
#         res = dict(zip(our_keys, res))
#         new_data = {
#             'student_enrollment_id': res['student_enrollment_id'],
#             'student_firstname': res['student_firstname'],
#             'student_lastname': res['student_lastname'],
#             'student_enrollment_account_id': res['student_enrollment_account_id'],
#             'student_account_id': res['student_account_id'],
#             'student_email': res['student_email'],
            # 'student_phonenumber': res['student_phonenumber'],
            # 'student_enrollment_cohort_id': res['student_enrollment_cohort_id'],
            # 'student_enrollment_amount_to_pay': res['student_enrollment_amount_to_pay'],
            # 'student_enrollment_finalprice': res['student_enrollment_finalprice'],
            # 'student_enrollment_discount': res['student_enrollment_discount'],
            # 'student_enrollment_created_at': res['student_enrollment_created_at'].strftime("%Y-%m-%d %H:%M:%S"),
            # 'course_id': res['course_id'],
            # 'course_name': res['course_name']
#         }
#         newjson = json.dumps(new_data) 
#         newfile = open('complete_fees.json', 'a')
#         newfile.write(f"{newjson},\n")
# newfile.close()