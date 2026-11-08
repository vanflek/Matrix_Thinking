CREATE TABLE IF NOT EXISTS game_events (
  day TEXT NOT NULL, game TEXT NOT NULL, session TEXT NOT NULL,
  event TEXT NOT NULL, test INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, game, session, event, test)
) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS game_daily (
  day TEXT NOT NULL, game TEXT NOT NULL, event TEXT NOT NULL,
  test INTEGER NOT NULL DEFAULT 0, total INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, game, event, test)
) WITHOUT ROWID;
CREATE TRIGGER IF NOT EXISTS count_game_event AFTER INSERT ON game_events
BEGIN
  INSERT INTO game_daily (day,game,event,test,total)
  VALUES (NEW.day,NEW.game,NEW.event,NEW.test,1)
  ON CONFLICT(day,game,event,test) DO UPDATE SET total=total+1;
END;
CREATE VIEW IF NOT EXISTS game_engagement AS
SELECT game,
 SUM(CASE WHEN event='interacted' THEN total ELSE 0 END) AS interactive_sessions,
 SUM(CASE WHEN event='engaged' THEN total ELSE 0 END) AS engaged_sessions,
 SUM(CASE WHEN event='active30' THEN total ELSE 0 END) AS active_30s,
 SUM(CASE WHEN event='active120' THEN total ELSE 0 END) AS active_2min
FROM game_daily WHERE test=0 AND day >= date('now','-30 days')
GROUP BY game;
