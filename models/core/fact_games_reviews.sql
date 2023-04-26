{{
    config(
        materialized='table',
        partition_by={
        "field": "timestamp_created",
        "data_type": "timestamp",
        "granularity": "month"
    },
    cluster_by = ["recommended", "game_genre", "game_name"]
    )
}}

with 
steam_reviews as (
    select
        *
    from {{ ref('stg_steam_reviews') }}
)
, steam_games as (
    select
        *
    from {{ ref('stg_steam_games') }}
    where game_name is not null
)

select
    {{ dbt_utils.generate_surrogate_key(['r.steamid','r.appid']) }} as unique_key,
    r.steamid,
    r.appid,
    g.name as game_name,
    g.genre as game_genre,
    g.release_date as game_release_date,
    r.voted_up as recommended,
    r.votes_up,	
    r.votes_funny,
    r.weighted_vote_score,	
    r.playtime_forever,	
    r.playtime_at_review,	
    r.num_games_owned,	
    r.num_reviews,	
    r.review,	
    r.timestamp_created,	
    r.timestamp_updated	
from steam_reviews as r 
left join steam_games as g on r.appid = g.appid