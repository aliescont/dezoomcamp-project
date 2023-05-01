{{
    config(
        materialized='view'
    )
}}

with steam_reviews_without_duplicates as (
    select  
        *,
        row_number() over(partition by appid ) as rn
    from {{ source('steam_kaggle', 'steam_games') }}
    qualify rn = 1
)
select
    * 
from steam_reviews_without_duplicates