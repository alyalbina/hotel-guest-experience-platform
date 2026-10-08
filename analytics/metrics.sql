-- Creation cohort, UTC; parameters: :start, :end, :department, :now.
-- NULL start/end/department means no restriction. Dates are inclusive.
WITH cohort AS (
  SELECT r.*,
    ROUND((julianday(responded_at)-julianday(created_at))*1440,6) AS response_minutes,
    ROUND((julianday(resolved_at)-julianday(created_at))*1440,6) AS resolution_minutes,
    ROUND((julianday(:now)-julianday(created_at))*1440,6) AS age_minutes
  FROM requests r
  WHERE (:start IS NULL OR created_at>=:start || 'T00:00:00Z')
    AND (:end IS NULL OR created_at<=:end || 'T23:59:59Z')
    AND (:department IS NULL OR department_id=:department)
)
SELECT
  COUNT(*) AS number_of_requests,
  COUNT(responded_at) AS responded_requests,
  ROUND(AVG(response_minutes),1) AS average_response_minutes,
  SUM(CASE WHEN status='resolved' THEN 1 ELSE 0 END) AS resolved_requests,
  ROUND(AVG(CASE WHEN status='resolved' THEN resolution_minutes END),1) AS average_resolution_minutes,
  ROUND(100.0*COUNT(CASE WHEN status='resolved' THEN 1 END)/NULLIF(COUNT(*),0),1) AS completion_rate,
  ROUND(100.0*COUNT(CASE WHEN status='resolved' AND resolution_minutes<=sla_minutes THEN 1 END)
    /NULLIF(COUNT(CASE WHEN status='resolved' THEN 1 END),0),1) AS sla_compliance,
  COUNT(first_resolved_at) AS ever_resolved_requests,
  ROUND(100.0*COUNT(CASE WHEN first_resolved_at IS NOT NULL AND reopen_count>0 THEN 1 END)
    /NULLIF(COUNT(first_resolved_at),0),1) AS reopened_requests_rate,
  COUNT(CASE WHEN status='resolved' THEN csat END) AS csat_responses,
  ROUND(AVG(CASE WHEN status='resolved' THEN csat END),1) AS csat_mean,
  ROUND(100.0*COUNT(CASE WHEN status='resolved' AND csat>=4 THEN 1 END)
    /NULLIF(COUNT(CASE WHEN status='resolved' THEN csat END),0),1) AS csat_positive_rate,
  ROUND(100.0*COUNT(CASE WHEN status='resolved' THEN csat END)
    /NULLIF(COUNT(CASE WHEN status='resolved' THEN 1 END),0),1) AS csat_response_rate,
  COUNT(CASE WHEN status NOT IN ('resolved','cancelled') THEN 1 END) AS active_requests,
  COUNT(CASE WHEN status NOT IN ('resolved','cancelled') AND age_minutes>sla_minutes THEN 1 END) AS overdue_active_requests
FROM cohort;
