SELECT "Top 3 users";

SELECT u.uid, SUM(l.cnt* so.duration) as s
FROM users u, sessions se, listen l, songs so, perform p
WHERE u.uid = se.uid 
AND se.sno = l.sno 
AND u.uid = l.uid
AND l.sid = p.sid 
AND p.aid = 'a1'
AND l.sid = so.sid
GROUP BY u.uid
ORDER BY  s DESC
LIMIT 3;

SELECT "Top 3 playlists";

SELECT pl.pid, pl.title, COUNT(*) as c
FROM playlists pl, plinclude pi,  perform p
WHERE pl.pid = pi.pid 
AND pi.sid = p.sid
AND p.aid = 'a1'
GROUP BY pl.pid, p.aid
ORDER BY c DESC
LIMIT 3;
