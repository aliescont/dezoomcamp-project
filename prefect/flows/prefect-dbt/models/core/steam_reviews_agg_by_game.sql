{{
    config(
        materialized='table',
        partition_by={
        "field": "created_at",
        "data_type": "timestamp",
        "granularity": "month"
    }
    )
}}

with 
games_reviews as (
    select
        *
    from {{ ref('fact_games_reviews') }}
)
, games_reviews_metrics as (
    select
        game_name,
        game_genre,
        timestamp_trunc(timestamp_created, month) as created_at,
        count(distinct unique_key) as tot_reviews,
        count(distinct 
          case 
            when recommended is true
            then unique_key
          end
        ) as tot_good_recommendations,
        count(distinct 
          case 
            when recommended is false
            then unique_key
          end
        ) as tot_bad_recommendations,
        count(distinct 
          case 
            when recommended is true and game_genre in ('Free to Play')
            then unique_key
          end
        ) as tot_free_games_recommended, 
        count(distinct 
          case 
            when recommended is true and game_genre in ('Early Access')
            then unique_key
          end
        ) as tot_early_access_games_recommended, 
    from games_reviews
    group by 1,2,3
)
select
    game_name,
    game_genre,
    created_at,
    tot_reviews,
    tot_good_recommendations,
    tot_bad_recommendations,
    safe_divide(tot_good_recommendations, tot_reviews) as good_reviews_ratio,
    safe_divide(tot_bad_recommendations, tot_reviews) as bad_reviews_ratio,
    tot_free_games_recommended,
    tot_early_access_games_recommended
from games_reviews_metrics
    