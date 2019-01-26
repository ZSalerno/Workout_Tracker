import pandas
import pprint
import datetime
from utils.db_utils import create_connection
from sqlalchemy import create_engine

_FILE = 'C:/Users/zack/PycharmProjects/Workout_Tracker/static/Workouts.xlsx'
_ENGINE = "mysql+mysqldb://python_user:PythonConn149147@localhost/workout_db"
_TABLE = 'set'
_SQL = 'Select * From lift'

def simple_import():
    # SQL Alchemy creating connection to MySQL DB
    engine = create_engine(_ENGINE)

    # Reading excel file with data
    # Can use converters to specify datatypes
    df = pandas.read_excel(_FILE,
                           sheet_name='Sets_Final'
                           # converters={'Date': pandas.to_datetime}
                        )

    # Insert data into DB connection from above
    df.to_sql(name=_TABLE,
              con=engine,
              if_exists='append',
              index=False,
              )

def merge_modify_import():
    # Connect to DB
    engine = create_engine(_ENGINE)

    # Pull lift table into DF
    lift_df = pandas.read_sql(_SQL, engine,)

    # Pull weight data from excel into DF
    ex_df = pandas.read_excel(_FILE,
                        sheet_name='Workouts_Edited',
                        converters={'Date': pandas.to_datetime},
                )

    # Join Lift DF to Exercise DF with lift name
    merge_df = pandas.merge(lift_df, ex_df, left_on='Lift_Name', right_on='LIFT_NAME')

    # Delete Lift Name and Body part column from exercise DF. Rename ID to Lift_ID
    merge_df = merge_df.drop(['Lift_Name', 'Body_Part', 'LIFT_NAME', 'PART'], axis=1)
    merge_df = merge_df.rename(index=str, columns={"ID":"Lift_ID"})

    # Load into the DB
    merge_df.to_sql(name=_TABLE,
              con=engine,
              if_exists='append',
              index=False,
              )

def export_to_excel():
    engine = create_engine(_ENGINE)
    # Get excercise ID and corresponding Lift ID
    # df = pandas.read_sql('Select e.*, l.lift_name From exercise e join lift l on e.lift_id = l.id', engine, )

    # Get full lift and exercise tables for backup
    ex_df = pandas.read_sql('Select * From exercise', engine, )
    lift_df = pandas.read_sql('Select * From lift', engine, )
    set_df = pandas.read_sql('Select * From workout_db.set', engine, )

    # Write DF to excel doc and save
    writer = pandas.ExcelWriter('DB_Export.xlsx')
    ex_df.to_excel(writer,'Exercise')
    lift_df.to_excel(writer,'Lift')
    set_df.to_excel(writer, 'Set')
    writer.save()

export_to_excel()