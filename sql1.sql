SELECT schedule.time, ActivityList.ID, ActivityList.activity
FROM schedule
INNER JOIN ActivityList ON schedule.activity=ActivityList.activity;