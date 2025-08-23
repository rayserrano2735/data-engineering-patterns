-- =====================================================
-- IMDB DATABASE SCHEMA DISCOVERY
-- Run these queries to map your database structure
-- =====================================================

-- 1. LIST ALL TABLES
-- This shows every table in your IMDB database
SHOW TABLES IN DATABASE IMDB;

-- =====================================================
-- 2. GET STRUCTURE OF KEY TABLES
-- =====================================================

-- Main movie information table
DESCRIBE TABLE IMDB.PUBLIC.TITLE_BASICS;

-- Ratings information
DESCRIBE TABLE IMDB.PUBLIC.TITLE_RATINGS;

-- Cast and crew information
DESCRIBE TABLE IMDB.PUBLIC.TITLE_PRINCIPALS;

-- People information
DESCRIBE TABLE IMDB.PUBLIC.NAME_BASICS;

-- =====================================================
-- 3. SAMPLE DATA FROM MAIN TABLES
-- =====================================================

-- Sample movies
SELECT * 
FROM IMDB.PUBLIC.TITLE_BASICS 
LIMIT 5;

-- Sample ratings
SELECT * 
FROM IMDB.PUBLIC.TITLE_RATINGS 
LIMIT 5;

-- Sample cast/crew
SELECT * 
FROM IMDB.PUBLIC.TITLE_PRINCIPALS 
LIMIT 5;

-- Sample people
SELECT * 
FROM IMDB.PUBLIC.NAME_BASICS 
LIMIT 5;

-- =====================================================
-- 4. DATA RANGES AND STATISTICS
-- =====================================================

-- Movie year ranges and counts
SELECT 
    MIN(start_year) as earliest_year,
    MAX(start_year) as latest_year,
    COUNT(*) as total_movies,
    COUNT(DISTINCT genres) as unique_genres
FROM IMDB.PUBLIC.TITLE_BASICS
WHERE title_type = 'movie'
    AND start_year IS NOT NULL;

-- Rating distribution
SELECT 
    MIN(average_rating) as min_rating,
    MAX(average_rating) as max_rating,
    AVG(average_rating) as avg_rating,
    COUNT(*) as rated_titles
FROM IMDB.PUBLIC.TITLE_RATINGS;

-- =====================================================
-- 5. CHECK FOR ADDITIONAL USEFUL TABLES
-- =====================================================

-- All tables with row counts
SELECT 
    table_name,
    row_count
FROM IMDB.INFORMATION_SCHEMA.TABLES 
WHERE table_schema = 'PUBLIC'
ORDER BY row_count DESC;

-- =====================================================
-- 6. CHECK RELATIONSHIPS
-- =====================================================

-- Check if tconst is the joining key
SELECT 
    COUNT(DISTINCT tb.tconst) as basics_count,
    COUNT(DISTINCT tr.tconst) as ratings_count,
    COUNT(DISTINCT tb.tconst) - COUNT(DISTINCT tr.tconst) as unrated_titles
FROM IMDB.PUBLIC.TITLE_BASICS tb
LEFT JOIN IMDB.PUBLIC.TITLE_RATINGS tr 
    ON tb.tconst = tr.tconst;
