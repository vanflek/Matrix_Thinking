-- Daily totals use UTC. Sessions are page loads with interaction, NOT unique people.
SELECT day, game,
 SUM(CASE WHEN event='interacted' THEN total ELSE 0 END) AS interactive_sessions,
 SUM(CASE WHEN event='engaged' THEN total ELSE 0 END) AS engaged_sessions,
 SUM(CASE WHEN event='active30' THEN total ELSE 0 END) AS active_30s,
 SUM(CASE WHEN event='active120' THEN total ELSE 0 END) AS active_2min
FROM game_daily WHERE test=0 AND day >= date('now','-30 days')
GROUP BY day,game ORDER BY day DESC,engaged_sessions DESC;
