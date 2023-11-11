WITH base_intl_top_terms AS (
  SELECT *
  FROM `bigquery-public-data.google_trends.international_top_terms`
  QUALIFY ROW_NUMBER() 
    OVER (PARTITION BY country_code, rank ORDER BY refresh_date desc) = 1
)

, current_week_data AS (
  SELECT *
  FROM base_intl_top_terms
  WHERE 1 = 1
    AND rank = 1
    AND EXTRACT(YEAR FROM refresh_date) = EXTRACT(YEAR FROM CURRENT_DATE())
    AND EXTRACT(WEEK FROM refresh_date) = EXTRACT(WEEK FROM CURRENT_DATE())
)

SELECT
  country_code
  , term
FROM current_week_data
ORDER BY country_code