-- INSERT artists
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('art0', 'Amir Tamino', 'Belgian', 'art0pwd');
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('art1', 'Gotye', 'Belgian', 'gotyPWD');
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('art2', 'Hozier', 'Irish', 'hoziier');
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('art3', 'Kimbera', 'New Zealand', '33Kimbera');
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('id00', 'Adna', 'Bosnia', 'myPassword');
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('art4', 'Ozzy Osbourne', 'English', 'ozzy');
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('art5', 'Lomelda', 'American', 'abcd');
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('art6', 'Flame', 'American', '1111');
INSERT INTO artists (aid, name, nationality, pwd) VALUES ('art7', 'Maren Morris', 'American', 'aabb');


-- INSERT users
INSERT INTO users (uid, name, pwd) VALUES ('id00', 'Frodo Baggins', 'myPassword');
INSERT INTO users (uid, name, pwd) VALUES ('usr0', 'Samwise Gamgee', 'samsam');
INSERT INTO users (uid, name, pwd) VALUES ('usr1', 'Gandalf the Grey', 'gandalf');
INSERT INTO users (uid, name, pwd) VALUES ('usr2', 'Gandalf the Grey', 'you shall not PASS');

-- INSERT songs
INSERT INTO songs (sid, title, duration) VALUES (0, 'Habibi', 302);
INSERT INTO songs (sid, title, duration) VALUES (1, 'So it Goes', 297);
INSERT INTO songs (sid, title, duration) VALUES (2, 'Indigo Night', 254);
INSERT INTO songs (sid, title, duration) VALUES (3, 'The Flame', 266);
INSERT INTO songs (sid, title, duration) VALUES (4, 'Sunflower', 263);
INSERT INTO songs (sid, title, duration) VALUES (5, 'Somebody That I Used To Know', 244);
INSERT INTO songs (sid, title, duration) VALUES (6, 'Hearts A Mess', 365);
INSERT INTO songs (sid, title, duration) VALUES (7, 'Nobody', 210);
INSERT INTO songs (sid, title, duration) VALUES (8, 'Movement', 237);
INSERT INTO songs (sid, title, duration) VALUES (9, 'Talk', 206);
INSERT INTO songs (sid, title, duration) VALUES (10, 'Cherry Wine', 240);
INSERT INTO songs (sid, title, duration) VALUES (11, 'In the Woods Somewhere', 331);
INSERT INTO songs (sid, title, duration) VALUES (12, 'Save Me', 267);
INSERT INTO songs (sid, title, duration) VALUES (13, 'Settle Down', 240);
INSERT INTO songs (sid, title, duration) VALUES (14, 'Night', 240);
INSERT INTO songs (sid, title, duration) VALUES (15, 'Dreamer', 249);
INSERT INTO songs (sid, title, duration) VALUES (16, 'The Prettiest', 198);
INSERT INTO songs (sid, title, duration) VALUES (17, 'Living', 281);
INSERT INTO songs (sid, title, duration) VALUES (18, 'Dreamer', 285);
INSERT INTO songs (sid, title, duration) VALUES (19, 'Talk', 70);
INSERT INTO songs (sid, title, duration) VALUES (20, 'Tell', 109);
INSERT INTO songs (sid, title, duration) VALUES (21, 'Somebody That I Used To Know (Live)', 244);
INSERT INTO songs (sid, title, duration) VALUES (22, 'Somebody That I Used To Know (Acoustic)', 244);
INSERT INTO songs (sid, title, duration) VALUES (23, 'Watcher', 294);
INSERT INTO songs (sid, title, duration) VALUES (24, 'GIRL', 250);


-- INSERT performs
INSERT INTO perform (aid, sid) VALUES ('art0', 0);
INSERT INTO perform (aid, sid) VALUES ('art0', 1);
INSERT INTO perform (aid, sid) VALUES ('art0', 2);
INSERT INTO perform (aid, sid) VALUES ('art0', 3);
INSERT INTO perform (aid, sid) VALUES ('art0', 4);
INSERT INTO perform (aid, sid) VALUES ('art1', 5);
INSERT INTO perform (aid, sid) VALUES ('art1', 6);
INSERT INTO perform (aid, sid) VALUES ('art2', 7);
INSERT INTO perform (aid, sid) VALUES ('art2', 8);
INSERT INTO perform (aid, sid) VALUES ('art2', 9);
INSERT INTO perform (aid, sid) VALUES ('art2', 10);
INSERT INTO perform (aid, sid) VALUES ('art2', 11);
INSERT INTO perform (aid, sid) VALUES ('art3', 5);
INSERT INTO perform (aid, sid) VALUES ('art3', 12);
INSERT INTO perform (aid, sid) VALUES ('art3', 13);
INSERT INTO perform (aid, sid) VALUES ('id00', 14);
INSERT INTO perform (aid, sid) VALUES ('id00', 15);
INSERT INTO perform (aid, sid) VALUES ('id00', 16);
INSERT INTO perform (aid, sid) VALUES ('id00', 17);
INSERT INTO perform (aid, sid) VALUES ('art4', 18);
INSERT INTO perform (aid, sid) VALUES ('art5', 19);
INSERT INTO perform (aid, sid) VALUES ('art5', 20);
INSERT INTO perform (aid, sid) VALUES ('art6', 23);
INSERT INTO perform (aid, sid) VALUES ('art1', 21);
INSERT INTO perform (aid, sid) VALUES ('art1', 22);
INSERT INTO perform (aid, sid) VALUES ('art7', 24);


-- INSERT playlists
INSERT INTO playlists (pid, title, uid) VALUES (0, 'Nobody MOVE', 'id00');
INSERT INTO playlists (pid, title, uid) VALUES (1, 'Save Me a Cherry Wine', 'usr1');
INSERT INTO playlists (pid, title, uid) VALUES (2, 'talk to a dreamer', 'usr1');
INSERT INTO playlists (pid, title, uid) VALUES (3, 'Somebody''s favs', 'usr0');


-- INSERT plinclude
INSERT INTO plinclude (pid, sid, sorder) VALUES (0, 11, 0);
INSERT INTO plinclude (pid, sid, sorder) VALUES (3, 11, 2);
INSERT INTO plinclude (pid, sid, sorder) VALUES (3, 7, 0);
INSERT INTO plinclude (pid, sid, sorder) VALUES (3, 8, 1);
INSERT INTO plinclude (pid, sid, sorder) VALUES (3, 9, 3);
INSERT INTO plinclude (pid, sid, sorder) VALUES (3, 10, 4);
INSERT INTO plinclude (pid, sid, sorder) VALUES (1, 7, 0);
INSERT INTO plinclude (pid, sid, sorder) VALUES (1, 8, 1);
INSERT INTO plinclude (pid, sid, sorder) VALUES (1, 9, 2);
INSERT INTO plinclude (pid, sid, sorder) VALUES (2, 10, 1);
INSERT INTO plinclude (pid, sid, sorder) VALUES (2, 11, 0);


-- INSERT sessions
INSERT INTO sessions (uid, sno, start, end) VALUES ('usr0', 0, '1667174400000', '1667174400000');


-- INSERT listen
INSERT INTO listen (uid, sno, sid, cnt) VALUES ('usr0', 0, 11, 2);
INSERT INTO listen (uid, sno, sid, cnt) VALUES ('usr0', 0, 9, 3);
INSERT INTO listen (uid, sno, sid, cnt) VALUES ('usr0', 0, 8, 1);




