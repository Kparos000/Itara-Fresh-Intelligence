# Store Transfer Exception Policy

## Purpose

This policy defines when inventory may move directly from one store to another.

## Core Rules

1. Store-to-store transfer is an exception, not a normal replenishment path.
2. Transfers should remain below 2 percent of replenishment actions.
3. Warehouse allocation must be checked before transfer approval.
4. Transfers must only occur when the source store remains safe after the transfer.
5. Transfers must only occur when the target store has a material stockout risk.
6. Transfers must respect distance and timing constraints.
7. Transfers must have positive expected financial impact.

## Required Inputs

- source store ID
- target store ID
- SKU ID
- source store forecast demand
- target store forecast demand
- source store on-hand units
- target store on-hand units
- warehouse availability
- shelf life remaining
- transfer distance
- transfer cost
- avoided stockout loss
- overnight transfer feasibility

## Approval Conditions

A transfer may be recommended only when all conditions are true:

1. Target store has high stockout risk.
2. Warehouse delivery cannot solve the risk in time.
3. Source store has low 7-day demand risk.
4. Source store remains above safety stock after transfer.
5. Shelf life remaining is sufficient.
6. Distance is within the allowed radius.
7. Transfer can occur in an approved window.
8. Expected avoided loss is greater than transfer cost.

## Rejection Conditions

Reject transfer when:

- warehouse can solve the issue in time
- source store becomes exposed to stockout risk
- source inventory is near expiry
- distance exceeds allowed radius
- transfer cost exceeds expected benefit
- required data is missing
