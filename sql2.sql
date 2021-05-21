SELECT s.date, s.time, s.duration, a.activity
FROM schedule s, ActivityList a
WHERE s.activity_id = a.activity_id