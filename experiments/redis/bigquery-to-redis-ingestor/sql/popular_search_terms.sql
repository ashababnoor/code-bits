WITH base_intl_top_terms AS (
  SELECT *
  FROM `bigquery-public-data.google_trends.international_top_terms`
  QUALIFY 
    row_number() 
  over( 
    PARTITION BY 
      country_code
      , week
      , rank
    ORDER BY 
      refresh_date
  ) = 1
)

SELECT
  country_code
  , week
  , array_agg(
    STRUCT(
      term AS term
      , rank AS rank
      , score AS score
    )
    IGNORE NULLS ORDER BY rank ASC
  ) AS popular_terms
FROM base_intl_top_terms
GROUP BY
  country_code
  , week
ORDER BY country_code, week desc