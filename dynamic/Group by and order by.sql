SELECT * FROM public.videostats
SELECT * FROM public.videostats

SELECT EXTRACT(YEAR from TIMESTAMP) as YEAR, count(*) as video_count
FROM videostats
GROUP BY YEAR
ORDER BY YEAR;

SELECT EXTRACT(MONTH from TIMESTAMP) as MONTH, count(*) as video_count
FROM videostats
GROUP BY MONTH
ORDER BY MONTH;

SELECT EXTRACT(DAY from TIMESTAMP) as DAY, count(*) as video_count
FROM videostats
GROUP BY DAY
ORDER BY DAY;

SELECT DATE_TRUNC('month', TIMESTAMP) as DATE, count(*) as video_count
FROM videostats
GROUP BY DATE
ORDER BY DATE;

SELECT CAST(TIMESTAMP as DATE) as DATE, count(*) as video_count
FROM videostats
GROUP BY DATE
ORDER BY DATE;

SELECT CAST(TIMESTAMP as DATE) as DATE, 
AVG(views) as AVERAGE_VIEW, 
AVG(comments) as AVERAGE_COMMENTS, 
AVG(likes) as AVERAGE_LIKES,
AVG(dislikes) as AVERAGE_DISLIKES
FROM videostats
GROUP BY DATE
ORDER BY DATE;

SELECT CAST(TIMESTAMP as DATE) as DATE,
AVG(views) as AVERAGE_VIEW, 
AVG(comments) as AVERAGE_COMMENTS, 
AVG(likes) as AVERAGE_LIKES,
AVG(dislikes) as AVERAGE_DISLIKES,
array_agg(videostatsid) AS VIDEOSTATS_IDS
FROM videostats
GROUP BY DATE
ORDER BY DATE;

SELECT CAST(TIMESTAMP as DATE) as DATE,
AVG(views) as AVERAGE_VIEW, 
AVG(comments) as AVERAGE_COMMENTS, 
AVG(likes) as AVERAGE_LIKES,
AVG(dislikes) as AVERAGE_DISLIKES,
array_to_string(array_agg(videostatsid), ',') AS VIDEOSTATS_IDS
FROM videostats
GROUP BY DATE
ORDER BY DATE;