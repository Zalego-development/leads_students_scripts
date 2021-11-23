import mysql.connector
import datetime
import pandas as pd
import json

zalegohrms_db = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    db="",
    charset="utf8",
)
zalego_cursor = zalegohrms_db.cursor()
zalegoquery = (
    "SELECT leadid, customer, handler, status, completeness, level, dateComplete, amount_to_pay,  finalprice, discount, created_at \
    FROM student_enrollments \
    INNER JOIN \
    (SELECT id AS student_acc_id, firstname, lastname, email,phonenumber \
    FROM student_accounts GROUP BY student_acc_id) student \
    ON student.student_acc_id = students_account_id"
    )
zalego_cursor.execute(zalegoquery)
result = zalego_cursor.fetchall()