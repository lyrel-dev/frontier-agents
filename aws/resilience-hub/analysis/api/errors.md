---
id: "resilience-workspace-api-errors"
title: "RPC errors and recovery"
type: "api-reference"
service: "aws-resilience-hub"
status: "implemented-mock"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "api"
  - "rpc"
aliases:
  - "RPC errors and recovery"
related:
  - "index.md"
  - "protocol.md"
---



# RPC errors and recovery

The mock uses typed errors with a non-2xx HTTP status, a JSON `__type` discriminator and a `message`. HTTP responses also carry `x-amzn-ErrorType` and a per-attempt `x-amzn-RequestId`. This table is generated from [contract.cjs](contract.cjs).

| Error | HTTP | Meaning | Client response |
| --- | --- | --- | --- |
| `ValidationException` | 400 | The target, JSON body, request schema, cursor, or domain input is invalid. | Correct the request or restart pagination with no token. Do not blindly retry the same invalid body. |
| `AccessDeniedException` | 403 | The trusted server-side principal lacks a required role or workspace scope. | Use a trusted context with the required role and resource scope. Request headers do not grant access. |
| `ResourceNotFoundException` | 404 | No active entity exists in the requested parent scope. | Refresh the scoped collection and confirm the entity still exists. A child ID in another parent scope is not a match. |
| `ConflictException` | 409 | An optimistic version, idempotency token, uniqueness rule, or reference guard conflicts. | Re-read local versions or remove the blocking reference. If an idempotency token was reused with changed input, choose a new token only for a new intended command. |
| `RequestEntityTooLargeException` | 413 | The HTTP body exceeds 1 MiB. | Reduce the request body to the documented limit. |
| `UnsupportedMediaTypeException` | 415 | Content-Type must be application/x-amz-json-1.1. | Send Content-Type: application/x-amz-json-1.1. |
| `InternalServerException` | 500 | An unexpected local implementation error occurred. | Retry only after considering an uncertain outcome; retain the same clientToken for an identical mutation. |

A non-POST request is the transport exception to the table: it returns HTTP 405 with `ValidationException` and `Allow: POST`. An invalid path or unknown target returns HTTP 400. These transport checks occur before operation execution.

## Conflict handling

A stale `expectedVersion`, a changed payload using an existing idempotency token, a duplicate identity/name, an active assessment or a reference guard can produce a conflict. An identical successful replay with the same principal, operation, body and token returns the cached result before checking the now-stale version. Compare error details and current state before deciding whether to retry a changed command.

## Native adapter errors

This mock does not issue AWS calls, exhaust AWS quotas or inject AWS throttling. A production adapter must preserve or deliberately map native failures, including retryability and any provider request ID. AWS documents `ServiceQuotaExceededException` as HTTP 402 in the native Create contracts; throttling is a separate error condition. Do not normalize all quota failures to a transient 429. See [AWS mapping](aws-mapping.md) for sources and differences.

## Uncertain outcomes

A client losing its HTTP response cannot assume the command failed. Retrying the exact body with the same token avoids repeated local side effects while the in-memory idempotency result exists. A process restart loses that result. Durable command state and a remote-outcome reconciliation strategy are production requirements; the mock does not claim exactly-once execution across AWS.
