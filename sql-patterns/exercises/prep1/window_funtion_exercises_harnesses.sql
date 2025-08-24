-- =====================================================
-- TEST HARNESSES FOR SQL EXERCISES
-- Copy your solution into the your_solution CTE
-- If result shows ✅ you got it right!
-- =====================================================

-- TEST 1: Deduplication Test
WITH your_solution AS (
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
	part_row = 1
),
expected AS (
    SELECT * FROM (
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY TITLE_CODE ORDER BY INGESTION_TS_UTC DESC) as rn
        FROM title_basics
        WHERE TITLE_TYPE = 'movie'
    ) WHERE rn = 1
),
validation AS (
    SELECT 
        (SELECT COUNT(DISTINCT TITLE_CODE) FROM your_solution) as your_unique_count,
        (SELECT COUNT(DISTINCT TITLE_CODE) FROM expected) as expected_unique_count,
        (SELECT COUNT(*) FROM your_solution) as your_total_rows,
        (SELECT COUNT(*) FROM expected) as expected_total_rows
)
SELECT 
    CASE 
        WHEN your_unique_count = 0 THEN '⚠️ No results - add your solution'
        WHEN your_unique_count != your_total_rows THEN '❌ Duplicates found! Each TITLE_CODE should appear once'
        WHEN your_unique_count != expected_unique_count THEN '❌ Wrong count - got ' || your_unique_count || ', expected ' || expected_unique_count
        ELSE '✅ CORRECT! Perfect deduplication!'
    END as result,
    your_unique_count,
    expected_unique_count
FROM validation;


-- TEST 2: RANK vs DENSE_RANK Test
WITH your_solution AS (
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

),
validation AS (
SELECT
	PRIMARY_TITLE,
	RUNTIME_MINUTES,
	CASE
		WHEN rank_with_gaps = RANK() OVER (
		ORDER BY RUNTIME_MINUTES DESC) 
            THEN 'Correct'
		ELSE 'Wrong'
	END AS rank_check,
	CASE
		WHEN dense_rank_no_gaps = DENSE_RANK() OVER (
		ORDER BY RUNTIME_MINUTES DESC) 
            THEN 'Correct'
		ELSE 'Wrong'
	END AS dense_rank_check
FROM
	your_solution
)
SELECT
	CASE
		WHEN SUM(CASE WHEN rank_check = 'Wrong' THEN 1 ELSE 0 END) > 0 THEN '❌ RANK() is incorrect'
		WHEN SUM(CASE WHEN dense_rank_check = 'Wrong' THEN 1 ELSE 0 END) > 0 THEN '❌ DENSE_RANK() is incorrect'
		ELSE '✅ CORRECT! You understand RANK vs DENSE_RANK!'
	END AS RESULT,
	SUM(CASE WHEN rank_check = 'Correct' THEN 1 ELSE 0 END) AS correct_ranks,
	SUM(CASE WHEN dense_rank_check = 'Correct' THEN 1 ELSE 0 END) AS correct_dense_ranks,
	COUNT(*) AS total_rows
FROM
	validation;


-- TEST 3: Top N per Group
WITH your_solution AS (
WITH ranked_movies AS (
SELECT
	tb.GENRES,
	tb.RUNTIME_MINUTES,
	TB.PRIMARY_TITLE,
	ROW_NUMBER() OVER (PARTITION BY tb.genres
ORDER BY
	tb.runtime_minutes DESC) duration_rank
FROM
	TITLE_BASICS tb
WHERE
	RUNTIME_MINUTES IS NOT NULL
)
SELECT
	*
FROM
	ranked_movies
WHERE
	duration_rank <= 3
),
validation AS (
    WITH expected AS (
SELECT
	*
FROM
	(
	SELECT
		PRIMARY_TITLE,
		GENRES,
		RUNTIME_MINUTES,
		ROW_NUMBER() OVER (PARTITION BY GENRES
	ORDER BY
		RUNTIME_MINUTES DESC) AS rn
	FROM
		title_basics
	WHERE
		TITLE_TYPE = 'movie'
		AND RUNTIME_MINUTES IS NOT NULL
        )
WHERE
	rn <= 3
    )
SELECT
	(
	SELECT
		COUNT(DISTINCT GENRES)
	FROM
		your_solution) AS your_genre_count,
	(
	SELECT
		COUNT(DISTINCT GENRES)
	FROM
		expected) AS expected_genre_count,
	(
	SELECT
		MAX(cnt)
	FROM
		(
		SELECT
			GENRES,
			COUNT(*) AS cnt
		FROM
			your_solution
		GROUP BY
			GENRES)) AS max_per_genre
)
SELECT
	CASE
		WHEN your_genre_count = 0 THEN '⚠️ No results - add your solution'
		WHEN max_per_genre > 3 THEN '❌ More than 3 movies per genre found!'
		WHEN your_genre_count < expected_genre_count * 0.9 THEN '❌ Missing genres'
		ELSE '✅ CORRECT! Top 3 per genre found!'
	END AS RESULT,
	your_genre_count,
	max_per_genre AS max_movies_per_genre
FROM
	validation;


-- TEST 4: Running Totals
WITH your_solution AS (
WITH count_by_year AS
(
SELECT
	START_YEAR,
	COUNT(*) AS movies_this_year
	--,
	-- Add running total here
FROM
	title_basics
WHERE
	TITLE_TYPE = 'movie'
	AND START_YEAR BETWEEN 2015 AND 2024
GROUP BY
	START_YEAR)
SELECT
	start_year,
	movies_this_year,
	sum(MOVIES_THIS_YEAR) OVER (
	ORDER BY start_year) AS running_total
FROM
	count_by_year
ORDER BY
	START_YEAR
),
expected AS (
SELECT
	START_YEAR,
	COUNT(*) AS movies_this_year,
	SUM(COUNT(*)) OVER (
	ORDER BY START_YEAR ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM
	title_basics
WHERE
	TITLE_TYPE = 'movie'
	AND START_YEAR BETWEEN 2015 AND 2024
GROUP BY
	START_YEAR
)
SELECT
	CASE
		WHEN COUNT(*) = 0 THEN '⚠️ No results - add your solution'
		WHEN EXISTS (
		SELECT
			1
		FROM
			your_solution y
		JOIN expected e ON
			y.START_YEAR = e.START_YEAR
		WHERE
			y.running_total != e.running_total
        ) THEN '❌ Running total calculation incorrect'
		ELSE '✅ CORRECT! Running totals calculated perfectly!'
	END AS RESULT
FROM
	your_solution;


-- TEST 5: Moving Average
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 5 SOLUTION HERE (with moving average)
    SELECT 
        START_YEAR,
        NULL::INT as movie_count,
        NULL::NUMERIC as moving_avg_3yr
    FROM (SELECT 1 as START_YEAR) -- placeholder
),
expected AS (
    WITH yearly_counts AS (
        SELECT 
            START_YEAR,
            COUNT(*) as movie_count
        FROM title_basics
        WHERE TITLE_TYPE = 'movie'
            AND START_YEAR BETWEEN 2010 AND 2024
        GROUP BY START_YEAR
    )
    SELECT 
        START_YEAR,
        movie_count,
        AVG(movie_count) OVER (
            ORDER BY START_YEAR 
            ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
        ) as moving_avg_3yr
    FROM yearly_counts
)
SELECT 
    CASE 
        WHEN COUNT(*) <= 1 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.START_YEAR = e.START_YEAR 
            WHERE ABS(y.moving_avg_3yr - e.moving_avg_3yr) > 0.01
        ) THEN '❌ Moving average calculation incorrect'
        ELSE '✅ CORRECT! 3-year moving average perfect!'
    END as result
FROM your_solution;


-- TEST 6: LAG and LEAD
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 6 SOLUTION HERE
    SELECT 
        PRIMARY_NAME,
        PRIMARY_TITLE,
        START_YEAR,
        NULL::VARCHAR as previous_movie,
        NULL::VARCHAR as next_movie
    FROM (SELECT 1) -- placeholder
),
expected AS (
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
        LAG(PRIMARY_TITLE) OVER (ORDER BY START_YEAR, ORDERING) as previous_movie,
        LEAD(PRIMARY_TITLE) OVER (ORDER BY START_YEAR, ORDERING) as next_movie
    FROM actor_movies
)
SELECT 
    CASE 
        WHEN COUNT(*) <= 1 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.PRIMARY_TITLE = e.PRIMARY_TITLE 
            WHERE COALESCE(y.previous_movie,'') != COALESCE(e.previous_movie,'')
               OR COALESCE(y.next_movie,'') != COALESCE(e.next_movie,'')
        ) THEN '❌ LAG/LEAD values incorrect'
        ELSE '✅ CORRECT! LAG and LEAD working perfectly!'
    END as result
FROM your_solution;


-- More tests for exercises 7-10 available when needed!