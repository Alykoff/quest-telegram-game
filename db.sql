create table log (id integer, chat_id integer, user_id integer, msg text);

create table users (id integer, username text, level integer, start_level integer);

create table lvl (id integer, num integer, start_msg text, end_msg text, wrong_msg text, answer text, image blob, delay integer);

create table errors (id integer, msg text);
