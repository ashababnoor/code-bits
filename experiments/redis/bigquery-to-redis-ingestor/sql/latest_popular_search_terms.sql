WITH base_intl_top_terms AS (
  SELECT *
  FROM `bigquery-public-data.google_trends.international_top_terms`
  QUALIFY ROW_NUMBER() 
    OVER (PARTITION BY country_code, rank ORDER BY refresh_date desc) = 1
),

current_week_data AS (
  SELECT *
  FROM base_intl_top_terms
  WHERE EXTRACT(YEAR FROM refresh_date) = EXTRACT(YEAR FROM CURRENT_DATE())
    AND EXTRACT(WEEK FROM refresh_date) = EXTRACT(WEEK FROM CURRENT_DATE())
    and rank = 1
)

SELECT
  country_code,
  week,
  term,
  -- ARRAY_AGG(
  --   STRUCT(
  --     term AS term,
  --     rank AS rank,
  --     score AS score
  --   ) 
  --   ORDER BY rank ASC
  -- ) AS popular_terms
FROM current_week_data
-- GROUP BY country_code, week
ORDER BY country_code, week DESC;
