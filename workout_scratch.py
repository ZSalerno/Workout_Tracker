import pandas
import datetime
import json

from flask import Flask, render_template, request
from sqlalchemy import create_engine, Table, MetaData

_ENGINE = "mysql+mysqldb://python_user:PythonConn149147@localhost/workout_db"
_HISTORY_SQL = '''
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
'''
_LIFT_SQL = '''
    SELECT ID, Lift_Name 
    FROM Lift
'''
_DAYS_PER_YEAR_SQL = '''
SELECT YEAR(Date) AS 'Year', COUNT(*) AS 'Days'
FROM (
    SELECT DISTINCT Date
    FROM Exercise
) AS a
GROUP BY YEAR(Date)
'''
_DAYS_PER_MONTH_SQL = '''
SELECT YEAR(Date) AS 'Year', MONTH(Date) AS 'Month', count(*) AS 'Days'
FROM (
    SELECT DISTINCT Date
    FROM Exercise
) AS a
GROUP BY YEAR(Date), MONTH(Date)
ORDER BY YEAR(DATE), MONTH(Date)

'''
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
    days_per_year_df = pandas.read_sql(_DAYS_PER_YEAR_SQL, engine, )
    days_per_list = days_per_year_df.values.tolist()

    days_per_month_df = pandas.read_sql(_DAYS_PER_MONTH_SQL, engine, )
    days_per_month_list = days_per_month_df.values.tolist()

    days_per_labels = []
    days_per_values = []
    for year in days_per_list:
        days_per_labels.append(year[0])
        days_per_values.append(year[1])

    print(days_per_month_df)

    # Dictionary with list of lists for month,days for each year in DB
    dict = {}
    for year in days_per_month_df['Year'].unique():
        dict[year] = [[days_per_month_df['Month'][day], days_per_month_df['Days'][day]] for day in days_per_month_df[days_per_month_df['Year']==year].index]
    print(dict)


    # Generate this for all years in return value
    # label: 'Days Exercised Per Month 2017',
    # data: [
    #     { % for v in dpv %}"{{ v }}", { % endfor %}
    # ]

    return render_template('visualizations.html',
                           dpl=days_per_labels,
                           dpv=days_per_values,
                           dictionary_test=dict,
                           )

# Is this going to work or should I send this to javascript and figure out a way to loop there? This seems
# overly complicated

# What I need in javascript - for every year in dictionary - create datapoint. Might look the same?
#     data: dataFunction()
#     And then the function would create strings? Or just have each list....
#     You'd need the dictionary. Access the year for the first sentence. then the data based on the lists >>

    #{% for item in dict %} ,{
        # label: 'Days Exercised Per Month in {{ item.year }},
        # data: [
        #     {% for months in item.list %}"x: {{ months }}", y: {{ days }}, { % endfor %}
        # ],
#         }
#   {% endfor %} ],

    # data: [{
    #     x: 10, - month
    #     y: 20 - days
    # }, {
    #     x: 15,
    #     y: 10
    # }]


# def create_data(dict):
#     data_point=''
#
#     lbl = "label: 'Days Exercised Per Month {}"
#     data = "data: "
#     return data_point