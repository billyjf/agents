# Scalability record

This file is an evidence-based decision record, not a wishlist. Keep today's architecture as simple as its measured workload permits. Update this document when a feature changes load shape, data volume, dependency usage, or the operating envelope.

## Current operating envelope

| Dimension | Current evidence | Safe envelope | Confidence |
| --- | --- | --- | --- |
| Requests or events | Unknown until measured | Establish through production telemetry/load test | Low |
| Concurrent work | Unknown until measured | Establish from runtime and dependency limits | Low |
| Data volume and growth | Unknown until measured | Establish from storage/database telemetry | Low |
| External API quotas | Inventory provider limits | Stay below documented quota with headroom | Low |
| Recovery objective | Define from customer impact | Set RTO/RPO with product owner | Low |

Replace unknowns with links to dashboards, load-test results, provider quotas, or measured production values. Never turn an estimate into a claimed measurement.

## Scaling ladder

Advance one rung only when its trigger is observed or forecast with credible evidence.

| Rung | Appropriate while | Smallest useful response |
| --- | --- | --- |
| 0. Single simple service | Load is low and synchronous work fits request/runtime limits | Tune queries and indexes; bound concurrency; add timeouts, telemetry, and quotas |
| 1. Background work | Requests time out, bursty integrations need smoothing, or retries block users | Move only slow/retryable work to a managed queue; add idempotency, queue age, dead-letter handling |
| 2. Cache/read optimization | A measured read hotspot dominates latency or provider/database load | Cache the narrow hotspot with ownership, TTL, invalidation, hit-rate, and stale-data behavior |
| 3. Data-path specialization | Database contention, volume, or tenant hotspots persist after query/index work | Partition/archive or add a read model around the proven access pattern |
| 4. Service separation | Independent scaling, isolation, ownership, or deploy cadence has measurable value | Extract the smallest bounded capability with explicit contracts and observability |

## Next rung decision

- **Likely bottleneck:** Unknown until the application and its workload are inspected.
- **Leading indicators:** Tail latency, error/retry rate, concurrency, database connections/lock time, queue age, rate-limit headroom, data growth, and cost per successful operation.
- **Trigger:** Define a sustained numeric threshold tied to a user or service objective.
- **Smallest next change:** Choose from the ladder only after the trigger is met.
- **Validation:** Define the load test, canary, or production comparison that will prove improvement.
- **Rollback:** Preserve the prior path until the new rung is verified when risk warrants it.
- **Owner/review date:** Assign when this record is adopted by a project.

## Feature-level entries

Copy this block for changes that materially affect scale:

```text
Feature/date:
Load shape:
Measured baseline:
Constraint/bottleneck:
Trigger and source:
Next rung:
Migration and rollback:
Decision owner:
```
