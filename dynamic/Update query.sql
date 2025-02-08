select * from videostats;

alter table videostats
add column link text;

update videostats
set link = 'https://www.youtube.com/watch?v=' || ytvideoid;