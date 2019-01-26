import pandas
import pprint
import datetime
from flask import Flask
from flask import render_template
from sqlalchemy import create_engine

# _ENGINE = "mysql+mysqldb://python_user:PythonConn149147@localhost/workout_db"
# _LIFT_SQL = '''
#     SELECT ID, Lift_Name
#     FROM Lift
# '''
#
# engine = create_engine(_ENGINE)
# lift_df = pandas.read_sql(_LIFT_SQL, engine,)
#                           # index_col="ID")
#
# print(lift_df.values.tolist())
#
# lift_list = lift_df.values.tolist()
# for i, l in lift_list:
#     print(str(i)+' '+l)
# # for i, l in lift_df.items():
# #     print(i+' '+l)
#
# # for l in lift_df.items():
# #     print(l)

date = datetime.date.today()
print(date)

