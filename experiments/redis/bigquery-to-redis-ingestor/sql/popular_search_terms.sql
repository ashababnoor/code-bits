with base_intl_top_terms as (
  select *
  from `bigquery-public-data.google_trends.international_top_terms`
  qualify 
    row_number() 
  over( 
    partition by 
      country_code
      , week
      , rank
    order by 
      refresh_date
  ) = 1
)

select
  country_code
  , week
  , array_agg(
    struct(
      term as term
      , rank as rank
      , score as score
    )
    ignore nulls order by rank asc
  ) as popular_terms
from base_intl_top_terms
group by
  country_code
  , week
limit 10