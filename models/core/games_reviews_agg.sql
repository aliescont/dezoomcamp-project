{{
    config(
        materialized ='table',
        partition_by = {
            "field": "created_at",
            "data_type": "timestamp",
            "granularity": "day"
        },
        cluster_by = ['app_name']
    )
}}

with 
reviews as (
    select * from {{ ref('stg_steam_reviews') }}
)
, games_agg as (
    select
        app_id,
        app_name,
        timestamp_trunc(timestamp_created, day) as created_at,
        count(distinct review_id) as tot_reviews,
        count(distinct 
          case 
            when recommended is true
            then review_id
          end
        ) as tot_good_recommendations,
        count(distinct
          case 
            when recommended is false
            then review_id
          end
        ) as tot_bad_recommendations,
        count(distinct
          case
            when recommended is true and steam_purchase is true
            then review_id
          end
        ) as tot_games_recommended_and_purchase,
        count(distinct
          case
            when recommended is true and received_for_free is true
            then review_id
          end
        ) as tot_free_games_recommended,
        count(distinct
          case
            when recommended is true and written_during_early_access is true
            then review_id
          end
        ) as tot_good_recommendations_newbies,
        avg(votes_helpful) as avg_votes_helpful,
        avg(votes_funny)  as avg_votes_funny,
    from reviews
    group by 1,2,3
)

select 
    app_id,
    app_name,
    created_at,
    tot_reviews,
    tot_good_recommendations,
    tot_bad_recommendations,
    safe_divide(tot_good_recommendations,tot_reviews) as recommendation_ratio,
    tot_games_recommended_and_purchase,
    safe_divide(tot_games_recommended_and_purchase, tot_good_recommendations) as games_recommended_and_purchase_ratio,
    tot_free_games_recommended,
    safe_divide(tot_free_games_recommended, tot_good_recommendations) as free_games_recommended_ratio,

from games_agg as g 
