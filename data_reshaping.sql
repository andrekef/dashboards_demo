SELECT
    id,
    created_at,
    state,
    MAX(CASE WHEN state = 'started' THEN occurred_at END) AS started_time,
    MAX(CASE WHEN state = 'finished' THEN occurred_at END) AS finished_time,
    MAX(CASE WHEN state = 'delivered' THEN occurred_at END) AS delivered_time,
    MAX(CASE WHEN state = 'accepted' THEN occurred_at END) AS acceptance_time,
    (strftime('%s', MAX(CASE WHEN state = 'finished' THEN occurred_at END)) -
     strftime('%s', MAX(CASE WHEN state = 'started' THEN occurred_at END))) / 3600.0 AS development_time_hours,
    (strftime('%s', MAX(CASE WHEN state = 'delivered' THEN occurred_at END)) -
     strftime('%s', MAX(CASE WHEN state = 'finished' THEN occurred_at END))) / 3600.0 AS alpha_test_time_hours,
     (strftime('%s', MAX(CASE WHEN state = 'accepted' THEN occurred_at END)) -
     strftime('%s', MAX(CASE WHEN state = 'delivered' THEN occurred_at END))) / 3600.0 AS staging_test_time_hours,
     (strftime('%s', MAX(CASE WHEN state = 'accepted' THEN occurred_at END)) -
     strftime('%s', MAX(CASE WHEN state = 'started' THEN occurred_at END))) / 3600.0 AS total_delivery_time_hours
FROM
    story_transitions_view
WHERE
    state IN ('started', 'finished', 'delivered', 'accepted')
GROUP BY
    id
HAVING
    development_time_hours > 0
    AND alpha_test_time_hours > 0
    AND staging_test_time_hours > 0
    AND total_delivery_time_hours > 0
ORDER BY
    id