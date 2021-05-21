import tkinter as tk
import sqlite3

window = tk.Tk()
window.title("Schedule Tracker")
window.geometry("500x500")

conn = sqlite3.connect('ScheduleTracker.db')
c = conn.cursor()
'''
c.execute("""CREATE TABLE schedule (
        time text,
        activity text,
        duration text,
        ontime text,
        late_status text,
        completion_status text
        )""")
'''
ActivityList = [
"Aries",
"Taurus",
"Gemini",
"Cancer"
]

CompletionStatus = [
    "Incomplete",
    "Half Complete",
    "Mostly Complete",
    "Complete"
]

def save():
    conn = sqlite3.connect('Database1.db')
    c = conn.cursor()
    c.execute("INSERT INTO schedule VALUES (:time, :activity, :duration, :ontime, :late_status, :completion_status)",
              {
                  'time': time_entry.get(),
                  'activity': activity_variable.get(),
                  'duration': duration_entry.get(),
                  'ontime': v.get(),
                  'late_status': late_status_entry.get(),
                  'completion_status': completion_status_variable.get()
              })
    conn.commit()
    conn.close()

def query():
    conn = sqlite3.connect('Database1.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM schedule")
    records = c.fetchall()
    print(records)

    print_records = ''
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" + str(record[6]) + "\n"

    query_label = tk.Label(text=print_records)
    query_label.place(x=10,y=330)

    conn.commit()
    conn.close()

time_label = tk.Label(text="Time:")
time_entry = tk.Entry()
time_label.place(x=0,y=10)
time_entry.place(x=60,y=10)

activity_label = tk.Label(text="Activity:")
activity_label.place(x=0,y=40)
activity_variable = tk.StringVar(window)
activity_variable.set(ActivityList[0])
activity_opt = tk.OptionMenu(window, activity_variable, *ActivityList)
activity_opt.place(x=60,y=35)

duration_label = tk.Label(text="Duration:")
duration_entry = tk.Entry()
duration_label.place(x=0,y=70)
duration_entry.place(x=60,y=70)

ontime_label = tk.Label(text="On time?")
ontime_label.place(x=0,y=105)
v = tk.StringVar(window, "0")
tk.Radiobutton(window, text = "YES", variable = v, value = 1, indicator = 0, background = "light blue").place(x=60,y=100)
tk.Radiobutton(window, text = "NO", variable = v, value = 2, indicator = 0, background = "light blue").place(x=110,y=100)

late_status_label = tk.Label(text="If no, how late? \n(in minutes)")
late_status_entry = tk.Entry()
late_status_label.place(x=0,y=135)
late_status_entry.place(x=100,y=145)

completion_status_label = tk.Label(text="Completion status:")
completion_status_label.place(x=0,y=197)
completion_status_variable = tk.StringVar(window)
completion_status_variable.set(CompletionStatus[0])
completion_status_opt = tk.OptionMenu(window, completion_status_variable, *CompletionStatus)
completion_status_opt.place(x=110,y=192)

save_entry = tk.Button(text="Save Entry",width=8,height=1, command=save)
save_entry.place(x=10,y=270)
query_btn = tk.Button(text="Show Records", command=query)
query_btn.place(x=10,y=300)

conn.commit()

conn.close()

window.mainloop()