{{ config(materialized='table') }}

with source as (
    select pick_per/ban_per bp_ratio
    from lol_basic_stat 
    order by pick_per/ban_per desc  
)

select *
from source 