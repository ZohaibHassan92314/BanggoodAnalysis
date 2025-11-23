create database BanggoodDB;
SELECT main_category, AVG(price) AS avg_price
FROM dbo.BanggoodProducts
GROUP BY main_category
ORDER BY avg_price DESC;


SELECT main_category, AVG(rating) AS avg_rating
FROM dbo.BanggoodProducts
GROUP BY main_category
ORDER BY avg_rating DESC;

SELECT main_category, COUNT(*) AS product_count
FROM dbo.BanggoodProducts
GROUP BY main_category
ORDER BY product_count DESC;

WITH RankedReviews AS (
    SELECT main_category, title, review_count,
           ROW_NUMBER() OVER (PARTITION BY main_category ORDER BY review_count DESC) AS rn
    FROM dbo.BanggoodProducts
)
SELECT main_category, title, review_count
FROM RankedReviews
WHERE rn <= 5
ORDER BY main_category, review_count DESC;

WITH PopularFlag AS (
    SELECT main_category,
           CASE WHEN popularity_score > (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY popularity_score) 
                                         FROM dbo.BanggoodProducts) THEN 1 ELSE 0 END AS popular_flag
    FROM dbo.BanggoodProducts
)
SELECT main_category,
       AVG(popular_flag) * 100 AS popularity_percentage
FROM PopularFlag
GROUP BY main_category
ORDER BY popularity_percentage DESC;

WITH RankedPrice AS (
    SELECT main_category, title, price,
           ROW_NUMBER() OVER (PARTITION BY main_category ORDER BY price DESC) AS rn
    FROM dbo.BanggoodProducts
)
SELECT main_category, title, price
FROM RankedPrice
WHERE rn <= 5
ORDER BY main_category, price DESC;

WITH RankedRating AS (
    SELECT main_category, title, rating,
           ROW_NUMBER() OVER (PARTITION BY main_category ORDER BY rating DESC) AS rn
    FROM dbo.BanggoodProducts
)
SELECT main_category, title, rating
FROM RankedRating
WHERE rn <= 5
ORDER BY main_category, rating DESC;