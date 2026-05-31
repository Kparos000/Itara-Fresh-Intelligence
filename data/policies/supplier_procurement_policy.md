# Supplier Procurement Policy

## Purpose

This policy defines how Itara Fresh evaluates supplier purchase orders.

## Core Rules

1. Supplier procurement is a warehouse-level or network-level decision.
2. Stores do not order directly from suppliers by default.
3. Supplier orders should only be considered after warehouse inventory and inbound shipments are checked.
4. Supplier orders should account for lead time, minimum order value, delivery days, reliability, and spoilage risk.
5. Emergency supplier delivery should be rare and financially justified.

## Required Inputs

- SKU ID
- category
- supplier ID
- warehouse on-hand inventory
- warehouse available inventory
- network forecast demand
- inbound supplier shipments
- supplier lead time
- supplier delivery days
- supplier reliability
- minimum order value
- emergency delivery allowed
- emergency delivery fee
- expected spoilage impact
- expected stockout impact

## Approved Actions

- no supplier order
- standard supplier purchase order
- emergency supplier purchase order review
- human escalation

## Decision Notes

Supplier procurement should not be triggered by a single store demand spike unless the spike reflects broader network need or cannot be solved through warehouse allocation.

Emergency supplier delivery requires stronger justification than standard procurement because it increases operating cost.
