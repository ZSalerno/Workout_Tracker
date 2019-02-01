import pandas
import datetime
import json
import numpy

from flask import Flask, render_template, request
from sqlalchemy import create_engine, Table, MetaData, text

_ENGINE = "mysql+mysqldb://python_user:PythonConn149147@localhost/workout_db"
_HISTORY_SQL = text('''
    SELECT e.Date
            , l.Lift_Name AS 'Lift'
            , l.Body_Part AS 'Body Part'
            , s.Weight
            , CONCAT(s.Sets,'x',s.Reps) As 'Sets & Reps'
            , e.Comments
    FROM workout_db.exercise e
    JOIN workout_db.lift l on l.id = e.lift_id
    JOIN workout_db.sets s on s.exercise_id = e.id
    ORDER BY e.Date desc, l.Body_Part asc, l.Lift_Name asc, s.Reps desc, s.Weight desc
''')

_HISTORY_SQL_TEST = '''SELECT e.Date, l.Lift_Name AS Lift, l.Body_Part, s.Weight, s.Sets, e.Comments 
    FROM workout_db.exercise e JOIN workout_db.lift l on l.id = e.lift_id
    JOIN workout_db.sets s on s.exercise_id = e.id 
    ORDER BY e.Date desc, l.Body_Part asc, l.Lift_Name asc, s.Reps desc, s.Weight desc'''

_LIFT_SQL = text('''
    SELECT ID
            , Lift_Name 
    FROM Lift
''')

_DAYS_PER_YEAR_SQL = text('''
    SELECT YEAR(Date) AS 'Year', COUNT(*) AS 'Days'
    FROM (
        SELECT DISTINCT Date
        FROM Exercise
    ) AS a
    GROUP BY YEAR(Date)
    ''')

_DAYS_PER_MONTH_SQL = text('''
    SELECT YEAR(Date) AS 'Year', MONTHNAME(Date) AS 'Month', count(*) AS 'Days'
    FROM (
        SELECT DISTINCT Date
        FROM Exercise
    ) AS a
    GROUP BY YEAR(Date), MONTH(Date)
    ORDER BY YEAR(DATE), MONTH(Date)
''')

app = Flask(__name__)

# dtypes={
#         'Date':'str',
#         'Exercise':'str',
#         'Part':'str',
#         'Weight':'int',
#         'Sets':'int',
#         'Reps':'int',
#     }
# df = pandas.read_excel('C:/Users/zack/PycharmProjects/Workout_Tracker/static/Workouts.xlsx',
#                        converters={'Date': pandas.to_datetime}
#                        )

engine = create_engine(_ENGINE)

@app.route('/')
def base():
    return render_template('base.html')


@app.route('/workouts/', methods=["POST", "GET"])
def workouts():

    # Get data for historical view and select list
    history_df = pandas.read_sql(_HISTORY_SQL, engine,)
    lift_df = pandas.read_sql(_LIFT_SQL, engine,)

    # Creates historical table
    html = history_df.to_html(
        classes=["table", "table-striped", "table-bordered", "table-sm"],
        index=False,
        table_id="historyTable"
    )

    # Create select list and get today's date for date column
    lift_list = lift_df.values.tolist()
    today_date = datetime.date.today()

    return render_template('gym.html', data=html, lifts=lift_list, today=today_date)


# Function to save exercise.
@app.route('/saveExercise', methods=["POST", "GET"])
def saveExercise():
    print("### SAVING EXERCISE ###")

    # Get table variables for insert statements
    meta = MetaData()
    exercises_table = Table('exercise', meta, autoload=True, autoload_with=engine)
    sets_table = Table('sets', meta, autoload=True, autoload_with=engine)

    # Check if comments is an empty string. If so, change to none
    if request.args.get("comments") == '':
        comment_value = None
    else:
        comment_value = request.args.get("comments")

    # Create exercise insert object. Create connection object and insert into DB
    ins_ex = exercises_table.insert().values(
        Date=request.args.get("date"),
        Lift_ID=request.args.get("lift"),
        Comments=comment_value,
    )
    conn = engine.connect()
    print("### INSERTING INTO EXERCISE TABLE ###")
    print(ins_ex.compile().params)
    result = conn.execute(ins_ex)

    # Create set insert object. Use result of exercise insert for exercise id. Insert into DB
    set_ins = sets_table.insert().values(
        Sets=request.args.get("sets"),
        Reps=request.args.get("reps"),
        Weight=request.args.get("weight"),
        Exercise_ID=result.inserted_primary_key[0],
    )
    print("### INSERTING INTO SETS TABLE ###")
    print(set_ins.compile().params)
    result=conn.execute(set_ins)

    # TODO
    # Save copied rows
    # How to do - need to enforce exercise table only having one record where date and lift id are the same
    # Create hash column based on date/lift id. must be unique
    # Check hash to get exercise id and save sets?
    # Or send exercise id back to html table....then save the sets
    # Save all records?

    # Need to check if row exists already before saving
    # Need to do a freeze on the row while ajax saves - have gif saved. need div on top of table that shows during ajax call
    # Need to change row color after record is saved
    print("test")

    return json.dumps({'status': 'OK', 'data': request.args})


@app.route('/visualizations')
def visualizations():

    ##### DAYS PER YEAR
    days_per_year_df = pandas.read_sql(_DAYS_PER_YEAR_SQL, engine, )
    days_per_list = days_per_year_df.values.tolist()

    days_per_labels = []
    days_per_values = []
    for year in days_per_list:
        days_per_labels.append(year[0])
        days_per_values.append(year[1])

    ##### DAYS PER MONTH
    # Dictionary with list of dictionaries for month,days for each year in DB
    days_per_month_df = pandas.read_sql(_DAYS_PER_MONTH_SQL, engine, )
    dpm_dict = {}
    for year in days_per_month_df['Year'].unique():
        dpm_dict[year] = [{"x":days_per_month_df['Month'][day], "y":days_per_month_df['Days'][day]} for day in days_per_month_df[days_per_month_df['Year']==year].index]

    ##### LIFTS OVER TIME
    history_df = pandas.read_sql(_HISTORY_SQL, engine, )
    # Lots of work to get from datetime objects to unique list of date strings
    dates = history_df.Date.unique()
    dates = numpy.sort(dates).tolist()
    for i, date in enumerate(dates):
        dates[i] = dates[i].strftime('%m/%d/%Y')

    # Some issue with dates that arent working as datetimes
    # history_df['Date'] = history_df['Date'].dt.strftime('%m/%d/%Y', errors='coerce')
    # print(history_df)

    lot_dict = {}
    for lift in history_df['Lift'].unique():
        lot_dict[lift] = [{"x":history_df['Date'][weight].strftime('%m/%d/%Y'), "y":history_df['Weight'][weight]} for weight in history_df[history_df['Lift']==lift].index]

    # Create lifts for dropdown selection
    lift_df = pandas.read_sql(_LIFT_SQL, engine, )
    lift_list = lift_df.values.tolist()

    print(lot_dict)

    return render_template('visualizations.html',
                            dpl=days_per_labels,
                            dpv=days_per_values,
                            dpm_dict=dpm_dict,
                            dates = dates,
                            lot_dict=lot_dict,
                            lifts=lift_list
                           )
