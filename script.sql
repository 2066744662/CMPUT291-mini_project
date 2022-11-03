SELECT a.name, s.sid, s.title, s.duration
FROM artists a, perform p, songs s 
WHERE s.sid = :sid
AND p.sid = s.sid
AND p.aid = a.aid