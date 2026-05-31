# Human Escalation Policy

## Purpose

This policy defines when automated decisioning should stop and request human review.

## Core Rules

1. Escalate when required inputs are missing.
2. Escalate when policy rules conflict.
3. Escalate when expected financial impact is unusually high.
4. Escalate when supplier reliability risk is severe.
5. Escalate when an action could violate transfer, procurement, or food safety constraints.
6. Escalate when confidence is too low for an automated recommendation.

## Escalation Triggers

Escalate when any of the following occur:

- missing store inventory data
- missing warehouse inventory data
- missing forecast
- missing supplier lead time
- invalid shelf-life data
- negative or impossible inventory values
- transfer would exceed radius constraints
- supplier procurement would violate minimum order policy
- recommended action has low confidence
- expected savings calculation cannot be verified
- action affects many stores or high-value inventory

## Required Escalation Output

The system must provide:

- reason for escalation
- missing or conflicting inputs
- affected store IDs
- affected SKU IDs
- recommended human decision owner
- safe fallback action
