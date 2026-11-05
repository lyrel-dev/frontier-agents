#!/usr/bin/env python3
"""Build the phase-one RPC specification. This is not a server or AWS adapter.

The model and its connected synthetic examples are independent source files.
This generator owns only files in api/: operations.json, rpc.schema.json,
examples.json and OPERATIONS.md. It does not execute any operation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODEL = json.loads((ROOT / "model/schema.json").read_text())
MODEL_ID = MODEL["$id"]
SCHEMA_ID = "https://schemas.frontier-agents.example/consolidated-operations-console/2026-11-05/rpc.json"
NAMESPACE = "ConsolidatedOperationsConsole_20261105"
NOW = 1793872800
DEFS: dict = {}
OPS: list[dict] = []
SAMPLES: dict = {}
RECORDS: dict = {}


def obj(properties, required=None, **extra):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False, **extra}


def string(lo=1, hi=4096, **extra):
    return {"type": "string", "minLength": lo, "maxLength": hi, **extra}


def enum(*values):
    return {"type": "string", "enum": list(values)}


def array(items, minimum=0, maximum=100, unique=False):
    out = {"type": "array", "items": items, "minItems": minimum, "maxItems": maximum}
    if unique:
        out["uniqueItems"] = True
    return out


def integer(minimum=0, maximum=9007199254740991):
    return {"type": "integer", "minimum": minimum, "maximum": maximum}


def local(name):
    return {"$ref": f"#/$defs/{name}"}


def model(name):
    return {"$ref": f"{MODEL_ID}#/$defs/{name}"}


def nullable(shape):
    return {"anyOf": [shape, {"type": "null"}]}


def lower(name):
    return name[0].lower() + name[1:]


def idfield(name):
    return lower(name) + "Id"


def identifier(name):
    rows = RECORDS.get(name, [])
    return rows[0][idfield(name)] if rows else lower(name) + "-demo"


def record(name, **selector):
    rows = RECORDS.get(name, [])
    if selector:
        rows = [x for x in rows if all(x.get(k) == v for k, v in selector.items())]
    if not rows:
        raise ValueError(f"Missing canonical synthetic example for {name} {selector}")
    return copy.deepcopy(rows[0])


def source_revision_for(entity):
    row = record(entity)
    for key in ("selectedSourceRevisionId", "sourceRevisionId"):
        if row.get(key):
            return row[key]
    for key in ("selectedDetailObservationId", "selectedObservationId", "selectedTaskObservationId", "selectedSummaryObservationId"):
        if row.get(key):
            return record("Observation", observationId=row[key])["sourceRevisionId"]
    if row.get("providerBindings"):
        return row["providerBindings"][0]["sourceRevisionId"]
    raise ValueError(f"No source precondition can be resolved for {entity}")


def eref(name):
    return {"kind": name, "id": identifier(name)}


def digest(value):
    # This is explicitly the local design-example digest, not provider identity.
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def model_shape(value):
    if isinstance(value, list):
        return [model_shape(v) for v in value]
    if isinstance(value, dict):
        return {k: (MODEL_ID + v if k == "$ref" and isinstance(v, str) and v.startswith("#/") else model_shape(v))
                for k, v in value.items()}
    return value


def properties_of(name, fields):
    return {key: model_shape(MODEL["$defs"][name]["properties"][key]) for key in fields}


ID = model("Id")
VERSION = model("Version")
TIME = model("Timestamp")
TOKEN = string(16, 128, pattern="^[A-Za-z0-9._~-]+$")
BOOL = {"type": "boolean"}
TEXT = string(0, 16384)
PAGE = {"maxResults": integer(1, 100), "nextToken": string(1, 4096)}
MUT = {"clientToken": TOKEN}
GUARDED = {**MUT, "expectedVersion": VERSION}

DEFS["Page"] = obj({
    "traversalId": ID, "asOfSequence": integer(0), "createdAt": TIME, "expiresAt": TIME,
}, ["traversalId", "asOfSequence", "createdAt", "expiresAt"])
DEFS["FieldViolation"] = obj({"path": string(1, 1024), "code": string(1, 128), "message": string(1, 2048)})
ERRORS = {
    "ValidationException": (400, False, "Invalid syntax, field, union, scalar or semantic input; no accepted mutation."),
    "UnauthenticatedException": (401, False, "No verified caller identity."),
    "AccessDeniedException": (403, False, "Caller or connection lacks permission for the complete subject/evidence scope."),
    "ResourceNotFoundException": (404, False, "Identity is absent or invisible in its trusted workspace and required parent scope."),
    "VersionConflictException": (409, False, "The named local mutable record no longer has expectedVersion."),
    "IdempotencyConflictException": (409, False, "The same operation/clientToken was used with different intent or precondition."),
    "CommandInProgressException": (409, True, "A matching durable token reservation is in flight; reconcile the returned command and retry the exact request."),
    "InvalidStateException": (409, False, "State, scope, binding, source precondition or cross-record invariant prevents this command."),
    "PaginationTokenExpiredException": (410, False, "The traversal snapshot expired; explicitly begin a new traversal."),
    "EvidenceUnavailableException": (410, False, "Retained content is expired, redacted or unavailable; its identity and known history remain."),
    "RequestTooLargeException": (413, False, "The request exceeds the declared byte or collection bound."),
    "UnsupportedMediaTypeException": (415, False, "The request is not application/x-amz-json-1.1."),
    "ThrottlingException": (429, True, "Admission capacity is limited; honor retryAfterSeconds and keep the original token."),
    "InternalServerException": (500, True, "An internal failure prevented a complete response; outcome requires receipt reconciliation."),
    "ServiceUnavailableException": (503, True, "Temporarily unavailable; retry the exact intent only within the recorded replay contract."),
}
DEFS["RpcError"] = obj({
    "__type": enum(*ERRORS), "code": string(1, 128), "message": string(1, 4096),
    "requestId": ID, "retryable": BOOL,
    "fieldViolations": array(local("FieldViolation"), maximum=100),
    "commandId": ID, "retryAfterSeconds": integer(1, 300),
}, ["__type", "code", "message", "requestId", "retryable"])


def add(name, module, kind, permission, entities, request, response, sample,
        semantics, native=(), phase=None, response_selector=None):
    mutating = kind != "READ"
    if mutating and "clientToken" not in request.get("required", []):
        raise ValueError(f"Mutation without required clientToken: {name}")
    if "clearFields" in request["properties"]:
        for field in request["properties"]["clearFields"]["items"]["enum"]:
            assigned = "assigneeSubjectId" if field == "owner" else field
            if assigned in request["properties"]:
                request.setdefault("allOf", []).append({
                    "if": {"required": ["clearFields"], "properties": {"clearFields": {"contains": {"const": field}}}},
                    "then": {"not": {"required": [assigned]}},
                })
    DEFS[name + "Request"] = request
    DEFS[name + "Response"] = response
    error_names = ["ValidationException", "UnauthenticatedException", "AccessDeniedException", "ResourceNotFoundException",
                   "ThrottlingException", "InternalServerException", "ServiceUnavailableException"]
    if name.startswith("List"):
        error_names.append("PaginationTokenExpiredException")
    if mutating:
        error_names += ["IdempotencyConflictException", "CommandInProgressException", "InvalidStateException"]
    if any(key.startswith("expected") and key.endswith("Version") for key in request["properties"]):
        error_names.append("VersionConflictException")
    if any(x in entities for x in ("SourceRevision", "Snapshot", "Observation", "Asset")):
        error_names.append("EvidenceUnavailableException")
    OPS.append({
        "name": name, "module": module, "kind": kind, "permission": permission,
        "entities": entities, "mutating": mutating, "maturity": "CONTRACT_ONLY",
        "deliveryPhase": phase or ("P2_READ_AND_INGEST" if kind in ("READ", "INGEST", "DERIVE") else
                                    "P4_WORKFLOW_RUNTIME" if module == "workflow" and kind == "EXECUTION_COMMAND" else
                                    "P3_DURABLE_COMMANDS"),
        "target": NAMESPACE + "." + name,
        "inputSchemaRef": "rpc.schema.json#/$defs/" + name + "Request",
        "outputSchemaRef": "rpc.schema.json#/$defs/" + name + "Response",
        "nativeOperations": list(native), "errors": error_names,
        "semantics": semantics,
        "scopeFields": [k for k in request["properties"] if k.endswith("Id") and k not in ("clientToken",)],
    })
    SAMPLES[name] = {"request": sample, "responseSelector": response_selector or {}}


def get(name, entity, module, parents=(), permission="console:Read", semantics=()):
    fields = {idfield(x): ID for x in (*parents, entity)}
    add(name, module, "READ", permission, [entity], obj(fields), obj({lower(entity): model(entity)}),
        lambda: {idfield(x): identifier(x) for x in (*parents, entity)},
        ["Returns retained canonical data with its provenance; does not fetch AWS synchronously.",
         "Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.", *semantics])


def listing(name, entity, module, parents=(), filters=None, permission="console:Read", semantics=(), sample_filters=None):
    fields = {idfield(x): ID for x in parents}
    fields.update(filters or {})
    fields.update(PAGE)
    add(name, module, "READ", permission, [entity], obj(fields, [idfield(x) for x in parents]),
        obj({"items": array(model(entity), maximum=100), "page": local("Page"), "nextToken": string(1, 4096)}, ["items", "page"]),
        lambda: {**{idfield(x): identifier(x) for x in parents}, **(sample_filters or {}), "maxResults": 20},
        ["Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.",
         "A completed local traversal does not establish complete upstream collection or claim coverage.", *semantics])


def command_response(entity=None):
    fields = {"command": model("Command")}
    if entity:
        fields[lower(entity)] = model(entity)
    return obj(fields)


def clear_fields(*names):
    return array(enum(*names), 1, len(names), True)


def at_least_change(fields):
    return [{"required": [name]} for name in fields]


def add_foundation():
    add("GetWorkspace", "foundation", "READ", "console:ReadWorkspace", ["Workspace"], obj({}),
        obj({"workspace": model("Workspace")}), lambda: {},
        ["Workspace comes exclusively from authenticated context; the request cannot select a tenant."])
    get("GetConnection", "Connection", "foundation", permission="console:ReadConnections")
    listing("ListConnections", "Connection", "foundation", permission="console:ReadConnections", filters={"enabled": BOOL})
    create = {"name": string(1, 256), "provider": enum("aws"), "credentialBindingId": ID,
              "allowedScopes": array(model("OwningScope"), 1, 100), **MUT}
    add("CreateConnection", "foundation", "LOCAL_COMMAND", "console:ManageConnections", ["Connection", "Command"],
        obj(create), command_response("Connection"),
        lambda: {"name": "AWS operations reader", "provider": "aws", "credentialBindingId": "credref-approved-reader",
                 "allowedScopes": record("Connection")["allowedScopes"], "clientToken": "create-connection-demo-0001"},
        ["Binds an already registered secret/identity reference after authorization; accepts no credential bytes.",
         "Requested scopes are checked against the caller's grant and the binding's capabilities; references do not grant access."])
    fields = {"connectionId": ID, "name": string(1, 256), "credentialBindingId": ID,
              "allowedScopes": array(model("OwningScope"), 1, 100), "enabled": BOOL, **GUARDED}
    add("UpdateConnection", "foundation", "LOCAL_COMMAND", "console:ManageConnections", ["Connection", "Command"],
        obj(fields, ["connectionId", "expectedVersion", "clientToken"],
            anyOf=at_least_change(["name", "credentialBindingId", "allowedScopes", "enabled"])),
        command_response("Connection"),
        lambda: {"connectionId": identifier("Connection"), "expectedVersion": record("Connection")["version"],
                 "enabled": False, "clientToken": "disable-connection-demo-0001"},
        ["Changes local connection configuration only; existing observations retain their original authorization provenance.",
         "Revocation is checked on every later read, replay and dispatch; disabling a connection does not erase historical evidence."])
    get("GetResource", "Resource", "foundation")
    listing("ListResources", "Resource", "foundation", filters={"serviceId": ID, "resourceType": string(1, 128)})
    get("GetCollection", "Collection", "foundation")
    listing("ListCollections", "Collection", "foundation", filters={"connectionId": ID, "subject": model("EntityRef")})
    listing("ListReadAttempts", "ReadAttempt", "foundation", parents=("Collection",),
            semantics=["Includes failed and empty reads; their absence from returned object rows must not erase collection evidence."])
    for entity in ("SourceRevision", "Observation", "ProjectionRevision", "Snapshot", "WorkItem", "Command"):
        get("Get" + entity, entity, "foundation")
    listing("ListSourceRevisions", "SourceRevision", "foundation", filters={
        "identity": model("SourceIdentity"), "profile": string(1, 256), "representation": MODEL["$defs"]["SourceRevision"]["properties"]["representation"]},
        semantics=["Native peripheral resources are retained typed profiles, including FIS templates/catalogs and DevOps registrations/triggers/goals.",
                   "Representation and source identity are explicit; matching hashes do not merge different logical source records."])
    listing("ListObservations", "Observation", "foundation", filters={"sourceRevisionId": ID, "collectionId": ID, "subject": model("EntityRef")})
    listing("ListProjectionRevisions", "ProjectionRevision", "foundation", filters={
        "subject": model("EntityRef"), "profile": MODEL["$defs"]["ProjectionRevision"]["properties"]["profile"]},
        semantics=["Returns immutable derivations. Current selection is a view; re-evaluation creates another revision and never rewrites a sealed Run."])
    listing("ListSnapshots", "Snapshot", "foundation", filters={"subject": model("EntityRef"), "kind": MODEL["$defs"]["Snapshot"]["properties"]["kind"]})
    listing("ListWorkItems", "WorkItem", "foundation", filters={"target": model("EntityRef"), "state": MODEL["$defs"]["WorkItem"]["properties"]["state"]})
    listing("ListCommands", "Command", "foundation", filters={"subject": model("EntityRef"), "operation": string(1, 128), "state": MODEL["$defs"]["Command"]["properties"]["state"]})

    # Collectors may invoke registered read contracts, never arbitrary URLs, code or cloud mutations.
    fields = {"connectionId": ID, "queries": array(model("CollectionQuery"), 1, 100), **MUT}
    add("StartCollection", "foundation", "INGEST", "console:Collect", ["Collection", "Command"],
        obj(fields), command_response("Collection"),
        lambda: {"connectionId": identifier("Connection"), "queries": record("Collection")["queries"],
                 "clientToken": "start-collection-demo-0001"},
        ["Admits a finite exact query set from the registered read-only adapter catalog; unknown operations or unauthorized scope fail admission.",
         "queryKey uniqueness, canonical requestDigest, filter types and operation-specific bounds are validated against that registered adapter.",
         "Completion, pagination, hydration, resolution and claim coverage remain independent facts."])
    attempt_fields = properties_of("ReadAttempt", ["collectionId", "readAttemptId", "state", "endedAt", "providerRequestId", "returnedCount", "nextTokenPresent", "error", "requestSourceRevisionId", "responseSourceRevisionId"])
    attempt_fields["state"] = enum("SUCCEEDED", "FAILED")
    attempt_fields["endedAt"] = TIME
    attempt_fields.update(MUT)
    add("RecordReadAttempt", "foundation", "INGEST", "console:IngestEvidence", ["ReadAttempt", "Command"],
        obj(attempt_fields, allOf=[
            {"if": {"properties": {"state": {"const": "SUCCEEDED"}}}, "then": {"properties": {"error": {"type": "null"}}}},
            {"if": {"properties": {"state": {"const": "FAILED"}}}, "then": {"properties": {"error": model("ReadError")}}},
        ]), command_response("ReadAttempt"),
        lambda: {**{k: record("ReadAttempt")[k] for k in attempt_fields if k != "clientToken"},
                 "clientToken": "record-read-attempt-demo-0001"},
        ["Settles the same existing STARTED ReadAttempt created by the trusted collector dispatch transaction before the actual read; does not append a second attempt or fabricate a pre-call record after the fact.",
         "Trusted context assigns authorizationContextKey; a caller cannot forge its acting principal or provenance.",
         "The requestSourceRevisionId must equal the already retained normalized request envelope for this attempt. Response envelope references must belong to this exact request and scope, including empty responses.",
         "IngestObservation may retain response/object observations while the attempt is STARTED; settlement then references those revisions. A response-lost failure has an explicit null response reference, not a fabricated empty response.",
         "A settled attempt is immutable. Exact replay returns the original result; conflicting terminal facts reject. Query identity, attemptNo, requestDigest, startedAt and authorization provenance are server-owned."])
    source_fields = properties_of("SourceRevision", ["identity", "representation", "profile", "profileVersion", "sourceOperation", "contentDigest", "digestProfile", "providerUpdatedAt", "providerVersion", "fieldPresence", "payloadStorage", "payload", "artifact"])
    DEFS["SourceRevisionInput"] = obj(source_fields, allOf=model_shape(MODEL["$defs"]["SourceRevision"].get("allOf", [])))
    observation_fields = properties_of("Observation", ["channel", "readAttemptId", "connectionId", "observedAt", "sourceTime", "transportTime", "expiresAt", "receiptKey"])
    observation_fields.update({"source": local("SourceRevisionInput"), **MUT})
    add("IngestObservation", "foundation", "INGEST", "console:IngestEvidence", ["SourceRevision", "Observation", "Command"],
        obj(observation_fields, allOf=model_shape(MODEL["$defs"]["Observation"].get("allOf", []))), obj({"sourceRevision": model("SourceRevision"), "observation": model("Observation"), "command": model("Command")}),
        lambda: {**{k: record("Observation")[k] for k in observation_fields if k not in ("source", "clientToken")},
                 "source": {k: record("SourceRevision", sourceRevisionId=record("Observation")["sourceRevisionId"])[k] for k in source_fields}, "clientToken": "ingest-observation-demo-0001"},
        ["Atomically retains or resolves the immutable source revision and appends this distinct receipt observation.",
         "The registered versioned profile validates typed known members, source identity, representation and digest; raw unknown provider output remains retained evidence.",
         "payload is the intentionally opaque provider document, bounded by the body cap and adapter schema; it cannot patch canonical state or set a verdict.",
         "The adapter reconciles canonical entity indexes through verified mappings. Digest equality alone is not event identity; receipt dedupe includes the authenticated channel/scope."])
    add("CompleteCollection", "foundation", "INGEST", "console:IngestEvidence", ["Collection", "Command"],
        obj({"collectionId": ID, "expectedProjectionVersion": VERSION, "coverage": array(model("Coverage"), 1, 100), **MUT}),
        command_response("Collection"),
        lambda: {"collectionId": identifier("Collection"), "expectedProjectionVersion": record("Collection")["projectionVersion"],
                 "coverage": record("Collection")["coverage"], "clientToken": "complete-collection-demo-0001"},
        ["Seals collection coverage after every declared query has a settled or explicitly unresolved outcome; referenced attempts must belong to this collection.",
         "A coverage conclusion must be justified by registered collector rules. Successful or exhausted pages cannot alone claim source sufficiency.",
         "expectedProjectionVersion fences this collector completion only; it is not a configuration edit version or AWS conditional write."])
    projection_input = properties_of("ProjectionRevision", ["projectionKey", "profile", "profileVersion", "subjectRefs", "inputRefs", "ruleDigest", "asOf"])
    projection_input.update(MUT)
    add("PublishProjection", "foundation", "DERIVE", "console:PublishProjection", ["ProjectionRevision", "Command"],
        obj(projection_input), command_response("ProjectionRevision"),
        lambda: {**{k: record("ProjectionRevision", profile="SERVICE_STATUS")[k] for k in projection_input if k != "clientToken"},
                 "clientToken": "publish-projection-demo-0001"},
        ["Executes an authorized registered immutable rule over the exact immutable inputs and appends a derived revision.",
         "The request cannot supply value, generatedAt, coverage or a desired verdict. The trusted projector derives them from the selected evidence.",
         "Every reference must be authorized, same-workspace and available. Missing evidence produces a qualified result or explicit failure; it never becomes success.",
         "Current projections and historical evaluations do not consume a local configuration version or modify prior revisions."],
        response_selector={"ProjectionRevision": {"profile": "SERVICE_STATUS"}})
    capture_input = {"kind": MODEL["$defs"]["Snapshot"]["properties"]["kind"], "subjectRefs": array(model("EntityRef"), 1, 100),
                     "sourceRevisionIds": array(ID, maximum=1000, unique=True), "observationIds": array(ID, maximum=1000, unique=True),
                     "projectionRevisionIds": array(ID, maximum=1000, unique=True), "collectionIds": array(ID, maximum=100, unique=True), **MUT}
    # Run admission is an internal atomic StartRun effect, not a user-editable snapshot.
    capture_input["kind"] = enum("INVESTIGATION", "TOPOLOGY", "POLICY_CONTEXT", "LIFECYCLE_CATALOG", "EVALUATION_INPUT")
    add("CaptureSnapshot", "foundation", "LOCAL_COMMAND", "console:CaptureEvidence", ["Snapshot", "Command"],
        obj(capture_input), command_response("Snapshot"),
        lambda: {"kind": "TOPOLOGY", **{k: record("Snapshot", kind="TOPOLOGY")[k] for k in ("subjectRefs", "sourceRevisionIds", "observationIds", "projectionRevisionIds")},
                 "collectionIds": sorted({r["collectionId"] for r in record("Snapshot", kind="TOPOLOGY")["readAttempts"]}), "clientToken": "capture-snapshot-demo-0001"},
        ["Builds a closed immutable manifest and typed contents from existing retained evidence, including failed/empty read attempts and coverage.",
         "The manifest does not consult mutable current fields after capture. capturedAt does not renew source timestamps or make paginated AWS reads atomic.",
         "RUN_INPUT snapshots are created only during StartRun admission; clients cannot replace a Run's inputs by creating a similarly named snapshot."],
        response_selector={"Snapshot": {"kind": "TOPOLOGY"}})

    add("CreateWorkItem", "foundation", "LOCAL_COMMAND", "console:ManageWork", ["WorkItem", "Command"],
        obj({"title": string(1, 256), "targets": array(model("EntityRef"), 1, 100), "priority": enum("CRITICAL", "HIGH", "MEDIUM", "LOW"), "dueAt": TIME, "assigneeSubjectId": ID, **MUT}, ["title", "targets", "clientToken"]), command_response("WorkItem"),
        lambda: {"title": "Review checkout resilience evidence", "targets": [eref("Service"), eref("Finding")], "clientToken": "create-work-item-demo-0001"},
        ["Creates local operator work; no provider state or operational conclusion is implied.",
         "assigneeSubjectId resolves through the trusted workspace directory and assignment policy; it selects a work owner, never the acting principal."])
    fields = {"workItemId": ID, "title": string(1, 256), "state": MODEL["$defs"]["WorkItem"]["properties"]["state"],
              "priority": enum("CRITICAL", "HIGH", "MEDIUM", "LOW"), "dueAt": TIME, "assigneeSubjectId": ID,
              "snoozedUntil": TIME, "resolutionEvidence": array(model("EvidenceRef"), maximum=100, unique=True),
              "note": TEXT, "clearFields": clear_fields("snoozedUntil", "dueAt", "owner"), **GUARDED}
    add("UpdateWorkItem", "foundation", "LOCAL_COMMAND", "console:ManageWork", ["WorkItem", "Command"],
        obj(fields, ["workItemId", "expectedVersion", "clientToken"],
            anyOf=at_least_change(["title", "state", "priority", "dueAt", "assigneeSubjectId", "snoozedUntil", "resolutionEvidence", "note", "clearFields"])),
        command_response("WorkItem"),
        lambda: {"workItemId": identifier("WorkItem"), "expectedVersion": record("WorkItem")["version"],
                 "state": "ACKNOWLEDGED", "note": "Reviewing the captured evidence.", "clientToken": "update-work-item-demo-0001"},
        ["Records a server-attributed WorkAction and advances only WorkItem.version.",
         "RESOLVED is an operator work state, not provider recovery, approved cloud work or verified remediation.",
         "A field cannot be both assigned and named in clearFields; assigneeSubjectId conflicts with clearing owner. Evidence citations retain their original meaning.",
         "The trusted directory resolves the assigned owner independently of the server-attributed acting principal. Verification uses its separate command."])
    add("RecordWorkItemVerification", "foundation", "LOCAL_COMMAND", "console:VerifyWork", ["WorkItem", "Command"],
        obj({"workItemId": ID, "result": enum("VERIFIED", "FAILED", "UNKNOWN"), "rationale": string(1, 4096),
             "evidenceRefs": array(model("EvidenceRef"), 1, 100, True), **GUARDED}), command_response("WorkItem"),
        lambda: {"workItemId": identifier("WorkItem"), "expectedVersion": record("WorkItem")["version"], "result": "UNKNOWN",
                 "rationale": "The review is complete, but retained provider findings do not establish remediation.",
                 "evidenceRefs": record("WorkItem")["resolutionEvidence"], "clientToken": "verify-work-item-demo-0001"},
        ["Records a separately authorized, qualified local verification judgment and an immutable server-attributed action under the WorkItem version.",
         "All evidence must resolve to this work's target scope. VERIFIED requires independent supporting evidence under the registered verification policy; the same operator resolution action or assessment completion alone is insufficient.",
         "The result updates verificationState/verificationEvidence, not WorkItem.state or any provider status, posture or historical source record."])


def add_workload():
    DEFS["MembershipInput"] = obj({"systemId": ID, "userJourneyIds": array(ID, maximum=100, unique=True)})
    for entity in ("System", "UserJourney", "Service"):
        parents = ("System",) if entity == "UserJourney" else ()
        fields = {idfield(x): ID for x in parents}
        fields.update({"name": string(1, 256), "description": TEXT})
        required = [idfield(x) for x in parents] + ["name", "clientToken"]
        if entity == "Service":
            fields["memberships"] = array(local("MembershipInput"), maximum=100, unique=True)
            fields["resourceIds"] = array(ID, maximum=1000, unique=True)
        fields.update(MUT)
        def sample_create(e=entity, ps=parents):
            out = {**{idfield(x): identifier(x) for x in ps}, "name": record(e)["name"], "description": "Canonical workload catalog entry.", "clientToken": "create-" + lower(e) + "-demo-0001"}
            if e == "Service":
                out.update({"memberships": [{k: m[k] for k in ("systemId", "userJourneyIds")} for m in record(e)["memberships"]], "resourceIds": record(e)["resourceIds"]})
            return out
        add("Create" + entity, "workload", "LOCAL_COMMAND", "console:ManageCatalog", [entity, "Command"],
            obj(fields, required), command_response(entity), sample_create,
            ["Creates local canonical workload identity and metadata; it does not create an AWS resource.",
             "Provider aliases are established by trusted verified mapping, not by caller-supplied matching names.",
             "Membership inputs contain only local system/journey IDs; the server stamps origin=LOCAL and sourceRevisionId=null. Imported provenance is reserved to the trusted importer."])
        get("Get" + entity, entity, "workload", parents=parents)
        filters = {"systemId": ID, "userJourneyId": ID} if entity == "Service" else None
        listing("List" + ("UserJourneys" if entity == "UserJourney" else entity + "s"), entity, "workload", parents=parents, filters=filters,
                semantics=["Service membership is many-to-many and deduplicated by canonical serviceId; it does not establish journey execution order or end-to-end compliance."] if entity == "Service" else [])
        updates = {idfield(x): ID for x in (*parents, entity)}
        updates.update({"name": string(1, 256), "description": TEXT})
        if entity == "Service":
            updates.update({"memberships": array(local("MembershipInput"), maximum=100, unique=True), "resourceIds": array(ID, maximum=1000, unique=True)})
        writable = [k for k in updates if not k.endswith("Id")]
        updates.update(GUARDED)
        def sample_update(e=entity, ps=parents):
            return {**{idfield(x): identifier(x) for x in (*ps, e)}, "description": "Reviewed local description.",
                    "expectedVersion": record(e)["version"], "clientToken": "update-" + lower(e) + "-demo-0001"}
        add("Update" + entity, "workload", "LOCAL_COMMAND", "console:ManageCatalog", [entity, "Command"],
            obj(updates, [idfield(x) for x in (*parents, entity)] + ["expectedVersion", "clientToken"], anyOf=at_least_change(writable)),
            command_response(entity), sample_update,
            ["Updates only local fields under this record's version; an observation or projection does not cause a configuration conflict.",
             "Omitted fields are unchanged; an empty description is a known empty value; supplied arrays replace their complete owned membership set.",
             "Service is the sole membership writer. Every journey must belong to its paired system; a journey update cannot set a second service list."])
    add("GetServiceStatus", "workload", "READ", "console:Read", ["ProjectionRevision"], obj({"serviceId": ID}),
        obj({"projectionRevision": {"allOf": [model("ProjectionRevision"), {"properties": {"profile": {"const": "SERVICE_STATUS"}}}]}}),
        lambda: {"serviceId": identifier("Service")},
        ["Returns the currently selected SERVICE_STATUS projection under its named rule, including evidence/freshness/coverage. Clients do not infer current state from newest receipt time.",
         "No current selected projection returns ResourceNotFoundException with code PROJECTION_NOT_AVAILABLE, never an invented healthy/default object.",
         "Runtime health, native assessed posture, collection quality and operator workflow remain distinct dimensions."],
        response_selector={"ProjectionRevision": {"profile": "SERVICE_STATUS"}})
    add("GetWorkspaceSummary", "workload", "READ", "console:ReadWorkspace", ["ProjectionRevision"], obj({}),
        obj({"projectionRevision": {"allOf": [model("ProjectionRevision"), {"properties": {"profile": {"const": "WORKSPACE_SUMMARY"}}}]}}),
        lambda: {},
        ["Returns the current qualified WORKSPACE_SUMMARY for the trusted caller's authorized workload scope, including exact distinct contributor identities, denominator and rule.",
         "An empty authorized scope has null percentages. Retained historical evidence is separate from current usable coverage; no end-to-end journey compliance is inferred.",
         "A cached broader summary must be recomputed/selected for the authorized scope; hidden records cannot leak through counts."],
        response_selector={"ProjectionRevision": {"profile": "WORKSPACE_SUMMARY"}})
    get("GetDependency", "Dependency", "workload", parents=("Service",))
    listing("ListDependencies", "Dependency", "workload", parents=("Service",))
    fields = {"serviceId": ID, "dependencyId": ID, "decision": enum("ALLOWED", "REVIEW", "DENIED"), "reason": string(1, 4096), **GUARDED}
    add("UpdateDependencyGovernance", "workload", "LOCAL_COMMAND", "console:ManageGovernance", ["Dependency", "Command"],
        obj(fields), command_response("Dependency"),
        lambda: {"serviceId": identifier("Service"), "dependencyId": identifier("Dependency"), "expectedVersion": record("Dependency")["governance"]["version"],
                 "decision": "REVIEW", "reason": "Review the observed external dependency.", "clientToken": "governance-demo-0001"},
        ["expectedVersion addresses dependency.governance.version only; native classification remains separate.",
         "An allowed/denied decision is local governance. It neither changes DNS evidence nor grants/revokes network access."])


def add_health():
    get("GetHealthEvent", "HealthEvent", "health")
    listing("ListHealthEvents", "HealthEvent", "health", filters={"serviceCode": string(1, 128), "eventTypeCode": string(1, 256)})
    listing("ListEventContexts", "EventContext", "health", parents=("HealthEvent",), filters={"kind": enum("PUBLIC", "ACCOUNT", "ORG_SUMMARY")})
    listing("ListEntityImpacts", "EntityImpact", "health", parents=("HealthEvent", "EventContext"),
            semantics=["Account/public/organization-summary evidence never leaks between contexts. Counts remain qualified by collection coverage."])
    listing("ListCommunications", "Communication", "health", parents=("HealthEvent", "EventContext"),
            semantics=["Conflicting and partial notification pages remain visible; delivery recipients do not redefine impacted account identity."])
    listing("ListLifecycleEntries", "LifecycleEntry", "health", parents=("Snapshot",), filters={"serviceCode": string(1, 128)},
            semantics=["snapshotId must identify a LIFECYCLE_CATALOG capture. Entries from different catalog snapshots are not merged by title."])
    SAMPLES["ListLifecycleEntries"]["request"] = lambda: {"snapshotId": record("Snapshot", kind="LIFECYCLE_CATALOG")["snapshotId"], "maxResults": 20}
    get("GetComponentDeployment", "ComponentDeployment", "health", parents=("Resource",))
    listing("ListComponentDeployments", "ComponentDeployment", "health", parents=("Resource",),
            semantics=["Lifecycle exposure is a separate versioned projection using these observed component versions and a pinned lifecycle catalog."])


def native_fields(entity, parents=()):
    return {**{idfield(x): ID for x in (*parents, entity)}, "connectionId": ID, "expectedSourceRevisionId": ID, **MUT}


def native_sample(name, entity, parents=(), **extra):
    return lambda: {**{idfield(x): identifier(x) for x in (*parents, entity)}, "connectionId": identifier("Connection"),
                    "expectedSourceRevisionId": source_revision_for(entity), "clientToken": name.lower() + "-demo-0001", **extra}


NATIVE_NOTES = [
    "Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.",
    "expectedSourceRevisionId compares the local observed version before admission/dispatch; it does not create an AWS compare-and-swap guarantee.",
    "The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.",
    "The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's revision or a stale unrelated summary is rejected even in the same workspace.",
]


def add_resilience():
    get("GetResiliencePolicy", "ResiliencePolicy", "resilience")
    listing("ListResiliencePolicies", "ResiliencePolicy", "resilience")
    get("GetResilienceAssessment", "ResilienceAssessment", "resilience", parents=("Service",))
    listing("ListResilienceAssessments", "ResilienceAssessment", "resilience", parents=("Service",))
    get("GetFinding", "Finding", "resilience", parents=("Service",))
    listing("ListFindings", "Finding", "resilience", parents=("Service",), filters={"disposition": enum("OPEN", "RESOLVED", "IRRELEVANT"), "severity": enum("LOW", "MEDIUM", "HIGH")},
            semantics=["Findings are service-scoped. No mandatory assessment filter or ownership FK is invented; capture-to-assessment is qualified correlation."])
    get("GetRecommendation", "Recommendation", "resilience", parents=("Service", "Finding"))
    listing("ListRecommendations", "Recommendation", "resilience", parents=("Service", "Finding"), filters={"sourceRevisionId": ID},
            semantics=["Instances are observation/group/ordinal scoped; historical equal text does not establish provider identity continuity."])
    add("StartResilienceAssessment", "resilience", "PROVIDER_COMMAND", "console:RunResilienceAssessment", ["Command", "ResilienceAssessment"],
        obj({"serviceId": ID, "connectionId": ID, "expectedServiceVersion": VERSION, **MUT}), command_response(),
        lambda: {"serviceId": identifier("Service"), "connectionId": identifier("Connection"), "expectedServiceVersion": record("Service")["version"], "clientToken": "start-resilience-demo-0001"},
        ["Pins the local service scope at admission, then requests native StartFailureModeAssessment. expectedServiceVersion is local only.",
         "GetCommand exposes the created assessment identity after readback. SUCCESS of assessment execution does not imply achievable posture or verified remediation.",
         "Findings remain service-scoped and independent of a particular run."], native=("StartFailureModeAssessment",))
    fields = native_fields("Finding", ("Service",))
    fields.update({"disposition": enum("OPEN", "RESOLVED", "IRRELEVANT"), "comment": string(0, 4096)})
    add("UpdateFindingDisposition", "resilience", "PROVIDER_COMMAND", "console:UpdateFindingDisposition", ["Finding", "Command"],
        obj(fields, [k for k in fields if k != "comment"]), command_response(),
        native_sample("UpdateFindingDisposition", "Finding", ("Service",), disposition="RESOLVED", comment="Change deployed; verification still required."),
        [*NATIVE_NOTES, "Maps only status/comment. Disposition is an operator assertion, not a new posture or finding-specific verification."], native=("UpdateFailureModeFinding",))
    fields = native_fields("Dependency", ("Service",))
    fields.update({"criticality": enum("HARD", "SOFT", "UNKNOWN"), "comment": string(0, 4096)})
    add("UpdateDependencyClassification", "resilience", "PROVIDER_COMMAND", "console:UpdateDependencyClassification", ["Dependency", "Command"],
        obj(fields, [k for k in fields if k not in ("criticality", "comment")], anyOf=at_least_change(["criticality", "comment"])), command_response(),
        native_sample("UpdateDependencyClassification", "Dependency", ("Service",), criticality="HARD"),
        [*NATIVE_NOTES, "Native criticality/comment and local allowed/denied governance have separate commands and revision ownership."], native=("UpdateDependency",))
    DEFS["RecoveryTargetsInput"] = obj({
        "rtoInMinutes": integer(0, 5256000), "rpoInMinutes": integer(0, 5256000),
        "disasterRecoveryApproach": enum("ACTIVE_ACTIVE", "HOT_STANDBY", "WARM_STANDBY", "PILOT_LIGHT", "BACKUP_AND_RESTORE"),
    }, [], minProperties=1)
    DEFS["ResiliencePolicyChanges"] = obj({
        "description": string(0, 615), "availabilitySlo": obj({"target": {"type": "number", "minimum": 0, "maximum": 100}}),
        "dataRecovery": obj({"timeBetweenBackupsInMinutes": integer(0, 5256000)}),
        "multiAz": local("RecoveryTargetsInput"), "multiRegion": local("RecoveryTargetsInput"), "sharingEnabled": BOOL,
    }, [], minProperties=1)
    fields = native_fields("ResiliencePolicy")
    fields["changes"] = local("ResiliencePolicyChanges")
    add("UpdateResiliencePolicyConfiguration", "resilience", "PROVIDER_COMMAND", "console:ManageProviderConfiguration", ["ResiliencePolicy", "Command"],
        obj(fields), command_response(),
        native_sample("UpdateResiliencePolicyConfiguration", "ResiliencePolicy", changes={"availabilitySlo": {"target": 99.95}}),
        [*NATIVE_NOTES, "The narrow supported write subset has four native component families. Explicit detachment/component clearing is deferred until native semantics are verified.",
         "Policy changes invalidate current applicability without modifying captured policy contexts or historical posture."], native=("UpdatePolicy",))
    DEFS["ResilienceServiceChanges"] = obj({
        "description": string(0, 615), "regions": array(string(6, 64, pattern="^[a-z]{2}-((iso[a-z]?|gov)-)?[a-z]+-[0-9]$"), 1, 5, True),
        "resiliencePolicyId": ID, "dependencyDiscovery": enum("ENABLED", "DISABLED"),
    }, [], minProperties=1)
    fields = native_fields("Service")
    fields["changes"] = local("ResilienceServiceChanges")
    add("UpdateResilienceServiceConfiguration", "resilience", "PROVIDER_COMMAND", "console:ManageProviderConfiguration", ["Service", "Command"],
        obj(fields), command_response(),
        native_sample("UpdateResilienceServiceConfiguration", "Service", changes={"dependencyDiscovery": "ENABLED"}),
        [*NATIVE_NOTES, "Changes the verified Resilience Hub service profile only. Local UpdateService remains the canonical catalog/membership command.",
         "This initial write subset covers description, Regions, direct policy attachment and desired discovery state. Native creation/deletion, association replacement, permissions, report configuration and clearing remain deferred adapter commands."], native=("UpdateService",))
    fields = {"serviceId": ID, "findingId": ID, "recommendationId": ID, "title": string(1, 256), "effort": string(1, 4096),
              "estimate": model("RecommendationEstimate"), "assigneeSubjectId": ID,
              "workState": enum("OPEN", "PLANNED", "IN_PROGRESS", "DONE", "DISMISSED"), "note": TEXT,
              "clearFields": clear_fields("title", "effort", "estimate", "owner"), **GUARDED}
    add("UpdateRecommendationEnrichment", "resilience", "LOCAL_COMMAND", "console:ManageRecommendationWork", ["Recommendation", "Command"],
        obj(fields, ["serviceId", "findingId", "recommendationId", "expectedVersion", "clientToken"], anyOf=at_least_change(["title", "effort", "estimate", "assigneeSubjectId", "workState", "note", "clearFields"])), command_response("Recommendation"),
        lambda: {"serviceId": identifier("Service"), "findingId": identifier("Finding"), "recommendationId": identifier("Recommendation"),
                 "expectedVersion": record("Recommendation")["enrichment"]["version"], "workState": "PLANNED", "clientToken": "enrich-recommendation-demo-0001"},
        ["expectedVersion refers to recommendation.enrichment.version; immutable source suggestion and observation identity never change.",
         "Estimate amount/currency/basis/complexity/source/time/confidence are typed local information, separate from native assessment execution cost.",
         "The trusted directory resolves assigneeSubjectId; the server stamps mutation provenance/updatedAt. Assignment is not acting identity and cannot be combined with clearing owner.",
         "Local work completion/estimates do not establish provider remediation or recommendation identity across generated observations."])


def add_investigation():
    get("GetAgentSpace", "AgentSpace", "investigation")
    listing("ListAgentSpaces", "AgentSpace", "investigation")
    get("GetInvestigation", "Investigation", "investigation", parents=("AgentSpace",))
    listing("ListInvestigations", "Investigation", "investigation", parents=("AgentSpace",))
    get("GetExecution", "Execution", "investigation", parents=("AgentSpace",),
        semantics=["AgentSpace is the owner scope. A single investigation foreign key is not required, preserving chat and shared/referenced executions."])
    listing("ListExecutions", "Execution", "investigation", parents=("AgentSpace",), filters={"investigationId": ID},
            semantics=["The optional investigation filter uses explicit TaskExecutionMembership evidence. A linked task can reference an execution created elsewhere in the same AgentSpace."])
    get("GetJournalRecord", "JournalRecord", "investigation", parents=("AgentSpace", "Execution"))
    listing("ListJournalRecords", "JournalRecord", "investigation", parents=("AgentSpace", "Execution"),
            semantics=["Journal record identity, raw native type and graph extraction provenance remain separate; a textual mention does not create a graph link."])
    get("GetApprovalRequest", "ApprovalRequest", "investigation", parents=("AgentSpace", "Execution"))
    listing("ListApprovalRequests", "ApprovalRequest", "investigation", parents=("AgentSpace", "Execution"),
            semantics=["These are retained validated chat request contexts, not a fabricated native Get/ListApproval API. A waiting task or Markdown button is insufficient."])
    get("GetAsset", "Asset", "investigation", parents=("AgentSpace",))
    listing("ListAssets", "Asset", "investigation", parents=("AgentSpace",))
    add("StartInvestigation", "investigation", "PROVIDER_COMMAND", "console:StartInvestigation", ["Investigation", "Command"],
        obj({"agentSpaceId": ID, "connectionId": ID, "title": string(1, 400), "description": string(0, 10000),
             "priority": enum("CRITICAL", "HIGH", "MEDIUM", "LOW", "MINIMAL"), **MUT},
            ["agentSpaceId", "connectionId", "title", "priority", "clientToken"]), command_response(),
        lambda: {"agentSpaceId": identifier("AgentSpace"), "connectionId": identifier("Connection"), "title": "Investigate checkout latency", "priority": "HIGH", "clientToken": "start-investigation-demo-0001"},
        ["Requests CreateBacklogTask with taskType=INVESTIGATION; it is not a native operation named StartInvestigation.",
         "A task creation receipt does not prove execution started. Native task, execution and result observations are reconciled separately.",
         "The adapter maps the durable console intent to a stable provider token within native bounds; no raw tenant/actor is accepted."], native=("CreateBacklogTask",))
    decision = {"agentSpaceId": ID, "executionId": ID, "approvalRequestId": ID, "connectionId": ID,
                "expectedRequestSourceRevisionId": ID, "expectedActionDigest": model("Digest"),
                "decision": enum("APPROVED", "REJECTED"), "singleUse": {"const": True}, "reason": string(0, 1024), **MUT}
    add("DecideApproval", "investigation", "PROVIDER_COMMAND", "console:DecideApproval", ["ApprovalRequest", "Command"],
        obj(decision, [k for k in decision if k not in ("reason", "singleUse")], allOf=[
            {"if": {"properties": {"decision": {"const": "APPROVED"}}}, "then": {"required": ["singleUse"]}},
            {"if": {"properties": {"decision": {"const": "REJECTED"}}}, "then": {"not": {"required": ["singleUse"]}}},
        ]), command_response(),
        lambda: {"agentSpaceId": identifier("AgentSpace"), "executionId": identifier("Execution"), "approvalRequestId": identifier("ApprovalRequest"),
                 "connectionId": identifier("Connection"), "expectedRequestSourceRevisionId": record("ApprovalRequest")["requestSourceRevisionId"],
                 "expectedActionDigest": record("ApprovalRequest")["actionDigest"], "decision": "REJECTED",
                 "reason": "The requested mutation is outside this investigation's intended scope.", "clientToken": "decide-approval-demo-0001"},
        ["First-release decision supports exact observed scope and single use only; reusable grants and pattern editing are explicitly deferred.",
         "APPROVED requires singleUse=true. REJECTED omits singleUse; the adapter also omits native pattern and TTL fields for rejection.",
         "Validates a complete authenticated chat request context and exact action digest, then invokes UpdateApprovalAction. It neither resumes the execution nor claims the tool ran.",
         "Native UpdateApprovalAction has no modeled idempotency token. A lost response is OUTCOME_UNKNOWN; local replay returns the receipt and must not repeat the remote mutation blindly.",
         "A successful rejection is a successful decision command, not a provider API failure."], native=("UpdateApprovalAction",))
    add("ResumeExecution", "investigation", "PROVIDER_COMMAND", "console:ResumeExecution", ["Execution", "ApprovalRequest", "Command"],
        obj({"agentSpaceId": ID, "executionId": ID, "approvalRequestId": ID, "decisionCommandId": ID, "connectionId": ID, **MUT}), command_response(),
        lambda: {"agentSpaceId": identifier("AgentSpace"), "executionId": identifier("Execution"), "approvalRequestId": identifier("ApprovalRequest"),
                 "decisionCommandId": "cmd-decideapproval-demo", "connectionId": identifier("Connection"), "clientToken": "resume-execution-demo-0001"},
        ["Requires a definitively successful matching decision Command, valid current authorization and a validated approval/interrupt/tool-use context.",
         "Constructs the native SendMessage APPROVAL_ACTION context from that retained request; the caller cannot substitute interrupt/tool IDs or widen approved scope.",
         "Decision, resume submission, credential redemption and actual tool outcome remain separate. Opening or completing a stream does not prove the tool succeeded.",
         "SendMessage has no modeled idempotency token. Persist stream fragments and unknown outcomes; do not blindly resend on disconnect."], native=("SendMessage",))


def add_workflow():
    add("CreateScenario", "workflow", "LOCAL_COMMAND", "console:AuthorScenario", ["Scenario", "Command"],
        obj({"name": string(1, 256), "description": TEXT, "draftDefinition": model("ScenarioDraft"), **MUT}, ["name", "draftDefinition", "clientToken"]), command_response("Scenario"),
        lambda: {"name": record("Scenario")["name"], "description": record("Scenario")["description"], "draftDefinition": record("Scenario")["draftDefinition"], "clientToken": "create-scenario-demo-0001"},
        ["Creates a local editable draft. An author cannot set trusted operation locks, capability grants or a published digest."])
    get("GetScenario", "Scenario", "workflow")
    listing("ListScenarios", "Scenario", "workflow", filters={"archived": BOOL})
    fields = {"scenarioId": ID, "name": string(1, 256), "description": TEXT, "draftDefinition": model("ScenarioDraft"), "archived": BOOL,
              "defaultRevisionId": ID, "clearFields": clear_fields("defaultRevisionId"), **GUARDED}
    add("UpdateScenario", "workflow", "LOCAL_COMMAND", "console:AuthorScenario", ["Scenario", "Command"],
        obj(fields, ["scenarioId", "expectedVersion", "clientToken"], anyOf=at_least_change(["name", "description", "draftDefinition", "archived", "defaultRevisionId", "clearFields"])), command_response("Scenario"),
        lambda: {"scenarioId": identifier("Scenario"), "expectedVersion": record("Scenario")["version"], "description": "Updated authoring note; published programs remain immutable.", "clientToken": "update-scenario-demo-0001"},
        ["Only the draft/catalog record changes; a default revision must belong to this Scenario. No already admitted Run is redirected.",
         "Omitted fields preserve; clearFields=[defaultRevisionId] removes the default pointer. Supplying it and clearing it in one request is invalid.",
         "archived=true rejects new Run admission while preserving all published revisions and historical Runs; exact replay of an already admitted Run still returns its original receipt."])
    add("PublishScenarioRevision", "workflow", "LOCAL_COMMAND", "console:PublishScenario", ["ScenarioRevision", "Scenario", "Command"],
        obj({"scenarioId": ID, "expectedVersion": VERSION, **MUT}), command_response("ScenarioRevision"),
        lambda: {"scenarioId": identifier("Scenario"), "expectedVersion": record("Scenario")["version"], "clientToken": "publish-scenario-demo-0001"},
        ["Compiles the exact current draft, resolves retained immutable implementation/schema locks and atomically publishes a new revision.",
         "Publication validates DAGs, dependency-scoped references, typed bindings, capability checks, required criteria, finalizers and fixed language/reducer semantics before any external work.",
         "The caller cannot submit a trusted lock or digest. Changing a later alias cannot alter this revision. Missing/revoked pinned artifacts reject future admission, never substitute."])
    get("GetScenarioRevision", "ScenarioRevision", "workflow", parents=("Scenario",))
    listing("ListScenarioRevisions", "ScenarioRevision", "workflow", parents=("Scenario",))
    input_values = {"type": "object", "additionalProperties": model("JsonValue"), "maxProperties": 100}
    bindings = {"type": "object", "propertyNames": string(1, 64, pattern="^[a-z][a-z0-9_]*$"), "additionalProperties": ID, "maxProperties": 100}
    add("StartRun", "workflow", "EXECUTION_COMMAND", "console:StartRun", ["Run", "Snapshot", "Command"],
        obj({"scenarioRevisionId": ID, "subject": model("EntityRef"), "expectedSubjectVersion": VERSION,
             "inputs": input_values, "bindings": bindings, **MUT}, ["scenarioRevisionId", "subject", "inputs", "bindings", "clientToken"]), command_response("Run"),
        lambda: {"scenarioRevisionId": identifier("ScenarioRevision"), "subject": eref("Service"), "expectedSubjectVersion": record("Service")["version"],
                 "inputs": record("Snapshot", kind="RUN_INPUT")["contents"]["inputValues"], "bindings": {"aws": identifier("Connection")}, "clientToken": "start-run-demo-0001"},
        ["Durably admits one Run, all StepRuns and a closed RUN_INPUT snapshot atomically; no claim that an AWS call has started.",
         "inputs are intentionally revision-defined and must pass its pinned closed input schema; unknown binding names, raw secrets, undeclared operations or unauthorized scope are rejected.",
         "Admission fixes enabled steps and the required-criterion denominator. Runtime skips/cancellation cannot shrink it; inapplicable admission criteria remain recorded.",
         "expectedSubjectVersion applies only when the subject is a local mutable configuration; it is not an AWS deployment lock. Material dispatch preconditions are rechecked by the adapter.",
         "A new execution intent uses a new clientToken. Pinned revision identity, never the default pointer, selects the program."])
    OPS[-1]["semantics"].append("The revision's owning Scenario must not be archived at new admission; archive state cannot redirect or cancel an already admitted Run.")
    get("GetRun", "Run", "workflow")
    listing("ListRuns", "Run", "workflow", filters={"scenarioRevisionId": ID, "phase": MODEL["$defs"]["Run"]["properties"]["phase"]})
    add("RequestRunCancellation", "workflow", "EXECUTION_COMMAND", "console:CancelRun", ["Run", "Command"],
        obj({"runId": ID, "reason": string(1, 4096), **MUT}, ["runId", "clientToken"]),
        obj({"command": model("Command"), "accepted": BOOL, "run": model("Run")}),
        lambda: {"runId": identifier("Run"), "reason": "Stop this assessment and reconcile outstanding effects.", "clientToken": "cancel-run-demo-0001"},
        ["Atomically accepts monotonic cancellation intent and fences new main dispatch; it does not set a remote effect to stopped.",
         "Already sealed Run returns accepted=false and its unchanged terminal record. Exact replay preserves the original accepted receipt after later completion.",
         "Finalizers reconcile active/unknown effects, including a lost Start response with no handle. A creating Start must never be reissued after cancellation just to discover its result.",
         "Different cancellation tokens converge on the first accepted intent. Cleanup, execution result and workload verdict remain independently visible."])
    listing("ListRunSteps", "StepRun", "workflow", parents=("Run",),
            semantics=["Includes every compiled step, including skipped zero-attempt steps. No independent retry/stop/status-update command exists."])
    listing("ListStepAttempts", "StepAttempt", "workflow", parents=("Run", "StepRun"),
            semantics=["Ordered by attemptNo; polling/resume/transport retry remain within the same attempt. A new mutating attempt is forbidden while its predecessor's effect is unresolved."])


def add_fis():
    get("GetExperiment", "Experiment", "fis", semantics=["Native actions are keyed by experiment + actionName; their catalog actionId is not an execution identity.",
        "Selected memberships, applied effects, workload criteria and report readiness are separate evidence dimensions."])
    listing("ListExperiments", "Experiment", "fis", filters={"connectionId": ID, "runId": ID},
            semantics=["runId filters only verified ExternalOperationRef links; imported experiments can have no product workflow Run."])
    fields = native_fields("Experiment")
    fields["reason"] = string(1, 4096)
    add("StopExperiment", "fis", "PROVIDER_COMMAND", "console:StopExperiment", ["Experiment", "Command"],
        obj(fields, [k for k in fields if k != "reason"]), command_response(),
        native_sample("StopExperiment", "Experiment", reason="Operator requested stop of the whole native experiment."),
        [*NATIVE_NOTES, "Requests native StopExperiment for the whole experiment; no individual native action stop/retry/pause command is fabricated.",
         "Stop acceptance, final native state, post-action cleanup, workload recovery and report completion remain separate.",
         "Starting new fault experiments is available only through an explicitly authorized pinned workflow adapter in this initial facade."], native=("StopExperiment",))


def command_example(op, request, result_entities=()):
    result = record("Command")
    result.update({"commandId": "cmd-" + op["name"].lower() + "-demo", "operation": op["name"],
                   "clientToken": request["clientToken"], "requestDigest": digest(request),
                   "expectedVersion": request.get("expectedVersion"), "acceptedAt": NOW,
                   "state": "ACCEPTED" if op["kind"] == "PROVIDER_COMMAND" else "SUCCEEDED",
                   "attempts": [], "effects": [], "replayExpiresAt": NOW + (90 * 86400 if op["kind"] == "EXECUTION_COMMAND" else 86400),
                   "subjectRefs": [], "resultRefs": [eref(x) for x in result_entities]})
    for entity in MODEL["x-entities"]:
        # x-entities is a list of names in the canonical model.
        if isinstance(entity, dict):
            entity = entity["name"]
        key = idfield(entity)
        if key in request:
            result["subjectRefs"].append({"kind": entity, "id": request[key]})
    if "subject" in request:
        result["subjectRefs"].append(copy.deepcopy(request["subject"]))
    if "subjectRefs" in request:
        result["subjectRefs"] += copy.deepcopy(request["subjectRefs"])
    return result


def create_response(op, request):
    output = DEFS[op["name"] + "Response"]["properties"]
    selectors = SAMPLES[op["name"]]["responseSelector"]
    result = {}
    for key, shape in output.items():
        if key == "command" and op["mutating"]:
            continue
        if key == "nextToken":
            continue  # This example contains one complete local page.
        if key == "items":
            entity = shape["items"]["$ref"].rsplit("/", 1)[1]
            result[key] = [record(entity)]
        elif key == "page":
            result[key] = {"traversalId": "page-" + op["name"].lower() + "-demo", "asOfSequence": 1, "createdAt": NOW, "expiresAt": NOW + 900}
        elif key == "accepted":
            result[key] = True
        elif "$ref" in shape:
            entity = shape["$ref"].rsplit("/", 1)[1]
            result[key] = record(entity, **selectors.get(entity, {}))
        elif "allOf" in shape and "$ref" in shape["allOf"][0]:
            entity = shape["allOf"][0]["$ref"].rsplit("/", 1)[1]
            result[key] = record(entity, **selectors.get(entity, {}))
        else:
            raise ValueError(f"No response generator for {op['name']} {key}")
    # Examples are independent contract illustrations, not a recorded invocation log.
    name = op["name"]
    for entity in ("System", "UserJourney", "Service", "Scenario", "Connection", "WorkItem"):
        if name in ("Create" + entity, "Update" + entity):
            row = result[lower(entity)]
            for key, value in request.items():
                if key in row and key not in (idfield(entity), "version", "localUpdatedAt", "providerBindings"):
                    row[key] = copy.deepcopy(value)
            row["version"] = 1 if name.startswith("Create") else request["expectedVersion"] + 1
            row["localUpdatedAt"] = NOW
            for key in request.get("clearFields", []):
                row[key] = None
            if name.startswith("Create") and "providerBindings" in row:
                row["providerBindings"] = []
            if "memberships" in request:
                row["memberships"] = [{**m, "origin": "LOCAL", "sourceRevisionId": None} for m in request["memberships"]]
            if "assigneeSubjectId" in request:
                row["owner"] = {"issuer": "fixture-identity", "subject": request["assigneeSubjectId"], "kind": "HUMAN"}
            if name == "CreateScenario":
                row["defaultRevisionId"] = None
                row["archived"] = False
            if name == "CreateWorkItem":
                row.update({"state": "OPEN", "owner": None, "snoozedUntil": None, "resolutionEvidence": [], "actions": [],
                            "priority": request.get("priority", "MEDIUM"), "dueAt": request.get("dueAt"), "verificationState": "NOT_REQUESTED", "verificationEvidence": []})
    if name == "UpdateDependencyGovernance":
        gov = result["dependency"]["governance"]
        gov["version"] = request["expectedVersion"] + 1
        if "decision" in gov:
            gov["decision"] = request["decision"]
        if "reason" in gov:
            gov["reason"] = request["reason"]
        gov["updatedAt"] = NOW
    if name == "UpdateRecommendationEnrichment":
        enriched = result["recommendation"]["enrichment"]
        enriched["version"] = request["expectedVersion"] + 1
        for key in ("title", "effort", "estimate", "workState", "note"):
            if key in request:
                enriched[key] = request[key]
        for key in request.get("clearFields", []):
            enriched[key] = None
        if "assigneeSubjectId" in request:
            enriched["owner"] = {"issuer": "fixture-identity", "subject": request["assigneeSubjectId"], "kind": "HUMAN"}
        enriched["updatedAt"] = NOW
        enriched["provenance"] = "LOCAL_OPERATOR_ENRICHMENT"
    if name == "RecordWorkItemVerification":
        result["workItem"].update({"version": request["expectedVersion"] + 1, "localUpdatedAt": NOW,
                                  "verificationState": request["result"], "verificationEvidence": copy.deepcopy(request["evidenceRefs"])})
    if name == "PublishScenarioRevision":
        result["scenarioRevision"].update({"scenarioRevisionId": "scenario-revision-published-demo", "revisionNumber": max(r["revisionNumber"] for r in RECORDS["ScenarioRevision"]) + 1, "publishedAt": NOW})
    if name == "StartRun":
        row = result["run"]
        row.update({"phase": "ADMITTED", "executionOutcome": "PENDING", "assessmentVerdict": "INCONCLUSIVE", "assessmentFinality": "PROVISIONAL",
                    "finalizationState": "PENDING", "effectState": "NONE", "cancellationIntent": None, "admittedAt": NOW, "terminalAt": None})
    if name == "StartCollection":
        result["collection"].update({"state": "RUNNING", "startedAt": NOW, "endedAt": None, "coverage": [], "projectionVersion": 1})
    if name == "CompleteCollection":
        result["collection"].update({"state": "COMPLETED", "endedAt": NOW, "coverage": copy.deepcopy(request["coverage"]), "projectionVersion": request["expectedProjectionVersion"] + 1})
    if "command" in output and op["mutating"]:
        entities = [e for e in op["entities"] if lower(e) in result and e != "Command"]
        result["command"] = command_example(op, request, entities)
        result["command"]["resultRefs"] = [{"kind": e, "id": result[lower(e)][idfield(e)]} for e in entities]
    if name == "UpdateWorkItem":
        result["workItem"]["actions"].append({"actionKey": "action-update-work-item-demo", "action": "UPDATE_WORK_ITEM",
            "actor": result["command"]["actor"], "at": NOW, "reason": request.get("note", ""), "evidenceRefs": request.get("resolutionEvidence", [])})
    if name == "RecordWorkItemVerification":
        result["workItem"]["actions"].append({"actionKey": "action-verify-work-item-demo", "action": "RECORD_VERIFICATION",
            "actor": result["command"]["actor"], "at": NOW, "reason": request["rationale"], "evidenceRefs": copy.deepcopy(request["evidenceRefs"])})
    if name == "RequestRunCancellation":
        result["run"].update({
            "phase": "FINALIZING", "executionOutcome": "RUNNING", "assessmentVerdict": "INCONCLUSIVE",
            "assessmentFinality": "PROVISIONAL", "finalizationState": "RUNNING", "effectState": "UNKNOWN", "terminalAt": None,
            "cancellationIntent": {"commandId": result["command"]["commandId"], "acceptedAt": NOW,
                                   "actor": result["command"]["actor"], "reason": request.get("reason", "")},
        })
    if name == "IngestObservation":
        for key, value in request["source"].items():
            result["sourceRevision"][key] = copy.deepcopy(value)
        for key, value in request.items():
            if key in result["observation"]:
                result["observation"][key] = copy.deepcopy(value)
        result["sourceRevision"]["sourceRevisionId"] = result["observation"]["sourceRevisionId"]
    return result


def describe_type(shape):
    if "$ref" in shape:
        return shape["$ref"].rsplit("/", 1)[1]
    if "const" in shape:
        return "literal " + json.dumps(shape["const"])
    if "enum" in shape:
        return "/".join(map(str, shape["enum"]))
    if "anyOf" in shape:
        return " or ".join(describe_type(s) for s in shape["anyOf"])
    if "allOf" in shape:
        return describe_type(shape["allOf"][0])
    if shape.get("type") == "array":
        return "List<" + describe_type(shape["items"]) + ">"
    return shape.get("type", "defined union")


def predecessor_mappings():
    rows = []
    def put(package, operations, targets, disposition, notes):
        for operation in operations.split():
            rows.append({"sourcePackage": package, "sourceOperation": operation, "disposition": disposition,
                         "newOperations": targets.split() if targets else [], "notes": notes})
    rh = "aws/resilience-hub/analysis/api"
    wf = "aws/fis/analysis/workflow"
    for entity, plural in (("System", "Systems"), ("UserJourney", "UserJourneys"), ("Service", "Services")):
        put(rh, "Get" + entity, "Get" + entity + " GetSourceRevision", "CANONICAL_READ_WITH_NATIVE_FACET",
            "Local canonical identity is separate from the retained native profile; verified provider binding supplies the bridge.")
        put(rh, "List" + plural, "List" + plural + " ListSourceRevisions", "CANONICAL_READ_WITH_NATIVE_FACET",
            "Canonical catalog list plus typed native source profiles; unresolved native references are not silently discarded.")
    put(rh, "CreateSystem CreateUserJourney CreateService CreatePolicy", "", "DEFERRED_NATIVE_COMMAND",
        "Old commands created provider resources. New identically named catalog Create commands are LOCAL and are not migration aliases for native creation.")
    put(rh, "UpdateSystem UpdateUserJourney", "", "DEFERRED_NATIVE_COMMAND",
        "Native description/sharing/journey/policy edits remain later adapter work; local UpdateSystem/UpdateUserJourney edit canonical metadata only.")
    put(rh, "DeleteSystem DeleteUserJourney DeleteService DeletePolicy", "", "DEFERRED_NATIVE_COMMAND",
        "Native destructive semantics/guards and preserved history need explicit later commands. No local delete substitutes for them.")
    put(rh, "UpdateService", "UpdateResilienceServiceConfiguration", "NARROW_PROVIDER_SUBSET",
        "Description, Regions, direct policy attachment and discovery intent now have explicit native authority. Remaining native fields and clearing are deferred.")
    put(rh, "UpdatePolicy", "UpdateResiliencePolicyConfiguration", "NARROW_PROVIDER_SUBSET",
        "Typed native policy components/description/sharing; no generic clear or local rename forwarded to the provider.")
    put(rh, "GetPolicy", "GetResiliencePolicy", "RENAMED_TYPED_READ", "Explicitly names the resilience policy bounded context.")
    put(rh, "ListPolicies", "ListResiliencePolicies", "RENAMED_TYPED_READ", "Explicitly names the resilience policy bounded context.")
    put(rh, "CreateInputSource DeleteInputSource", "", "DEFERRED_NATIVE_COMMAND", "Retained input-source profile is in scope; provider CRUD is deferred.")
    put(rh, "ListInputSources", "ListSourceRevisions GetSourceRevision", "RETAINED_TYPED_PROFILE", "Use aws.resilience-hub.input-source/v1 and exact service-scoped source identity.")
    put(rh, "StartFailureModeAssessment", "StartResilienceAssessment", "EXPLICIT_ASYNC_COMMAND", "Receipt and later provider assessment identity are separate.")
    put(rh, "GetFailureModeAssessment", "GetResilienceAssessment", "RENAMED_TYPED_READ", "Retained service-scoped provider execution; no invented native Get call.")
    put(rh, "ListFailureModeAssessments", "ListResilienceAssessments", "RENAMED_TYPED_READ", "Stable local traversal, with independent upstream coverage.")
    put(rh, "GetFailureModeFinding", "GetFinding", "CANONICAL_READ_WITH_NATIVE_FACET", "Scoped finding; summary/detail observations and captures remain explicit.")
    put(rh, "ListFailureModeFindings", "ListFindings", "CANONICAL_READ_WITH_NATIVE_FACET", "No mandatory assessment ownership is inferred.")
    put(rh, "UpdateFailureModeFinding", "UpdateFindingDisposition", "EXPLICIT_ASYNC_COMMAND", "Native status/comment only; no posture or repair verification implied.")
    for operation in ("GetRecommendation", "ListRecommendations", "UpdateRecommendationEnrichment", "GetDependency", "ListDependencies", "UpdateDependencyGovernance"):
        put(rh, operation, operation, "PRESERVED_WITH_CANONICAL_SCOPE", "Canonical IDs replace native URL-like keys; source identity and independent local versions remain retained.")
    put(rh, "UpdateDependency", "UpdateDependencyClassification", "EXPLICIT_ASYNC_COMMAND", "Provider criticality/comment remain separate from local governance.")
    put(rh, "CaptureTopologySnapshot", "CaptureSnapshot", "SHARED_CAPTURE", "kind=TOPOLOGY; preserves source times and closed manifest, not a native atomic snapshot.")
    put(rh, "GetTopologySnapshot", "GetSnapshot", "SHARED_CAPTURE", "Read the exact retained topology snapshot identity.")
    put(rh, "ListTopologySnapshots", "ListSnapshots", "SHARED_CAPTURE", "Filter kind=TOPOLOGY and the exact service subject.")
    put(rh, "GetServiceStatus", "GetServiceStatus", "QUALIFIED_PROJECTION_READ", "Returns currently selected SERVICE_STATUS ProjectionRevision with its evidence and independent dimensions.")
    put(rh, "GetWorkspaceSummary", "GetWorkspaceSummary", "QUALIFIED_PROJECTION_READ", "Returns WORKSPACE_SUMMARY for authorized contributors, with denominator and rule.")
    put(rh, "ListEvents", "ListObservations ListSourceRevisions", "SHARED_EVIDENCE_READ", "Filter exact subjects/profile/channel evidence; delivery ID never becomes a HealthEvent ID.")
    put(rh, "PutHealthObservation", "IngestObservation PublishProjection", "SHARED_TRUSTED_INGEST", "Retain runtime-health source evidence then derive SERVICE_STATUS. This is distinct from AWS Health Event ingestion.")
    put(rh, "IngestEvent", "IngestObservation StartCollection", "SHARED_TRUSTED_INGEST", "Retains raw channel evidence and schedules authorized read collection; event body cannot patch authoritative state.")
    for operation in ("GetScenario", "ListScenarios", "GetScenarioRevision", "ListScenarioRevisions", "GetRun", "ListRuns", "RequestRunCancellation", "ListRunSteps", "ListStepAttempts"):
        put(wf, operation, operation, "RPC_REBINDING", "Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions.")
    put(wf, "CreateScenario", "CreateScenario", "EXTENDED_AUTHORING_CONTRACT", "Creates metadata and a typed editable draft; trusted operation locks remain publication-owned.")
    put(wf, "UpdateScenario", "UpdateScenario", "RPC_REBINDING", "expectedVersion replaces If-Match; omission preserves and explicit allowed clears replace nullable PATCH ambiguity.")
    put(wf, "PublishScenarioRevision", "UpdateScenario PublishScenarioRevision", "DRAFT_THEN_PUBLISH", "Update the typed draft, then publish its exact expected Scenario version; server compiles and resolves trusted locks.")
    put(wf, "StartRun", "StartRun", "RPC_REBINDING", "Pins canonical subject, revision, validated inputs and authorized bindings; retains immutable admission and criterion denominator.")
    put(wf, "ListRunEvidence", "ListObservations ListSourceRevisions ListProjectionRevisions", "SHARED_TYPED_EVIDENCE", "Filter the exact Run subject/producer references; raw source, receipt and derived evidence types stay explicit.")
    put(wf, "GetEvidence", "GetSourceRevision GetObservation GetProjectionRevision GetSnapshot", "SHARED_TYPED_EVIDENCE", "Resolve the discriminated EvidenceRef kind; evidence is not collapsed into an untyped payload.")
    put(wf, "ListOperations", "GetScenarioRevision", "DYNAMIC_DISCOVERY_DEFERRED", "Published locks remain inspectable. Authorized discovery of executable adapter aliases is later registry work; facade operations.json is not that adapter registry.")
    assert sum(x["sourcePackage"] == rh for x in rows) == 44
    assert sum(x["sourcePackage"] == wf for x in rows) == 16
    assert len({(x["sourcePackage"], x["sourceOperation"]) for x in rows}) == 60
    available = {op["name"] for op in OPS}
    assert all(set(row["newOperations"]) <= available for row in rows)
    return rows


def generate_docs(catalog):
    lines = ["# Consolidated operations console — RPC operations", "",
             f"API version **2026-11-05** · namespace `{NAMESPACE}` · **{len(OPS)} operations**", "",
             "**Status: phase-one design contracts.** There is no HTTP server, provider adapter, authentication implementation, scheduler or executed cloud mutation in this package. The schemas, examples and validation make the proposed interface reviewable. [Protocol](PROTOCOL.md) defines the shared semantics; [model](../MODEL.md) defines authority and identity.", "",
             "All calls use `POST /` with `application/x-amz-json-1.1` and `X-Amz-Target: " + NAMESPACE + ".<Operation>`. Successful calls use HTTP 200, including durable asynchronous command receipts. `Command.state=SUCCEEDED` means that command's documented effect succeeded; it does not imply successful assessment, healthy workload or verified repair.", "",
             "Exact request/response schemas are in [rpc.schema.json](rpc.schema.json). [operations.json](operations.json) records scope, permissions, provenance, delivery phase and errors. [examples.json](examples.json) contains one complete synthetic request/response for every operation. Inputs are closed writable DTOs. Responses refer directly to the canonical model shapes; clients tolerate optional future response members and raw future provider vocabulary.", "",
             "## Module index", "", "| Module | Operations | Read | Mutating |", "| --- | ---: | ---: | ---: |"]
    grouped = defaultdict(list)
    for op in OPS:
        grouped[op["module"]].append(op)
    for module, operations in grouped.items():
        count = sum(not x["mutating"] for x in operations)
        lines.append(f"| [{module}](#{module}) | {len(operations)} | {count} | {len(operations)-count} |")
    lines += ["", "## Common field conventions", "",
              "`clientToken` is required for every mutation. `expectedVersion` addresses the exact mutable local record named by the operation, including nested enrichment/governance. `expectedSourceRevisionId` is a local observed-evidence precondition, never an AWS conditional-write guarantee. `maxResults` is 1–100, default 20; `nextToken` is an opaque authorization-bound snapshot cursor. No JSON body accepts the acting user, role or workspace ID.", "",
              "In the field tables, **required** members are marked with `*`. Every operation-specific response schema is a closed local validation snapshot; this does not require clients to reject future optional response members. Empty/null/missing/unknown remain distinct. A getter returns a retained record, not an implicit new provider read.", ""]
    for module, operations in grouped.items():
        lines += ["## " + module, ""]
        for op in operations:
            name = op["name"]
            req = DEFS[name + "Request"]
            resp = DEFS[name + "Response"]
            lines += ["### " + name, "",
                      f"`{op['kind']}` · permission `{op['permission']}` · implementation gate `{op['deliveryPhase']}`", "",
                      "| Request member | Type |", "| --- | --- |"]
            if not req["properties"]:
                lines.append("| Empty body | Send `{}` |")
            else:
                for key, shape in req["properties"].items():
                    required = " *" if key in req["required"] else ""
                    lines.append(f"| `{key}`{required} | `{describe_type(shape)}` |")
            lines += ["", "**Response:** " + "; ".join(f"`{key}{'?' if key not in resp['required'] else ''}: {describe_type(shape)}`" for key, shape in resp["properties"].items()) + ".", ""]
            if op["nativeOperations"]:
                lines += ["**Native adapter basis:** " + ", ".join("`" + x + "`" for x in op["nativeOperations"]) + ". These are mapped operations, not identical wire payloads.", ""]
            lines += ["- " + note for note in op["semantics"]]
            lines += ["", "**Errors:** " + ", ".join("`" + e + "`" for e in op["errors"]) + ".", ""]
    lines += ["## Entity coverage", "", "Every canonical entity is returned by a named getter or scoped full-record list. Owned values are returned by their owner; no artificial CRUD lifecycle is introduced.", "",
              "| Entity | Read operations |", "| --- | --- |"]
    for entity, ops in catalog["entityCoverage"].items():
        reads = [name for name in ops if next(o for o in OPS if o["name"] == name)["kind"] == "READ"]
        lines.append("| `" + entity + "` | " + ", ".join("`" + x + "`" for x in reads) + " |")
    lines += ["", "## Prior operation migration", "",
              "This table accounts for every operation in the prior 44-operation Resilience facade and 16-operation generalized workflow proposal. Preserving a model does not silently redefine a native command as a local metadata write. Changes of scope, transport or supported fields are explicit.", "",
              "| Source | Prior operation | Consolidated operation(s) | Disposition and meaning |", "| --- | --- | --- | --- |"]
    for entry in catalog["predecessorMappings"]:
        source = "Resilience" if "resilience-hub" in entry["sourcePackage"] else "Workflow"
        targets = ", ".join("`" + name + "`" for name in entry["newOperations"]) or "Deferred"
        lines.append(f"| {source} | `{entry['sourceOperation']}` | {targets} | `{entry['disposition']}`. {entry['notes']} |")
    lines += ["", "## Deliberately deferred command families", "",
              "The previous service packages remain the detailed native API references. This first consolidation defines a narrow provider mutation surface; the rest remain typed source profiles and explicit later adapter work:", "",
              "| Family | Retained now | Later command work |", "| --- | --- | --- |",
              "| Resilience provider systems/journeys/services/policies | Native source revisions, verified canonical bindings and selected configuration commands | Native creates/deletes, association replacement/detachment, permission/report/input-source configuration and destructive clears |",
              "| FIS templates/catalog/resource types/safety lever | Typed source profiles; experiment reads and whole-experiment stop | Template CRUD and scope-wide safety-lever mutation after dedicated authorization and adapter semantics |",
              "| DevOps registration/association/webhook/goal/recommendation/trigger/operator/private connection | Typed source DTOs and their exact scopes through SourceRevision reads | Provider management commands; no native recommendation is conflated with Resilience recommendation identity |",
              "| Asset byte access | Versioned artifact references and read authorization boundary | Expiring artifact download/upload grants and binary transport, with independent content access |",
              "| Workflow execution | Published program, admission, cancellation and owned execution read contracts | Durable dispatch, recovery, retries, leases, fences, source coverage and cloud adapters |",
              "| Retention/deletion | Immutable evidence identity and unavailable/tombstone semantics | Retention policy execution and explicitly guarded destructive commands |", "",
              "These are delivery boundaries, not discarded models. [MAPPING.md](../MAPPING.md) and [adapter-profiles.json](../model/adapter-profiles.json) retain every reviewed source concept and native family.", ""]
    return "\n".join(lines)


def build(with_examples=True):
    if with_examples:
        data = json.loads((ROOT / "model/examples.json").read_text())
        RECORDS.update(data["records"])
    add_foundation(); add_workload(); add_health(); add_resilience(); add_investigation(); add_workflow(); add_fis()
    entity_names = MODEL["x-entities"]
    if entity_names and isinstance(entity_names[0], dict):
        entity_names = [x["name"] for x in entity_names]
    coverage = {name: [op["name"] for op in OPS if name in op["entities"]] for name in entity_names}
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": SCHEMA_ID,
              "title": "Consolidated operations console RPC contracts", "description": "Design-only operation input/output and error schemas; all model references resolve offline to ../model/schema.json.",
              "$defs": DEFS}
    catalog = {"apiVersion": "2026-11-05", "namespace": NAMESPACE, "maturity": "CONTRACT_ONLY", "operationCount": len(OPS),
               "transport": {"method": "POST", "path": "/", "contentType": "application/x-amz-json-1.1", "targetHeader": "X-Amz-Target", "successStatus": 200},
               "limits": {"requestBytes": 1048576, "responseBytes": 8388608, "defaultMaxResults": 20, "maxResults": 100, "cursorTtlSeconds": 900},
               "schema": "rpc.schema.json", "modelSchema": "../model/schema.json", "operations": OPS, "entityCoverage": coverage,
               "predecessorMappings": predecessor_mappings(),
               "errors": {k: {"status": v[0], "retryable": v[1], "description": v[2]} for k, v in ERRORS.items()}}
    outputs = {"rpc.schema.json": schema, "operations.json": catalog, "OPERATIONS.md": generate_docs(catalog)}
    if with_examples:
        examples = []
        for op in OPS:
            request = SAMPLES[op["name"]]["request"]()
            response = create_response(op, request)
            examples.append({"operation": op["name"], "request": request, "response": response})
        errors = [
            {"name": "stale-local-configuration", "operation": "UpdateService", "status": 409,
             "response": {"__type": "VersionConflictException", "code": "EXPECTED_VERSION_MISMATCH", "message": "The service configuration changed; read it before issuing a new intent.", "requestId": "req-stale-demo", "retryable": False}},
            {"name": "expired-snapshot-cursor", "operation": "ListFindings", "status": 410,
             "response": {"__type": "PaginationTokenExpiredException", "code": "CURSOR_EXPIRED", "message": "Begin a new explicit list traversal.", "requestId": "req-expired-demo", "retryable": False}},
            {"name": "token-payload-conflict", "operation": "StartRun", "status": 409,
             "response": {"__type": "IdempotencyConflictException", "code": "TOKEN_INTENT_MISMATCH", "message": "The token already identifies a different request.", "requestId": "req-token-demo", "retryable": False}},
        ]
        outputs["examples.json"] = {"schemaVersion": "consolidated-rpc-examples/1", "synthetic": True,
                                    "notice": "Independent schema-valid design examples assembled from the canonical synthetic dataset. No operation was invoked; receipts and outcomes are illustrative.",
                                    "examples": examples, "errors": errors}
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare generated text without writing files")
    parser.add_argument("--without-examples", action="store_true", help="Author schema/catalog before model fixtures exist")
    args = parser.parse_args()
    outputs = build(not args.without_examples)
    mismatch = []
    for name, content in outputs.items():
        encoded = content if isinstance(content, str) else json.dumps(content, indent=2, ensure_ascii=False) + "\n"
        path = HERE / name
        if args.check:
            if not path.exists() or path.read_text() != encoded:
                mismatch.append(name)
        else:
            path.write_text(encoded)
    if mismatch:
        raise SystemExit("Generated API files differ: " + ", ".join(mismatch))
    print(json.dumps({"operationCount": len(OPS), "files": list(outputs), "mode": "check" if args.check else "generate"}))


if __name__ == "__main__":
    main()
