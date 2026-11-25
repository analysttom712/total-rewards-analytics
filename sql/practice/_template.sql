-- =============================================================================
-- NNN_short_name.sql   (copy this file; keep the number, rename the rest)
-- Ticket:    P2-NN  (docs/backlog/phase-2.md)
--
-- Business question (in the manager's words):
--   ...
--
-- Grain of the result: one row per ...
-- Source tables:       ...
-- As-of date (if any): ...
--
-- Expected result (fill in AFTER you run it and check it by hand):
--   Row count: ...
--   Spot-check: first row ..., last row ..., one value you verified another way
--   How I verified it: ...
-- =============================================================================

-- Style: lowercase keywords, one CTE per step, snake_case names, explicit joins.

with

step_one as (

    select
        ...
    from ...

)

select
    ...
from step_one
;
