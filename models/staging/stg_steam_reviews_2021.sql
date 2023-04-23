{{
    config(
        materialized='view'
    )
}}

with steam_reviews_without_duplicates as (
    select  
        *,
        row_number() over(partition by review_id ) as rn
    from {{ source('steam_kaggle', 'steam_reviews_data') }}
    qualify rn = 1
)
select
    * except(rn, author_last_played),
    timestamp_seconds(cast(author_last_played as int)) as author_last_played
from steam_reviews_without_duplicates