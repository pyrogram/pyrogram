create table sessions (
  dc_id integer primary key,
  test_mode integer,
  auth_key blob,
  user_id integer,
  date integer,
  is_bot integer
);

create table peers_cache (
  id integer primary key,
  hash integer,
  username text,
  phone integer
);

create table migrations (
  name text primary key
);

insert into migrations (name) values ('0001');
