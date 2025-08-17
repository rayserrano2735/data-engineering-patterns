-- Filename: sql-patterns/window-functions/interview_quickref.sql
-- Window Functions Interview Quick Reference
-- Test these against your Snowflake IMDB database!

-- =====================================================
-- THE BIG THREE - MEMORIZE THIS
-- =====================================================

-- Sample data to visualize the difference
WITH scores AS (
    SELECT 'Alice' as name, 95 as score UNION ALL
    SELECT 'Bob', 92 UNION ALL
    SELECT 'Carol', 92 UNION ALL
    SELECT 'David', 90 UNION ALL
    SELECT 'Eve', 88
)
SELECT 
    name,
    score,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num,    -- 1,2,3,4,5
    RANK() OVER (ORDER BY score DESC) as rank,             -- 1,2,2,4,5 
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank  -- 1,2,2,3,4
FROM scores;

-- =====================================================
-- QUESTION 1: "Remove duplicates from a table"
-- This comes up in 70% of interviews!
-- =====================================================

-- The Pattern (memorize this structure)
WITH deduped AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY [unique_identifier]
            ORDER BY [timestamp_or_priority] DESC
        ) as rn
    FROM [table_name]
)
SELECT * FROM deduped WHERE rn = 1;

-- Real IMDB Example
WITH latest_movie_data AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY tconst  -- movie ID
            ORDER BY last_updated DESC
        ) as rn
    FROM title_basics_updates
)
SELECT * FROM latest_movie_data WHERE rn = 1;

-- =====================================================
-- QUESTION 2: "Find top N per group"
-- Second most common question!
-- =====================================================

-- Top 3 movies per genre
WITH ranked_movies AS (
    SELECT 
        primary_title,
        genres,
        average_rating,
        ROW_NUMBER() OVER (
            PARTITION BY genres 
            ORDER BY average_rating DESC
        ) as genre_rank
    FROM title_basics tb
    JOIN title_ratings tr ON tb.tconst = tr.tconst
    WHERE average_rating IS NOT NULL
)
SELECT * FROM ranked_movies WHERE genre_rank <= 3;

-- =====================================================
-- QUESTION 3: "Calculate running totals"
-- Shows you understand frame clauses
-- =====================================================

-- Running total pattern
SELECT 
    date,
    amount,
    SUM(amount) OVER (
        ORDER BY date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM daily_revenue;

-- IMDB Example: Cumulative movies released
SELECT 
    start_year,
    COUNT(*) as movies_this_year,
    SUM(COUNT(*)) OVER (
        ORDER BY start_year
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as cumulative_movies
FROM title_basics
WHERE start_year BETWEEN 2000 AND 2024
GROUP BY start_year;

-- =====================================================
-- QUESTION 4: "Moving averages"
-- Shows advanced understanding
-- =====================================================

-- 7-day moving average
SELECT 
    date,
    daily_views,
    AVG(daily_views) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7day
FROM movie_daily_stats;

-- =====================================================
-- QUESTION 5: "Find gaps in sequences"
-- The dreaded gap-and-island problem!
-- =====================================================

-- Find gaps in sequential IDs
WITH numbered AS (
    SELECT 
        id,
        id - ROW_NUMBER() OVER (ORDER BY id) as group_id
    FROM sequential_table
)
SELECT 
    MIN(id) as gap_start,
    MAX(id) as gap_end,
    COUNT(*) as gap_size
FROM numbered
GROUP BY group_id
HAVING COUNT(*) > 1;

-- =====================================================
-- ADVANCED: LAG/LEAD for comparisons
-- =====================================================

-- Compare with previous row
SELECT 
    movie_id,
    rating_date,
    rating,
    LAG(rating) OVER (PARTITION BY movie_id ORDER BY rating_date) as prev_rating,
    rating - LAG(rating) OVER (PARTITION BY movie_id ORDER BY rating_date) as rating_change,
    LEAD(rating) OVER (PARTITION BY movie_id ORDER BY rating_date) as next_rating
FROM movie_ratings;

-- =====================================================
-- THE KILLER DEMO FOR YOUR INTERVIEW
-- =====================================================

-- "Let me show you on real data..."
-- Connect to your Snowflake and run this:

WITH movie_analytics AS (
    SELECT 
        primary_title,
        start_year,
        average_rating,
        num_votes,
        -- Ranking functions
        ROW_NUMBER() OVER (PARTITION BY start_year ORDER BY average_rating DESC) as year_rank,
        DENSE_RANK() OVER (ORDER BY average_rating DESC) as overall_rank,
        PERCENT_RANK() OVER (ORDER BY num_votes DESC) as popularity_percentile,
        -- Analytics
        AVG(average_rating) OVER (PARTITION BY start_year) as year_avg_rating,
        average_rating - AVG(average_rating) OVER (PARTITION BY start_year) as rating_vs_year_avg,
        -- Running calculations
        SUM(num_votes) OVER (
            PARTITION BY start_year 
            ORDER BY average_rating DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) as cumulative_votes_in_year
    FROM title_basics tb
    JOIN title_ratings tr ON tb.tconst = tr.tconst
    WHERE start_year >= 2020
        AND num_votes > 10000  -- Only popular movies
)
SELECT * 
FROM movie_analytics
WHERE year_rank <= 5  -- Top 5 per year
ORDER BY start_year DESC, year_rank;

-- =====================================================
-- INTERVIEW TALKING POINTS
-- =====================================================

/*
When they ask about window functions, mention:

1. PERFORMANCE: "Window functions often outperform self-joins"
2. READABILITY: "Cleaner than complex subqueries"
3. FLEXIBILITY: "Can combine multiple calculations in one pass"
4. FRAME CLAUSES: Show you understand ROWS vs RANGE
5. OPTIMIZATION: "I always index PARTITION BY and ORDER BY columns"

COMMON MISTAKES TO AVOID:
- Forgetting to handle NULLs in ORDER BY
- Not understanding ROWS vs RANGE (default is RANGE)
- Using window functions when GROUP BY would be simpler
- Not considering performance on large datasets

YOUR POWER PHRASE:
"I use window functions daily. Let me show you a pattern I developed
for deduplicating 5 million records in under 30 seconds..."
[Then show this actual code on your Snowflake]
*/