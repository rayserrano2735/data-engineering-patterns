-- =====================================================
-- IMDB WINDOW FUNCTION EXERCISES
-- Practice problems using your actual database
-- =====================================================

-- EXERCISE 1: Basic ROW_NUMBER() - Deduplicate titles
-- Find the most recent version of each movie (remove duplicates)
-- TODO: Write a query that keeps only one row per TITLE_CODE, choosing the most recent ingestion
SELECT 
    -- Your code here
FROM title_basics
WHERE TITLE_TYPE = 'movie';

--- SOLUTION
WITH set_row AS 
(
SELECT
	title_code,
	ingestion_ts_utc,
	ROW_NUMBER() OVER (PARTITION BY title_code
ORDER BY
	ingestion_ts_utc DESC) AS part_row
FROM
	title_basics
WHERE
	title_type = 'movie')
SELECT
	title_code
FROM
	set_row
WHERE
	part_row = 1;


-- EXERCISE 2: RANK() vs DENSE_RANK() 
-- Rank movies by runtime within each year
-- TODO: Show the difference between RANK() and DENSE_RANK() for movies with same runtime
SELECT 
    -- Your code here
FROM title_basics
WHERE TITLE_TYPE = 'movie' 
    AND START_YEAR = 2020
    AND RUNTIME_MINUTES IS NOT NULL;

--- Solution
SELECT
	-- Your code here
	PRIMARY_TITLE ,
	start_year,
	runtime_minutes,
	RANK() OVER (PARTITION BY START_YEAR
ORDER BY
	RUNTIME_MINUTES DESC) AS rank_with_gaps,
	DENSE_RANK() OVER (PARTITION BY START_YEAR
ORDER BY
	RUNTIME_MINUTES DESC) AS dense_rank_no_gaps  
FROM
	title_basics
WHERE
	TITLE_TYPE = 'movie'
	AND START_YEAR = 2020
	AND RUNTIME_MINUTES IS NOT NULL


-- EXERCISE 3: Top N per Group
-- Find the top 3 longest movies for each genre
-- TODO: Use ROW_NUMBER() to get top 3 by runtime for each genre
WITH ranked_movies AS (
    -- Your code here
)
SELECT * FROM ranked_movies WHERE -- Your filter here;

--- SOLUTION
WITH ranked_movies AS (
    SELECT tb.GENRES, tb.RUNTIME_MINUTES, TB.PRIMARY_TITLE,
    row_number() OVER (PARTITION BY tb.genres ORDER BY tb.runtime_minutes desc) duration_rank
    FROM TITLE_BASICS tb 
    WHERE RUNTIME_MINUTES IS NOT null
)
SELECT * FROM ranked_movies WHERE duration_rank <= 3 -- Your filter here;


-- EXERCISE 4: Running Totals
-- Calculate cumulative count of movies released each year
-- TODO: Show year, movies that year, and running total of all movies up to that year
SELECT 
    START_YEAR,
    COUNT(*) as movies_this_year,
    -- Add running total here
FROM title_basics
WHERE TITLE_TYPE = 'movie' 
    AND START_YEAR BETWEEN 2015 AND 2024
GROUP BY START_YEAR
ORDER BY START_YEAR;

--- SOLUTION
WITH count_by_year as
(SELECT 
    START_YEAR,
    COUNT(*) as movies_this_year--,
    -- Add running total here
FROM title_basics
WHERE TITLE_TYPE = 'movie' 
    AND START_YEAR BETWEEN 2015 AND 2024
GROUP BY START_YEAR)
SELECT start_year, movies_this_year,
  sum(MOVIES_THIS_YEAR) OVER (ORDER BY start_year) AS running_total
FROM count_by_year 
ORDER BY START_YEAR
;



-- EXERCISE 5: Moving Average
-- Calculate 3-year moving average of movies released
-- TODO: For each year, show average of (previous year, current year, next year)
--- SOLUTION
WITH yearly_counts AS (
SELECT
	START_YEAR,
	COUNT(*) AS movie_count
FROM
	title_basics
WHERE
	TITLE_TYPE = 'movie'
	AND START_YEAR BETWEEN 2010 AND 2024
GROUP BY
	START_YEAR
)
SELECT
	START_YEAR,
	movie_count,
	avg(MOVIE_COUNT) OVER (
	ORDER BY start_year ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_3yr
FROM
	yearly_counts
ORDER BY
	START_YEAR
;


-- EXERCISE 6: LAG and LEAD
-- Show each actor's previous and next movie
-- TODO: For PERSON_CODE = 'nm0000093' (Brad Pitt), show each movie with previous and next
WITH actor_movies AS (
    SELECT 
        nb.PRIMARY_NAME,
        tb.PRIMARY_TITLE,
        tb.START_YEAR,
        tp.ORDERING
    FROM title_principals tp
    JOIN title_basics tb ON tp.TITLE_CODE = tb.TITLE_CODE
    JOIN name_basics nb ON tp.PERSON_CODE = nb.PERSON_CODE
    WHERE tp.PERSON_CODE = 'nm0000093'
        AND tb.TITLE_TYPE = 'movie'
        AND tb.START_YEAR IS NOT NULL
)
SELECT 
    PRIMARY_NAME,
    PRIMARY_TITLE,
    START_YEAR,
    -- Add LAG for previous movie
    -- Add LEAD for next movie
FROM actor_movies
ORDER BY START_YEAR, ORDERING;


-- EXERCISE 7: PERCENT_RANK()
-- Find percentile ranking of movie runtimes
-- TODO: What percentile is a 120-minute movie in?
SELECT DISTINCT
    RUNTIME_MINUTES,
    -- Add PERCENT_RANK here
FROM title_basics
WHERE TITLE_TYPE = 'movie'
    AND RUNTIME_MINUTES IS NOT NULL
ORDER BY RUNTIME_MINUTES;


-- EXERCISE 8: Multiple Window Functions
-- Complex: Rank actors by number of movies, show running total of their movies
-- TODO: For each actor, show: rank by movie count, their count, and running total
WITH actor_counts AS (
    SELECT 
        tp.PERSON_CODE,
        nb.PRIMARY_NAME,
        COUNT(DISTINCT tp.TITLE_CODE) as movie_count
    FROM title_principals tp
    JOIN title_basics tb ON tp.TITLE_CODE = tb.TITLE_CODE
    JOIN name_basics nb ON tp.PERSON_CODE = nb.PERSON_CODE
    WHERE tb.TITLE_TYPE = 'movie'
        AND tp.JOB_CATEGORY IN ('actor', 'actress')
    GROUP BY tp.PERSON_CODE, nb.PRIMARY_NAME
    HAVING COUNT(DISTINCT tp.TITLE_CODE) > 50
)
SELECT 
    PRIMARY_NAME,
    movie_count,
    -- Add DENSE_RANK by movie_count DESC
    -- Add running SUM of movie_count
FROM actor_counts
ORDER BY movie_count DESC
LIMIT 20;


-- EXERCISE 9: Gap and Island Problem
-- Find consecutive years where an actor was active
-- TODO: Identify "career breaks" for a specific actor
WITH actor_years AS (
    SELECT DISTINCT
        tp.PERSON_CODE,
        tb.START_YEAR,
        -- Add ROW_NUMBER to find gaps
    FROM title_principals tp
    JOIN title_basics tb ON tp.TITLE_CODE = tb.TITLE_CODE
    WHERE tp.PERSON_CODE = 'nm0000093'  -- Brad Pitt
        AND tb.START_YEAR IS NOT NULL
        AND tb.TITLE_TYPE = 'movie'
)
SELECT 
    PERSON_CODE,
    MIN(START_YEAR) as career_period_start,
    MAX(START_YEAR) as career_period_end,
    COUNT(*) as years_active
FROM actor_years
-- Add GROUP BY with gap detection
ORDER BY career_period_start;


-- EXERCISE 10: FIRST_VALUE and LAST_VALUE
-- Show each actor's first and most recent movie
-- TODO: In one row per actor, show first movie title and latest movie title
WITH actor_timeline AS (
    SELECT 
        tp.PERSON_CODE,
        nb.PRIMARY_NAME,
        tb.PRIMARY_TITLE,
        tb.START_YEAR
    FROM title_principals tp
    JOIN title_basics tb ON tp.TITLE_CODE = tb.TITLE_CODE
    JOIN name_basics nb ON tp.PERSON_CODE = nb.PERSON_CODE
    WHERE tp.JOB_CATEGORY IN ('actor', 'actress')
        AND tb.TITLE_TYPE = 'movie'
        AND tb.START_YEAR IS NOT NULL
        AND tp.PERSON_CODE IN ('nm0000093', 'nm0000136', 'nm0000138')  -- Sample actors
)
SELECT DISTINCT
    PERSON_CODE,
    PRIMARY_NAME,
    -- Add FIRST_VALUE for earliest movie
    -- Add LAST_VALUE for latest movie (remember frame clause!)
FROM actor_timeline
ORDER BY PRIMARY_NAME;


-- =====================================================
-- DEBUGGING EXERCISES - Fix these broken queries!
-- =====================================================

-- FIX 1: Window function in WHERE clause (WON'T WORK)
SELECT 
    PRIMARY_TITLE,
    RUNTIME_MINUTES,
    ROW_NUMBER() OVER (ORDER BY RUNTIME_MINUTES DESC) as rn
FROM title_basics
WHERE ROW_NUMBER() OVER (ORDER BY RUNTIME_MINUTES DESC) <= 10;  -- This breaks!


-- FIX 2: Wrong frame clause for running total
SELECT 
    START_YEAR,
    COUNT(*) as yearly_count,
    SUM(COUNT(*)) OVER (
        ORDER BY START_YEAR
        ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING  -- Wrong direction!
    ) as running_total
FROM title_basics
WHERE TITLE_TYPE = 'movie'
GROUP BY START_YEAR;


-- FIX 3: PARTITION BY and ORDER BY confusion
SELECT 
    PRIMARY_TITLE,
    GENRES,
    RUNTIME_MINUTES,
    RANK() OVER (PARTITION BY RUNTIME_MINUTES ORDER BY GENRES) as genre_rank  -- Backwards!
FROM title_basics
WHERE TITLE_TYPE = 'movie';


-- =====================================================
-- SOLUTIONS SECTION (Try exercises first!)
-- =====================================================

/*
SOLUTION 1: Deduplication
WITH deduped AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY TITLE_CODE 
            ORDER BY RUNTIME_MINUTES DESC NULLS LAST
        ) as rn
    FROM title_basics
    WHERE TITLE_TYPE = 'movie'
)
SELECT * FROM deduped WHERE rn = 1;

SOLUTION 2: RANK vs DENSE_RANK
SELECT 
    PRIMARY_TITLE,
    RUNTIME_MINUTES,
    RANK() OVER (ORDER BY RUNTIME_MINUTES DESC) as rank_with_gaps,
    DENSE_RANK() OVER (ORDER BY RUNTIME_MINUTES DESC) as dense_rank_no_gaps
FROM title_basics
WHERE TITLE_TYPE = 'movie' 
    AND START_YEAR = 2020
    AND RUNTIME_MINUTES IS NOT NULL
LIMIT 20;

... (more solutions available when you're stuck!)
*/