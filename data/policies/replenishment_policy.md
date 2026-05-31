# Replenishment Policy

## Purpose

This policy defines how Itara Fresh evaluates store replenishment needs.

## Core Rules

1. Store replenishment must check warehouse inventory before supplier procurement.
2. Store demand risk must be evaluated using forecast demand, current inventory, shelf life, and inbound deliveries.
3. A high-demand store does not automatically justify a supplier purchase order.
4. Supplier procurement is a network-level decision, not a single-store reaction.
5. Routine low-risk replenishment should be handled deterministically without LLM calls.

## Required Inputs

- store ID
- SKU ID
- forecast demand
- current on-hand inventory
- available warehouse inventory
- inbound shipment schedule
- shelf life
- days of cover
- stockout risk
- spoilage risk
- overstock risk

## Approved Actions

- no action
- warehouse allocation
- warehouse-to-store delivery
- markdown review
- transfer exception review
- human escalation

## Decision Notes

The system should prefer stable, low-cost actions before expensive or exceptional actions.

Warehouse allocation should be selected when the warehouse has available inventory and the delivery window can solve the store risk in time.

Human escalation is required when required inputs are missing or when operational constraints conflict.
