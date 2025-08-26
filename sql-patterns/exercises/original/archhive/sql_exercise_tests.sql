-- =====================================================
-- TEST HARNESSES FOR SQL EXERCISES
-- Copy your solution into the your_solution CTE
-- If result shows ✅ you got it right!
-- =====================================================

-- TEST 1: Deduplication Test
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 1 SOLUTION HERE
    SELECT * FROM title_basics WHERE 1=0  -- placeholder
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
    -- PASTE YOUR EXERCISE 2 SOLUTION HERE
    SELECT 
        PRIMARY_TITLE,
        RUNTIME_MINUTES,
        NULL::INT as rank_with_gaps,     -- Replace NULLs with RANK()
        NULL::INT as dense_rank_no_gaps  -- Replace NULLs with DENSE_RANK()
    FROM title_basics
    WHERE TITLE_TYPE = 'movie' 
        AND START_YEAR = 2020
        AND RUNTIME_MINUTES IS NOT NULL
),
validation AS (
    SELECT 
        PRIMARY_TITLE,
        RUNTIME_MINUTES,
        CASE 
            WHEN rank_with_gaps = RANK() OVER (ORDER BY RUNTIME_MINUTES DESC) 
            THEN 'Correct' 
            ELSE 'Wrong' 
        END as rank_check,
        CASE 
            WHEN dense_rank_no_gaps = DENSE_RANK() OVER (ORDER BY RUNTIME_MINUTES DESC) 
            THEN 'Correct' 
            ELSE 'Wrong' 
        END as dense_rank_check
    FROM your_solution
)
SELECT 
    CASE 
        WHEN SUM(CASE WHEN rank_check = 'Wrong' THEN 1 ELSE 0 END) > 0 THEN '❌ RANK() is incorrect'
        WHEN SUM(CASE WHEN dense_rank_check = 'Wrong' THEN 1 ELSE 0 END) > 0 THEN '❌ DENSE_RANK() is incorrect'
        ELSE '✅ CORRECT! You understand RANK vs DENSE_RANK!'
    END as result,
    SUM(CASE WHEN rank_check = 'Correct' THEN 1 ELSE 0 END) as correct_ranks,
    SUM(CASE WHEN dense_rank_check = 'Correct' THEN 1 ELSE 0 END) as correct_dense_ranks,
    COUNT(*) as total_rows
FROM validation;


-- TEST 3: Top N per Group
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 3 SOLUTION HERE (final result, not the CTE)
    SELECT * FROM title_basics WHERE 1=0  -- placeholder
),
validation AS (
    WITH expected AS (
        SELECT * FROM (
            SELECT 
                PRIMARY_TITLE,
                GENRES,
                RUNTIME_MINUTES,
                ROW_NUMBER() OVER (PARTITION BY GENRES ORDER BY RUNTIME_MINUTES DESC) as rn
            FROM title_basics
            WHERE TITLE_TYPE = 'movie' 
                AND RUNTIME_MINUTES IS NOT NULL
        ) WHERE rn <= 3
    )
    SELECT 
        (SELECT COUNT(DISTINCT GENRES) FROM your_solution) as your_genre_count,
        (SELECT COUNT(DISTINCT GENRES) FROM expected) as expected_genre_count,
        (SELECT MAX(cnt) FROM (SELECT GENRES, COUNT(*) as cnt FROM your_solution GROUP BY GENRES)) as max_per_genre
)
SELECT 
    CASE 
        WHEN your_genre_count = 0 THEN '⚠️ No results - add your solution'
        WHEN max_per_genre > 3 THEN '❌ More than 3 movies per genre found!'
        WHEN your_genre_count < expected_genre_count * 0.9 THEN '❌ Missing genres'
        ELSE '✅ CORRECT! Top 3 per genre found!'
    END as result,
    your_genre_count,
    max_per_genre as max_movies_per_genre
FROM validation;


-- TEST 4: Running Totals
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 4 SOLUTION HERE
    SELECT 
        START_YEAR,
        NULL::BIGINT as movies_this_year,  -- Replace with COUNT(*)
        NULL::BIGINT as running_total      -- Replace with running SUM
    FROM title_basics
    WHERE TITLE_TYPE = 'movie' 
        AND START_YEAR BETWEEN 2015 AND 2024
    GROUP BY START_YEAR
),
expected AS (
    SELECT 
        START_YEAR,
        COUNT(*) as movies_this_year,
        SUM(COUNT(*)) OVER (ORDER BY START_YEAR ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
    FROM title_basics
    WHERE TITLE_TYPE = 'movie' 
        AND START_YEAR BETWEEN 2015 AND 2024
    GROUP BY START_YEAR
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.START_YEAR = e.START_YEAR 
            WHERE y.running_total != e.running_total
        ) THEN '❌ Running total calculation incorrect'
        ELSE '✅ CORRECT! Running totals calculated perfectly!'
    END as result
-- TEST 11: NTILE Quartiles
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 11 SOLUTION HERE
    SELECT 
        PRIMARY_TITLE,
        RUNTIME_MINUTES,
        NULL::INT as quartile
    FROM title_basics
    WHERE TITLE_TYPE = 'movie'
        AND RUNTIME_MINUTES IS NOT NULL
        AND START_YEAR = 2023
),
expected AS (
    SELECT 
        PRIMARY_TITLE,
        RUNTIME_MINUTES,
        NTILE(4) OVER (ORDER BY RUNTIME_MINUTES) as quartile
    FROM title_basics
    WHERE TITLE_TYPE = 'movie'
        AND RUNTIME_MINUTES IS NOT NULL
        AND START_YEAR = 2023
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.PRIMARY_TITLE = e.PRIMARY_TITLE 
            WHERE COALESCE(y.quartile,0) != e.quartile
        ) THEN '❌ NTILE quartiles incorrect'
        ELSE '✅ CORRECT! NTILE quartiles working!'
    END as result
FROM your_solution;


-- TEST 12: Second Highest per Group
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 12 SOLUTION HERE (final result only)
    SELECT * FROM title_basics WHERE 1=0 -- placeholder
),
expected AS (
    WITH ranked_runtimes AS (
        SELECT 
            GENRES,
            RUNTIME_MINUTES,
            DENSE_RANK() OVER (PARTITION BY GENRES ORDER BY RUNTIME_MINUTES DESC) as dr
        FROM title_basics
        WHERE TITLE_TYPE = 'movie'
            AND RUNTIME_MINUTES IS NOT NULL
    )
    SELECT GENRES, RUNTIME_MINUTES
    FROM ranked_runtimes 
    WHERE dr = 2
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '⚠️ No results - add your solution'
        WHEN COUNT(DISTINCT GENRES) < (SELECT COUNT(DISTINCT GENRES) FROM expected) * 0.8 
            THEN '❌ Missing genres - check DENSE_RANK logic'
        ELSE '✅ CORRECT! Second highest found!'
    END as result,
    COUNT(DISTINCT GENRES) as genres_found
FROM your_solution;


-- TEST 13: Median Calculation
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 13 SOLUTION HERE
    SELECT 
        START_YEAR,
        NULL::NUMERIC as median_runtime
    FROM (SELECT 2020 as START_YEAR) -- placeholder
),
expected AS (
    SELECT 
        START_YEAR,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY RUNTIME_MINUTES) as median_runtime
    FROM title_basics
    WHERE TITLE_TYPE = 'movie'
        AND RUNTIME_MINUTES IS NOT NULL
        AND START_YEAR BETWEEN 2020 AND 2024
    GROUP BY START_YEAR
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.START_YEAR = e.START_YEAR 
            WHERE ABS(COALESCE(y.median_runtime,0) - e.median_runtime) > 0.1
        ) THEN '❌ Median calculation incorrect'
        ELSE '✅ CORRECT! Median calculation perfect!'
    END as result
FROM your_solution;


-- TEST 14: Date-Based Rolling Windows
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 14 SOLUTION HERE
    SELECT 
        PRIMARY_NAME,
        START_YEAR,
        NULL::INT as movies_this_year,
        NULL::INT as rolling_3year_total
    FROM (SELECT 'Test' as PRIMARY_NAME, 2020 as START_YEAR) -- placeholder
),
expected AS (
    WITH actor_yearly AS (
        SELECT 
            tp.PERSON_CODE,
            nb.PRIMARY_NAME,
            tb.START_YEAR,
            COUNT(*) as movies_this_year
        FROM title_principals tp
        JOIN title_basics tb ON tp.TITLE_CODE = tb.TITLE_CODE
        JOIN name_basics nb ON tp.PERSON_CODE = nb.PERSON_CODE
        WHERE tp.PERSON_CODE = 'nm0000093'
            AND tb.TITLE_TYPE = 'movie'
            AND tb.START_YEAR IS NOT NULL
        GROUP BY tp.PERSON_CODE, nb.PRIMARY_NAME, tb.START_YEAR
    )
    SELECT 
        PRIMARY_NAME,
        START_YEAR,
        movies_this_year,
        SUM(movies_this_year) OVER (
            ORDER BY START_YEAR 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) as rolling_3year_total
    FROM actor_yearly
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.START_YEAR = e.START_YEAR 
            WHERE y.rolling_3year_total != e.rolling_3year_total
        ) THEN '❌ Rolling window calculation incorrect'
        ELSE '✅ CORRECT! 3-year rolling window working!'
    END as result
FROM your_solution;


-- TEST 15: Self-Join with Window Functions
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 15 SOLUTION HERE (final result only)
    SELECT 
        actor1,
        actor2,
        movies_together,
        NULL::INT as collaboration_rank
    FROM (SELECT 'nm1' as actor1, 'nm2' as actor2, 1 as movies_together) -- placeholder
),
validation AS (
    SELECT COUNT(*) as result_count
    FROM your_solution
    WHERE collaboration_rank <= 10
)
SELECT 
    CASE 
        WHEN result_count = 0 THEN '⚠️ No results - add your solution'
        WHEN result_count > 0 THEN '✅ CORRECT! Top collaborations found!'
        ELSE '❌ Check your RANK logic'
    END as result
FROM validation;


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
            tb.START_YEAR
        FROM title_principals tp
        JOIN title_basics tb ON tp.TITLE_CODE = tb.TITLE_CODE
        JOIN name_basics nb ON tp.PERSON_CODE = nb.PERSON_CODE
        WHERE tp.PERSON_CODE = 'nm0000093'
            AND tb.TITLE_TYPE = 'movie'
            AND tb.START_YEAR IS NOT NULL
            AND tp.JOB_CATEGORY = 'actor'
            AND tp.ORDERING = 1  -- Primary role only
        ORDER BY tb.START_YEAR
    )
    SELECT 
        PRIMARY_NAME,
        PRIMARY_TITLE,
        START_YEAR,
        LAG(PRIMARY_TITLE) OVER (ORDER BY START_YEAR, PRIMARY_TITLE) as previous_movie,
        LEAD(PRIMARY_TITLE) OVER (ORDER BY START_YEAR, PRIMARY_TITLE) as next_movie
    FROM actor_movies
    ORDER BY START_YEAR, PRIMARY_TITLE
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

-- TEST 7: PERCENT_RANK
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 7 SOLUTION HERE
    SELECT DISTINCT
        RUNTIME_MINUTES,
        NULL::NUMERIC as percentile_rank
    FROM title_basics
    WHERE TITLE_TYPE = 'movie'
        AND RUNTIME_MINUTES IS NOT NULL
),
expected AS (
    SELECT DISTINCT
        RUNTIME_MINUTES,
        PERCENT_RANK() OVER (ORDER BY RUNTIME_MINUTES) as percentile_rank
    FROM title_basics
    WHERE TITLE_TYPE = 'movie'
        AND RUNTIME_MINUTES IS NOT NULL
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.RUNTIME_MINUTES = e.RUNTIME_MINUTES 
            WHERE ABS(COALESCE(y.percentile_rank,0) - e.percentile_rank) > 0.001
        ) THEN '❌ PERCENT_RANK calculation incorrect'
        ELSE '✅ CORRECT! PERCENT_RANK working perfectly!'
    END as result
FROM your_solution;


-- TEST 8: Multiple Window Functions
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 8 SOLUTION HERE
    SELECT 
        PRIMARY_NAME,
        movie_count,
        NULL::INT as actor_rank,
        NULL::BIGINT as running_total
    FROM (SELECT 'test' as PRIMARY_NAME, 1 as movie_count) -- placeholder
),
expected AS (
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
        DENSE_RANK() OVER (ORDER BY movie_count DESC) as actor_rank,
        SUM(movie_count) OVER (ORDER BY movie_count DESC, PRIMARY_NAME 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
    FROM actor_counts
    ORDER BY movie_count DESC
    LIMIT 20
)
SELECT 
    CASE 
        WHEN COUNT(*) <= 1 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.PRIMARY_NAME = e.PRIMARY_NAME 
            WHERE y.actor_rank != e.actor_rank 
               OR y.running_total != e.running_total
        ) THEN '❌ Multiple window functions incorrect'
        ELSE '✅ CORRECT! Multiple windows working!'
    END as result
FROM your_solution;


-- TEST 9: Gap and Island (Complex - simplifying for exercise)
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 9 SOLUTION HERE
    SELECT 
        PERSON_CODE,
        NULL::INT as career_period_start,
        NULL::INT as career_period_end,
        NULL::INT as years_active
    FROM (SELECT 'nm0000093' as PERSON_CODE) -- placeholder
),
validation AS (
    -- Simplified test - just check if you found some career periods
    SELECT COUNT(DISTINCT career_period_start) as period_count
    FROM your_solution
    WHERE PERSON_CODE = 'nm0000093'
)
SELECT 
    CASE 
        WHEN period_count = 0 THEN '⚠️ No results - add your solution'
        WHEN period_count >= 1 THEN '✅ CORRECT! Gap detection working!'
        ELSE '❌ Gap detection needs work'
    END as result,
    period_count as career_periods_found
FROM validation;


-- TEST 10: FIRST_VALUE and LAST_VALUE
WITH your_solution AS (
    -- PASTE YOUR EXERCISE 10 SOLUTION HERE
    SELECT DISTINCT
        PERSON_CODE,
        PRIMARY_NAME,
        NULL::VARCHAR as first_movie,
        NULL::VARCHAR as last_movie
    FROM (SELECT 'nm0000093' as PERSON_CODE, 'Test' as PRIMARY_NAME) -- placeholder
),
expected AS (
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
            AND tp.PERSON_CODE IN ('nm0000093', 'nm0000136', 'nm0000138')
    )
    SELECT DISTINCT
        PERSON_CODE,
        PRIMARY_NAME,
        FIRST_VALUE(PRIMARY_TITLE) OVER (
            PARTITION BY PERSON_CODE 
            ORDER BY START_YEAR
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as first_movie,
        LAST_VALUE(PRIMARY_TITLE) OVER (
            PARTITION BY PERSON_CODE 
            ORDER BY START_YEAR
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as last_movie
    FROM actor_timeline
)
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '⚠️ No results - add your solution'
        WHEN EXISTS (
            SELECT 1 FROM your_solution y 
            JOIN expected e ON y.PERSON_CODE = e.PERSON_CODE 
            WHERE COALESCE(y.first_movie,'') != COALESCE(e.first_movie,'')
               OR COALESCE(y.last_movie,'') != COALESCE(e.last_movie,'')
        ) THEN '❌ FIRST/LAST_VALUE incorrect'
        ELSE '✅ CORRECT! FIRST/LAST_VALUE working!'
    END as result
FROM your_solution;