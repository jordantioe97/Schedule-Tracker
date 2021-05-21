from tkinter import *
import tkinter.font as font
import datetime as dt
import sqlite3

root = Tk()
root.title('Schedule Tracker')
root.geometry("400x800")

# Click command
def about_command():
    about = Tk()
    about.title('About')
    about.geometry("400x300")
    title_Font = font.Font(size=12)
    about_label = Label(about, text="About Schedule Tracker")
    about_label['font'] = title_Font
    about_label.place(x=200, y=20, anchor="center")

    description_label = Label(about, text="Created on 10/13/2020 by Jordan Tioe")
    description_label.place(x=10, y=50)
    description2_label = Label(about, text="Open Source Software")
    description2_label.place(x=10, y=75)

my_menu = Menu(root)
root.config(menu=my_menu)

# Create a menu item
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="About", command=about_command)


conn = sqlite3.connect('scheduletracker.db')

c = conn.cursor()

# Display all active activities in the dropdown menu
c.execute("SELECT activity, activity_id FROM ActivityList WHERE active='Y'")
ActivityList = []
while True:
    records = c.fetchone()
    if records is None:
        break
    ActivityList.append(records[0])

# Display all completion status from dropdown menu
c.execute("SELECT status, status_id FROM ActivityStatus")
CompletionStatus = []
while True:
    records = c.fetchone()
    if records is None:
        break
    CompletionStatus.append(records[0])

# Display all late status from dropdown menu
c.execute("SELECT late_status, late_id FROM LateStatus")
LateStatusList = []
while True:
    records = c.fetchone()
    if records is None:
        break
    LateStatusList.append(records[0])

# Radio button list for on-time status
OnTimeStatus = [
    ("YES", "YES"),
    ("NO", "NO"),
]

# Dropdown for AM or PM
AmPm = [
    "AM",
    "PM"
]

# Dropdown for duration in minutes
DurationList = [
    "30",
    "60",
    "90",
    "120"
]


# Update a record in database
def update():
    conn = sqlite3.connect('scheduletracker.db')
    c = conn.cursor()

    select_activity_editor = "SELECT activity_id FROM ActivityList WHERE active='Y' AND activity = "
    get_activity_editor = activity_editor.get()
    update_activity = select_activity_editor + "'" + get_activity_editor + "'"
    c.execute(update_activity)
    activity_id_rec = c.fetchone()
    activity_id = activity_id_rec[0]

    select_completion_editor = "SELECT status_id FROM ActivityStatus WHERE status = "
    get_completion_editor = completion_status_editor.get()
    update_completion = select_completion_editor + "'" + get_completion_editor + "'"
    c.execute(update_completion)
    status_id_rec = c.fetchone()
    status_id = status_id_rec[0]

    select_late_editor = "SELECT late_id FROM LateStatus WHERE late_status = "
    get_late_editor = late_status_editor.get()
    update_late = select_late_editor + "'" + get_late_editor + "'"
    c.execute(update_late)
    late_id_rec = c.fetchone()
    late_id = late_id_rec[0]

    record_id = delete_box.get()
    c.execute("""UPDATE schedule SET
        date = :date,
        time = :time,
        amOrpm = :amOrpm,
        activity_id = :activity_id,
        duration = :duration,
        ontime = :ontime,
        late_id = :late_id,
        status_id = :status_id

        WHERE oid = :oid""",
              {
                  'date': date_editor.get(),
                  'time': time_editor.get(),
                  'amOrpm': time_AmPm_editor.get(),
                  'activity_id': activity_id,
                  'duration': duration_editor.get(),
                  'ontime': ontime_editor.get(),
                  'late_id': late_id,
                  'status_id': status_id,
                  'oid': record_id
              })

    conn.commit()
    conn.close()
    editor.destroy()


# Edit a record in database
def edit():
    global editor
    editor = Tk()
    editor.title('Update A Record')
    editor.geometry("400x300")
    conn = sqlite3.connect('scheduletracker.db')
    c = conn.cursor()

    record_id = delete_box.get()
    select_schedule = "SELECT date, time, amOrpm, activity, duration, ontime, late_status, status "
    from_schedule = "FROM schedule, ActivityList, LateStatus, ActivityStatus "
    where_schedule = "WHERE schedule.activity_id = ActivityList.activity_id AND schedule.late_id = LateStatus.late_id "
    and_schedule = "AND schedule.status_id = ActivityStatus.status_id AND schedule.oid = "
    execute_schedule = select_schedule + from_schedule + where_schedule + and_schedule
    c.execute(execute_schedule + record_id)
    records = c.fetchall()

    # Create Global Variables for text box names
    global date_editor
    global time_editor
    global time_AmPm_editor
    global activity_editor
    global duration_editor
    global ontime_editor
    global late_status_editor
    global completion_status_editor

    # Text Bpxes
    date_editor = Entry(editor, width=25)
    date_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

    time_editor = Entry(editor, width=25)
    time_editor.grid(row=1, column=1, padx=20, pady=(10, 0))

    time_AmPm_editor = StringVar(editor)
    time_AmPm_editor_opt = OptionMenu(editor, time_AmPm_editor, *AmPm)
    time_AmPm_editor_opt.grid(sticky="E", row=1, column=1)

    activity_editor = StringVar(editor)
    activity_editor_opt = OptionMenu(editor, activity_editor, *ActivityList)
    activity_editor_opt.grid(row=2, column=1)

    duration_editor = StringVar(editor)
    duration_editor_opt = OptionMenu(editor, duration_editor, *DurationList)
    duration_editor_opt.grid(row=3, column=1)

    ontime_editor = StringVar(editor)
    Radiobutton(editor, text="YES", variable=ontime_editor, value="YES").grid(row=4, column=1, padx="50", sticky="W")
    Radiobutton(editor, text="NO", variable=ontime_editor, value="NO").grid(row=4, column=1, padx="50", sticky="E")
    ontimeLabel_editor = Label(editor, text=ontime_editor.get())
    ontimeLabel_editor.grid(row=5, column=1)

    late_status_editor = StringVar(editor)
    late_status_editor_opt = OptionMenu(editor, late_status_editor, *LateStatusList)
    late_status_editor_opt.grid(row=5, column=1)

    completion_status_editor = StringVar(editor)
    completion_status_editor_opt = OptionMenu(editor, completion_status_editor, *CompletionStatus)
    completion_status_editor_opt.grid(row=6, column=1)

    # Text Box Labels
    date_label = Label(editor, text="Date (MM/DD/YYYY)")
    date_label.grid(row=0, column=0, pady=(10, 0))

    time_label = Label(editor, text="Time (hh:mm)")
    time_label.grid(row=1, column=0, pady=(10, 0))

    activity_label = Label(editor, text="Activity")
    activity_label.grid(row=2, column=0)

    duration_label = Label(editor, text="Duration \n(in minutes)")
    duration_label.grid(row=3, column=0)

    ontime_label = Label(editor, text="On Time?")
    ontime_label.grid(row=4, column=0)

    late_status_label = Label(editor, text="If no, how late?")
    late_status_label.grid(row=5, column=0)

    completion_status_label = Label(editor, text="Completion Status")
    completion_status_label.grid(row=6, column=0)

    for record in records:
        date_editor.insert(0, record[0])
        time_editor.insert(0, record[1])
        time_AmPm_editor.set(record[2])
        activity_editor.set(record[3])
        duration_editor.set(record[4])
        ontime_editor.set(record[5])
        late_status_editor.set(record[6])
        completion_status_editor.set(record[7])

    # Button to save edited record
    edit_btn = Button(editor, text="Save Record", command=update)
    edit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=145)


# Delete a record from the database
def delete():
    conn = sqlite3.connect('scheduletracker.db')
    c = conn.cursor()
    c.execute("DELETE from schedule WHERE oid = " + delete_box.get())

    conn.commit()
    conn.close()


# Add record to database
def addRecord():
    conn = sqlite3.connect('scheduletracker.db')
    c = conn.cursor()

    select_activity = "SELECT activity_id FROM ActivityList WHERE active='Y' AND activity = "
    get_activity = activity.get()
    add_activity = select_activity + "'" + get_activity + "'"
    c.execute(add_activity)
    activity_id_rec = c.fetchone()
    activity_id = activity_id_rec[0]

    default_date = date.get()
    default_time = time.get()
    default_AmPm = time_AmPm.get()

    c.execute("INSERT INTO schedule VALUES (:date, :time, :amOrpm, :activity_id, :duration, :ontime, :late_id, :status_id)",
              {
                  'date': date.get(),
                  'time': time.get(),
                  'amOrpm': time_AmPm.get(),
                  'activity_id': activity_id,
                  'duration': duration.get(),
                  'ontime': 'NO',
                  'late_id': '0',
                  'status_id': '0'
              })
    conn.commit()
    conn.close()

    date.delete(0, END)
    date.insert(0, default_date)
    time.delete(0, END)
    time.insert(0, default_time)
    time_AmPm.set('')
    time_AmPm.set(default_AmPm)
    activity.set('')
    duration.set('')

# Query a scheduled date from the database and display the record id, time, and activity
def query():
    conn = sqlite3.connect('scheduletracker.db')
    c = conn.cursor()

    select_query = "SELECT date,time, amOrpm, activity, schedule.oid FROM schedule, ActivityList WHERE schedule.activity_id=ActivityList.activity_id AND date = "
    get_query = "'" + query_date.get() + "'"
    execute_query = select_query + get_query
    c.execute(execute_query)

    records = c.fetchall()
    scheduleDisplay = str(query_date.get())
    query_title = Label(root, text="Schedule for " + scheduleDisplay)
    myFont = font.Font(size=12)
    query_title['font'] = myFont
    query_title.grid(row=10, column=0, columnspan=2)

    print_records = ''
    for record in records:
        print_records += str(record[4]) + ": " + str(record[1]) + " " + str(record[2]) + \
                         " " + str(record[3]) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=11, column=0, columnspan=2)

    conn.commit()
    conn.close()

# Evaluate schedule for a date
def evaluate():
    conn = sqlite3.connect('scheduletracker.db')
    c = conn.cursor()

    evaluate_title = Label(root, text="Evaluating Schedule for " + str(query_date.get()))
    myFont = font.Font(size=12)
    evaluate_title['font'] = myFont
    evaluate_title.grid(row=12, column=0, columnspan=2)

    penalty = 0
    c.execute("SELECT schedule.late_id, penalty_point FROM schedule, LateStatus WHERE schedule.late_id = LateStatus.late_id AND date = '" + query_date.get() + "'")
    late_id_List = []
    penalty_counter = 0
    while True:
        late_record = c.fetchone()
        if late_record is None:
            break
        late_id_List.append(late_record[0])
        penalty = penalty + late_record[1]
        penalty_counter = penalty_counter + 1

    if penalty_counter == 0:
        penalty_counter = 1

    total_penalty_late = round(penalty / penalty_counter)
    late_penalty_label = Label(root, text="Penalty for late = " + str(-total_penalty_late))
    late_penalty_label.grid(row=13, column=0, columnspan=2)

    c.execute("SELECT schedule.status_id, penalty_point FROM schedule, ActivityStatus WHERE schedule.status_id = ActivityStatus.status_id AND date = '" + query_date.get() + "'")
    status_id_List = []
    penalty = 0
    penalty_counter = 0
    while True:
        status_record = c.fetchone()
        if status_record is None:
            break
        status_id_List.append(status_record[0])
        penalty = penalty + status_record[1]
        penalty_counter = penalty_counter + 1

    if penalty_counter == 0:
        penalty_counter = 1

    total_penalty_status = round(penalty / penalty_counter)
    completion_penalty_label = Label(root, text="Penalty for completion = " + str(-total_penalty_status))
    completion_penalty_label.grid(row=14, column=0, columnspan=2)

    total_penalty = total_penalty_late + total_penalty_status
    final_score = 100 - total_penalty

    if final_score >= 90:
        score_label = Label(root, text="Great Job!\nFinal Score: " + str(final_score))
        score_label.grid(row=15, column=0, columnspan=2)
    elif final_score >= 80:
        score_label = Label(root, text="Good Job! You followed the schedule well, "
            "\nbut there is still some room for improvement. "
            "\nFinal Score: " + str(final_score))
        score_label.grid(row=15, column=0, columnspan=2)
    elif final_score >= 70:
        score_label = Label(root, text="You followed the schedule reasonably well, "
            "\nbut still needs improvement. Try to plan more accordingly. "
            "\nFinal Score: " + str(final_score))
        score_label.grid(row=15, column=0, columnspan=2)
    else:
        score_label = Label(root, text="You failed to follow the schedule effectively, "
            "\nTry to set goals on what you need to accomplish for the day. "
            "\nFinal Score: " + str(final_score))
        score_label.grid(row=15, column=0, columnspan=2)
    conn.commit()
    conn.close()


# Text Boxes
date = Entry(root, width=25)
date.grid(row=1, column=1, padx=20, pady=(10, 0))

time = Entry(root, width=25)
time.grid(row=2, column=1, padx=20, pady=(10, 0))

time_AmPm = StringVar(root)
time_AmPm.set("AM")
time_AmPm_opt = OptionMenu(root, time_AmPm, *AmPm)
time_AmPm_opt.grid(sticky="e", row=2, column=1)

activity = StringVar(root)
activity.set("")
activity_opt = OptionMenu(root, activity, *ActivityList)
activity_opt.grid(row=3, column=1)

duration = StringVar(root)
duration.set("60")
duration_opt = OptionMenu(root, duration, *DurationList)
duration_opt.grid(row=4, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=8, column=1, pady=5)

current_date = dt.datetime.now()
format_date = f"{current_date:%m/%d/%Y}"

# Text Box Labels
date_display_label = Label(root, text="Today: " + str(format_date))
date_display_label.grid(row=0, column=1, pady=(10, 0))

date_label = Label(root, text="Date (MM/DD/YYYY)")
date_label.grid(row=1, column=0, pady=(10, 0))

time_label = Label(root, text="Time (hh:mm)")
time_label.grid(row=2, column=0, pady=(10, 0))

activity_label = Label(root, text="Activity")
activity_label.grid(row=3, column=0)

duration_label = Label(root, text="Duration \n(in minutes)")
duration_label.grid(row=4, column=0)

delete_box_label = Label(root, text="Select ID to Edit or Delete")
delete_box_label.grid(row=8, column=0)

# Add record to database
add_btn = Button(root, text="Add Record To Database", command=addRecord)
add_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Query from a scheduled date
query_date_label = Label(root, text="Enter a scheduled date")
query_date_label.grid(row=6, column=0, pady=(10, 0))
query_date = Entry(root, width=25)
query_date.grid(row=6, column=1, padx=20, pady=(10, 0))
query_btn = Button(root, text="Display schedule", command=query)
query_btn.grid(row=7, column=0, pady=10, padx=10, ipadx=15)

# Edit Button
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=9, column=0, pady=10, padx=10, ipadx=25)

# Delete Button
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=9, column=1, pady=10, padx=10, ipadx=18)

# Evaluate overall schedule for a date
evaluate_btn = Button(root, text="Evaluate schedule", command=evaluate)
evaluate_btn.grid(row=7, column=1, pady=10, padx=10, ipadx=13)

conn.commit()

conn.close()

root.mainloop()
