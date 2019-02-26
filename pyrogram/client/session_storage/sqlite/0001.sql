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

create index username_idx on peers_cache(username);
create index phone_idx on peers_cache(phone);

insert into migrations (name) values ('0001');
