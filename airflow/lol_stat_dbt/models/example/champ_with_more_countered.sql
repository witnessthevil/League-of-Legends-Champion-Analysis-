{{ config(materialized='table') }}

with source as (
    select champ, count(champ)
    from lol_counter_stat
    where win_per < 50 
    group by champ
    order by count(champ) desc 
)

select * from source 