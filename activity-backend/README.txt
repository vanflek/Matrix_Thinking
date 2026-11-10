Matrix Thinking game activity — deployed 2026-11-07 (America/Los_Angeles)

Frontend: game-activity.js, shared by all ten published interactive pages.
Backend: matrix-game-events.vanflek.workers.dev; Cloudflare Workers Free.
D1: matrix-game-activity, binding DB; ID e01a11b3-c4e0-438f-8ef1-546eddb0665b.
The main book-code branch and the GitHub Pages CNAME must remain unchanged.

Reports are private in the owner's Cloudflare account:
https://dash.cloudflare.com/1647630b32722aea2a9cb5b7abe64b7a/workers/d1/databases/e01a11b3-c4e0-438f-8ef1-546eddb0665b/console
Run: SELECT * FROM game_engagement ORDER BY engaged_sessions DESC;
This view excludes QA and groups the last 30 UTC days by laboratory.
For daily results use report.sql; for action coverage inspect game_daily.

Interpretation:
interacted = at least one approved trusted DOM interaction, once per page session.
engaged = at least three debounced actions and five focused/visible active seconds.
active30 / active120 = same action requirement and 30 / 120 active seconds.
Active time stops after 60 seconds without interaction. Page reloads and new tabs
start independent sessions. Sessions are NOT unique people; automation may imitate
trusted browser input. Missing counts may reflect DNT/GPC, blockers or failures.
Different milestone days can differ for sessions crossing midnight UTC.
Action categories are recorded once per session, not raw click/keypress totals.

Only fixed game/event names, UTC day, test flag and random page UUID enter D1.
No cookies or persistent browser ID. Dedup rows older than 14 days are cleaned
opportunistically; aggregate totals remain. Normal Cloudflare network/service
logs follow the provider's policies. No public statistics endpoint exists.
?analytics=off disables the additional collector. DNT and GPC are respected.
?activity_test=1 routes manual QA events to test=1, excluded from reports.
No retrospective classification of the earlier CSTA visits is possible.

Checks:
node activity/check-activity.cjs
python activity/check-database.py
python activity/check-markup.py
python validate-site.py (run from the main workspace)

Deployment source: worker.js and schema.sql; use Cloudflare dashboard code editor
and D1 console. Flatten whitespace before pasting SQL into the single-line console.
Never put Cloudflare API tokens, database access tokens or private reports in the
public frontend or GitHub Pages branch. The frontend endpoint URL is public.

Micro:bit added 2026-11-09: step records A and brightness B; restart records shake and shift B reset; inspect records cell selection; control records experiment selection. Each category is a per-session milestone, not a raw count of button presses. The existing engagement thresholds and privacy exclusions are unchanged.
