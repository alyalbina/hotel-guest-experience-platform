-- Apply the same created-date cohort to these breakdowns.
SELECT d.name AS department, COUNT(*) AS requests
FROM requests r JOIN departments d ON d.id=r.department_id
WHERE (:start IS NULL OR r.created_at>=:start || 'T00:00:00Z')
 AND (:end IS NULL OR r.created_at<=:end || 'T23:59:59Z')
 AND (:department IS NULL OR r.department_id=:department)
GROUP BY d.name ORDER BY requests DESC;

SELECT substr(created_at,1,10) AS day_utc, COUNT(*) AS requests
FROM requests
WHERE (:start IS NULL OR created_at>=:start || 'T00:00:00Z')
 AND (:end IS NULL OR created_at<=:end || 'T23:59:59Z')
 AND (:department IS NULL OR department_id=:department)
GROUP BY day_utc ORDER BY day_utc;
