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
SCHEMA_ID = "https://schemas.frontier-agents.example/consolidated-operations-console/2026-11-05/v2/rpc.json"
NAMESPACE = "ConsolidatedOperationsConsole_20261105V2"
NOW = 1793872800
V1_OPERATION_NAMES = ['GetWorkspace', 'GetConnection', 'ListConnections', 'CreateConnection', 'UpdateConnection', 'GetResource', 'ListResources', 'GetCollection', 'ListCollections', 'ListReadAttempts', 'GetSourceRevision', 'GetObservation', 'GetProjectionRevision', 'GetSnapshot', 'GetWorkItem', 'GetCommand', 'ListSourceRevisions', 'ListObservations', 'ListProjectionRevisions', 'ListSnapshots', 'ListWorkItems', 'ListCommands', 'StartCollection', 'RecordReadAttempt', 'IngestObservation', 'CompleteCollection', 'PublishProjection', 'CaptureSnapshot', 'CreateWorkItem', 'UpdateWorkItem', 'RecordWorkItemVerification', 'CreateSystem', 'GetSystem', 'ListSystems', 'UpdateSystem', 'CreateUserJourney', 'GetUserJourney', 'ListUserJourneys', 'UpdateUserJourney', 'CreateService', 'GetService', 'ListServices', 'UpdateService', 'GetServiceStatus', 'GetWorkspaceSummary', 'GetDependency', 'ListDependencies', 'UpdateDependencyGovernance', 'GetHealthEvent', 'ListHealthEvents', 'ListEventContexts', 'ListEntityImpacts', 'ListCommunications', 'ListLifecycleEntries', 'GetComponentDeployment', 'ListComponentDeployments', 'GetResiliencePolicy', 'ListResiliencePolicies', 'GetResilienceAssessment', 'ListResilienceAssessments', 'GetFinding', 'ListFindings', 'GetRecommendation', 'ListRecommendations', 'StartResilienceAssessment', 'UpdateFindingDisposition', 'UpdateDependencyClassification', 'UpdateResiliencePolicyConfiguration', 'UpdateResilienceServiceConfiguration', 'UpdateRecommendationEnrichment', 'GetAgentSpace', 'ListAgentSpaces', 'GetInvestigation', 'ListInvestigations', 'GetExecution', 'ListExecutions', 'GetJournalRecord', 'ListJournalRecords', 'GetApprovalRequest', 'ListApprovalRequests', 'GetAsset', 'ListAssets', 'StartInvestigation', 'DecideApproval', 'ResumeExecution', 'CreateScenario', 'GetScenario', 'ListScenarios', 'UpdateScenario', 'PublishScenarioRevision', 'GetScenarioRevision', 'ListScenarioRevisions', 'StartRun', 'GetRun', 'ListRuns', 'RequestRunCancellation', 'ListRunSteps', 'ListStepAttempts', 'GetExperiment', 'ListExperiments', 'StopExperiment']
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
    # First choose one logical identity; a getter without a version selects only
    # that identity's current head, never a different object with a high version.
    identity = rows[0][idfield(name)]
    rows = [row for row in rows if row[idfield(name)] == identity]
    return copy.deepcopy(max(rows, key=lambda row: row["version"]))


def historical_record(name):
    grouped = defaultdict(list)
    for row in RECORDS[name]:
        grouped[row[idfield(name)]].append(row)
    versions = next((rows for rows in grouped.values() if len(rows) > 1), next(iter(grouped.values())))
    return copy.deepcopy(min(versions, key=lambda row: row["version"]))


def resolve(ref):
    """Resolve an exact retained representation; never substitute the head."""
    return record(ref["kind"], **{idfield(ref["kind"]): ref["id"], "version": ref["version"]})


def source_for(entity):
    row = record(entity)
    for key in ("selectedSource", "source", "requestSource"):
        if row.get(key):
            return copy.deepcopy(row[key])
    for key in ("selectedDetailObservation", "selectedObservation", "selectedTaskObservation", "selectedSummaryObservation"):
        if row.get(key):
            return resolve(row[key])["source"]
    if row.get("providerBindings"):
        return copy.deepcopy(row["providerBindings"][0]["source"])
    raise ValueError(f"No source precondition can be resolved for {entity}")


def eref(name, row=None, **selector):
    row = row or record(name, **selector)
    return {"kind": name, "id": row[idfield(name)], "version": row["version"]}


def identity(name):
    return {"kind": name, "id": identifier(name)}


def exact_ref(name):
    return {"allOf": [model("EntityRef"), {"properties": {"kind": {"const": name}}}]}


def scoped_ids(entity, row, parents, include_entity=True):
    """Select the actual owning chain; unrelated first parent rows are invalid."""
    values = {idfield(entity): row[idfield(entity)]} if include_entity else {}
    current = row
    for parent in reversed(parents):
        key = idfield(parent)
        if key not in current:
            raise ValueError(f"Cannot resolve {entity} ownership through {parent}")
        values[key] = current[key]
        current = record(parent, **{key: current[key]})
    return values


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
    "totalResults": {**integer(0), "description": "Optional exact cardinality of the authorized, filtered result set for this retained traversal publication. Omit when not computed; zero requires an established empty result set. It is not current-page length or upstream AWS coverage."},
}, ["traversalId", "asOfSequence", "createdAt", "expiresAt"],
    description="Response-owned traversal metadata. A supplied totalResults is stable across pages of the same authorization/filter/publication scope; omitted means unknown. It does not create an entity or make pagination exhaustion proof of upstream completeness.")
DEFS["FieldViolation"] = obj({"path": string(1, 1024), "code": string(1, 128), "message": string(1, 2048)})
ERRORS = {
    "ValidationException": (400, False, "Invalid syntax, field, union, scalar or semantic input; no accepted mutation."),
    "UnauthenticatedException": (401, False, "No verified caller identity."),
    "AccessDeniedException": (403, False, "Caller or connection lacks permission for the complete subject/evidence scope."),
    "ResourceNotFoundException": (404, False, "Identity is absent or invisible in its trusted workspace and required parent scope."),
    "VersionConflictException": (409, False, "The named entity head no longer has expectedVersion; no mutation was admitted."),
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
    if any(key.startswith("expected") and key.endswith("Version") for key in request["properties"]) or name == "StartRun":
        error_names.append("VersionConflictException")
    if kind == "READ" or any(x in entities for x in ("Source", "Snapshot", "Observation", "Asset")):
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
        "scopeFields": [k for k in request["properties"] if k.endswith("Id") or k in
                        ("entity", "subject", "subjectRefs", "members", "source", "expectedSource", "expectedRequestSource",
                         "connection", "scenario", "approvalRequest", "decisionCommand", "bindings")],
    })
    SAMPLES[name] = {"request": sample, "responseSelector": response_selector or {}}


def get(name, entity, module, parents=(), permission="console:Read", semantics=()):
    fields = {idfield(x): ID for x in (*parents, entity)}
    required = list(fields)
    fields["version"] = VERSION
    add(name, module, "READ", permission, [entity], obj(fields, required), obj({lower(entity): model(entity)}),
        lambda: {**scoped_ids(entity, record(entity), parents), "version": record(entity)["version"]},
        ["Returns retained canonical data with its provenance; does not fetch AWS synchronously.",
         "An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.",
         "Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.", *semantics])


def listing(name, entity, module, parents=(), filters=None, permission="console:Read", semantics=(), sample_filters=None):
    fields = {idfield(x): ID for x in parents}
    fields.update(filters or {})
    fields.update(PAGE)
    add(name, module, "READ", permission, [entity], obj(fields, [idfield(x) for x in parents]),
        obj({"items": array(model(entity), maximum=100), "page": local("Page"), "nextToken": string(1, 4096)}, ["items", "page"]),
        lambda: {**scoped_ids(entity, record(entity), parents, include_entity=False), **(sample_filters or {}), "maxResults": 20},
        ["Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.",
         "Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.",
         "A completed local traversal does not establish complete upstream collection or claim coverage.", *semantics])


def owned_listing(name, entity, module, parent, member_field, parents=(), semantics=()):
    version_field = lower(parent) + "Version"
    ids = {idfield(x): ID for x in (*parents, parent)}
    add(name, module, "READ", "console:Read", [entity, parent],
        obj({**ids, version_field: VERSION, **PAGE}, list(ids)),
        obj({"parent": exact_ref(parent), "items": array(model(entity), maximum=100),
             "page": local("Page"), "nextToken": string(1, 4096)}, ["parent", "items", "page"]),
        lambda: {**{idfield(x): identifier(x) for x in (*parents, parent)},
                 version_field: record(parent)["version"], "maxResults": 20},
        [f"Selects the exact {parent} version when {version_field} is supplied; otherwise selects its current head once. The response identifies that selected parent.",
         f"Returns the exact {entity} versions named in {parent}.{member_field}, never current child heads or a timestamp-based reconstruction. A missing referenced version fails the read.",
         "Pagination binds the selected parent version and its immutable member set. Current authorization applies to parent and every returned child.", *semantics])
    SAMPLES[name]["ownedParent"] = {"entity": parent, "field": member_field, "versionField": version_field}


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
    add("GetWorkspace", "foundation", "READ", "console:ReadWorkspace", ["Workspace"], obj({"version": VERSION}, []),
        obj({"workspace": model("Workspace")}), lambda: {},
        ["Workspace comes exclusively from authenticated context; the request cannot select a tenant.",
         "version selects an exact immutable representation. Omission selects the current head; current authorization is always enforced, including historical reads."])
    add("ListEntityVersions", "foundation", "READ", "console:ReadHistory", list(MODEL["x-entities"]),
        obj({"entity": model("EntityIdentity"), **PAGE}, ["entity"]),
        obj({"items": array(model("EntityRef"), maximum=100), "page": local("Page"), "nextToken": string(1, 4096)}, ["items", "page"]),
        lambda: {"entity": identity("Service"), "maxResults": 20},
        ["Enumerates immutable exact references for one logical entity, ordered by descending version in a fixed traversal. References are values, not separately managed Version resources.",
         "Resolve each reference with that entity's Get operation and the returned version. Historical versions are never silently replaced by current heads.",
         "The current caller must hold both history capability and the entity's normal domain-read permission; each returned version must authorize its full retained closure.",
         "A Workspace identity must equal the already authenticated workspace. This operation cannot select another tenant or bypass domain parent/scope checks.",
         "The cursor binds entity kind/id, authenticated scope and the traversal's retained version set. It exposes no hidden version count."])
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
    get("GetReadAttempt", "ReadAttempt", "foundation", parents=("Collection",))
    listing("ListReadAttempts", "ReadAttempt", "foundation", parents=("Collection",),
            semantics=["Includes failed and empty reads; their absence from returned object rows must not erase collection evidence."])
    for entity in ("Source", "Observation", "Projection", "Snapshot", "WorkItem", "Command"):
        get("Get" + entity, entity, "foundation")
    SAMPLES["GetSource"]["request"] = lambda: {"sourceId": historical_record("Source")["sourceId"], "version": historical_record("Source")["version"]}
    listing("ListSources", "Source", "foundation", filters={
        "identity": model("SourceIdentity"), "profile": string(1, 256), "representation": MODEL["$defs"]["Source"]["properties"]["representation"]},
        semantics=["Native peripheral resources are retained typed profiles, including FIS templates/catalogs and DevOps registrations/triggers/goals.",
                   "Representation and source identity are explicit; matching hashes do not merge different logical source records."])
    listing("ListObservations", "Observation", "foundation", filters={"source": exact_ref("Source"), "collectionId": ID, "subject": model("EntityRef")})
    listing("ListProjections", "Projection", "foundation", filters={
        "subject": model("EntityRef"), "profile": MODEL["$defs"]["Projection"]["properties"]["profile"]},
        semantics=["Returns current Projection heads. Each logical projection has ordinary entity versions; exact prior derivations remain readable without a ProjectionRevision entity."])
    listing("ListSnapshots", "Snapshot", "foundation", filters={"subject": model("EntityRef"), "kind": MODEL["$defs"]["Snapshot"]["properties"]["kind"]})
    listing("ListWorkItems", "WorkItem", "foundation", filters={"target": model("EntityIdentity"), "state": MODEL["$defs"]["WorkItem"]["properties"]["state"]})
    listing("ListCommands", "Command", "foundation", filters={"subject": model("EntityRef"), "operation": string(1, 128), "state": MODEL["$defs"]["Command"]["properties"]["state"]})

    # Collectors may invoke registered read contracts, never arbitrary URLs, code or cloud mutations.
    fields = {"connection": exact_ref("Connection"), "queries": array(model("CollectionQuery"), 1, 100), **MUT}
    add("StartCollection", "foundation", "INGEST", "console:Collect", ["Collection", "Command"],
        obj(fields), command_response("Collection"),
        lambda: {"connection": eref("Connection"), "queries": record("Collection")["queries"],
                 "clientToken": "start-collection-demo-0001"},
        ["Admits a finite exact query set from the registered read-only adapter catalog; unknown operations or unauthorized scope fail admission.",
         "queryKey uniqueness, canonical requestDigest, filter types and operation-specific bounds are validated against that registered adapter.",
         "Completion, pagination, hydration, resolution and claim coverage remain independent facts.",
         "Trusted collection admission records exact collector and selectionPolicy implementation identities on the Collection; caller input cannot forge these processing identities."])
    attempt_fields = properties_of("ReadAttempt", ["collectionId", "readAttemptId", "state", "endedAt", "providerRequestId", "returnedCount", "nextTokenPresent", "error", "requestSource", "responseSource"])
    # Optional item outcomes retain failedSet without changing legacy settlement inputs.
    attempt_required = list(attempt_fields) + list(GUARDED)
    attempt_fields.update(properties_of("ReadAttempt", ["itemErrors", "itemOutcome"]))
    attempt_fields["state"] = enum("SUCCEEDED", "FAILED")
    attempt_fields["endedAt"] = TIME
    attempt_fields.update(GUARDED)
    add("RecordReadAttempt", "foundation", "INGEST", "console:IngestEvidence", ["ReadAttempt", "Command"],
        obj(attempt_fields, attempt_required, allOf=[
            {"if": {"properties": {"state": {"const": "SUCCEEDED"}}}, "then": {"properties": {"error": {"type": "null"}}}},
            {"if": {"properties": {"state": {"const": "FAILED"}}}, "then": {"properties": {"error": model("ReadError")}}},
        ] + model_shape(MODEL["$defs"]["ReadAttempt"].get("allOf", [])),
            dependentRequired=copy.deepcopy(MODEL["$defs"]["ReadAttempt"].get("dependentRequired", {}))), command_response("ReadAttempt"),
        lambda: {**{k: record("ReadAttempt")[k] for k in attempt_fields if k not in ("clientToken", "expectedVersion") and k in record("ReadAttempt")},
                 "expectedVersion": max(1, record("ReadAttempt")["version"] - 1), "clientToken": "record-read-attempt-demo-0001"},
        ["Settles the same existing STARTED ReadAttempt created by the trusted collector dispatch transaction before the actual read; does not append a second attempt or fabricate a pre-call record after the fact.",
         "Trusted context assigns authorizationContextKey; a caller cannot forge its acting principal or provenance.",
         "expectedVersion guards the existing STARTED ReadAttempt head. Settlement creates the next version of that same identity; prior STARTED representations remain intact.",
         "requestSource must equal the exact already retained request envelope for this attempt. Response references must belong to this exact request and scope, including empty responses.",
         "IngestObservation may retain response/object observations while the attempt is STARTED; settlement then references those revisions. A response-lost failure has an explicit null response reference, not a fabricated empty response.",
         "A settled attempt is immutable. Exact replay returns the original result; conflicting terminal facts reject. Query identity, attemptNo, requestDigest, startedAt and authorization provenance are server-owned.",
         "Optional itemErrors and itemOutcome preserve event/account failedSet entries. A successful HTTP response can have PARTIAL or FAILED item outcome while transport state remains SUCCEEDED; transport failures remain error. Omitting these fields means item outcome was not recorded, never complete success."])
    # Source identity/version metadata remains server-owned; optional typed views are writable only through trusted ingestion.
    source_server_fields = {"sourceId", "workspaceId", "version", "createdAt", "updatedAt"}
    source_fields = properties_of("Source", [name for name in MODEL["$defs"]["Source"]["properties"] if name not in source_server_fields])
    source_required = [name for name in MODEL["$defs"]["Source"]["required"] if name in source_fields]
    DEFS["SourceInput"] = obj(source_fields, source_required,
        allOf=model_shape(MODEL["$defs"]["Source"].get("allOf", [])),
        dependentRequired=copy.deepcopy(MODEL["$defs"]["Source"].get("dependentRequired", {})))
    observation_fields = properties_of("Observation", ["channel", "readAttempt", "connection", "observedAt", "sourceTime", "transportTime", "expiresAt", "receiptKey"])
    observation_fields.update({"source": local("SourceInput"), **MUT})
    add("IngestObservation", "foundation", "INGEST", "console:IngestEvidence", ["Source", "Observation", "Command"],
        obj(observation_fields, allOf=model_shape(MODEL["$defs"]["Observation"].get("allOf", []))), obj({"source": model("Source"), "observation": model("Observation"), "command": model("Command")}),
        lambda: {**{k: record("Observation")[k] for k in observation_fields if k not in ("source", "clientToken")},
                 "source": {k: resolve(record("Observation")["source"])[k] for k in source_fields if k in resolve(record("Observation")["source"])}, "clientToken": "ingest-observation-demo-0001"},
        ["Atomically resolves the stable Source identity independently of content digest, retains a new Source version when its accepted representation changes, and records a distinct Observation with an exact Source reference.",
         "An unchanged consecutive receipt reuses the current Source version only when raw content, optional normalized views and their rule provenance all agree. Changed normalization appends a version even with the same raw contentDigest. A→B→A publishes versions 1→2→3; byte deduplication cannot relabel the last observation as the old version 1.",
         "The registered versioned profile validates typed known members, source identity, representation and digest; raw unknown provider output remains retained evidence.",
         "payload is the intentionally opaque provider document, bounded by the body cap and adapter schema; it cannot patch canonical state or set a verdict.",
         "Optional normalized Source fields require their registered profile and normalization input/rule provenance. contentDigest remains the raw payload/artifact digest; inputContentDigest must agree with it. Unknown native content remains retained in payload and must not be rejected solely because it cannot populate a normalized view. Existing records without those optional fields are not claimed to be normalized.",
         "The adapter reconciles canonical entity indexes through verified mappings. Digest equality alone is not event identity; receipt dedupe includes the authenticated channel/scope."])
    add("CompleteCollection", "foundation", "INGEST", "console:IngestEvidence", ["Collection", "Command"],
        obj({"collectionId": ID, "coverage": array(model("Coverage"), 1, 100), **GUARDED}),
        command_response("Collection"),
        lambda: {"collectionId": identifier("Collection"), "expectedVersion": max(1, record("Collection")["version"] - 1),
                 "coverage": record("Collection")["coverage"], "clientToken": "complete-collection-demo-0001"},
        ["Seals collection coverage after every declared query has a settled or explicitly unresolved outcome; referenced attempts must belong to this collection.",
         "A coverage conclusion must be justified by registered collector rules. Successful or exhausted pages cannot alone claim source sufficiency.",
         "New coverage conclusions record the exact evaluationPolicy identity. Historical absence remains unknown; it cannot be assigned the current policy retroactively.",
         "expectedVersion guards the Collection head; completion publishes its next ordinary entity version. There is no second projectionVersion clock."])
    projection_input = properties_of("Projection", ["projectionKey", "profile", "profileVersion", "subjectRefs", "inputRefs", "ruleDigest", "asOf"])
    projection_input.update({"expectedVersion": nullable(VERSION), **MUT})
    add("PublishProjection", "foundation", "DERIVE", "console:PublishProjection", ["Projection", "Command"],
        obj(projection_input), command_response("Projection"),
        lambda: {**{k: record("Projection", profile="SERVICE_STATUS")[k] for k in projection_input if k not in ("clientToken", "expectedVersion")},
                 "expectedVersion": record("Projection", profile="SERVICE_STATUS")["version"], "clientToken": "publish-projection-demo-0001"},
        ["Executes an authorized registered rule over exact entity-version inputs and publishes the next version of the same logical Projection.",
         "expectedVersion=null requires that the named projection identity does not exist; a positive value guards its current head. The first publication is version 1. Concurrent incompatible publication returns VersionConflictException.",
         "The request cannot supply value, generatedAt, coverage or a desired verdict. The trusted projector derives them from the selected evidence.",
         "INVESTIGATION_TIMELINE and INVESTIGATION_ASSERTIONS use their typed value contracts. The trusted projector records DerivationContext and outputDigest; every source citation is among inputRefs. Published claims preserve attribution and do not expose private model reasoning.",
         "Every reference must be authorized, same-workspace and available. Missing evidence produces a qualified result or explicit failure; it never becomes success.",
         "A new projection version does not change its source subjects or any earlier entity representation. Current-view selection never rewrites a sealed Run."],
        response_selector={"Projection": {"profile": "SERVICE_STATUS"}})
    capture_input = {"kind": MODEL["$defs"]["Snapshot"]["properties"]["kind"], "subjectRefs": array(model("EntityRef"), 1, 100),
                     "members": array(model("EntityRef"), 1, 1000, True), **MUT}
    # Run admission is an internal atomic StartRun effect, not a user-editable snapshot.
    capture_input["kind"] = enum("INVESTIGATION", "TOPOLOGY", "POLICY_CONTEXT", "LIFECYCLE_CATALOG", "EVALUATION_INPUT")
    add("CaptureSnapshot", "foundation", "LOCAL_COMMAND", "console:CaptureEvidence", ["Snapshot", "Command"],
        obj(capture_input), command_response("Snapshot"),
        lambda: {"kind": "TOPOLOGY", **{k: record("Snapshot", kind="TOPOLOGY")[k] for k in ("subjectRefs", "members")},
                 "clientToken": "capture-snapshot-demo-0001"},
        ["Builds a closed immutable manifest and typed contents from existing retained evidence, including failed/empty read attempts and coverage.",
         "All selected subjects and members use exact (kind,id,version) references. The server closes the authorized retained reference graph without resolving any member to latest; unavailable versions reject capture.",
         "The manifest does not consult mutable current fields after capture. capturedAt does not renew source timestamps or make paginated AWS reads atomic.",
         "RUN_INPUT snapshots are created only during StartRun admission; clients cannot replace a Run's inputs by creating a similarly named snapshot."],
        response_selector={"Snapshot": {"kind": "TOPOLOGY"}})

    add("CreateWorkItem", "foundation", "LOCAL_COMMAND", "console:ManageWork", ["WorkItem", "Command"],
        obj({"title": string(1, 256), "targets": array(model("EntityIdentity"), 1, 100), "priority": enum("CRITICAL", "HIGH", "MEDIUM", "LOW"), "dueAt": TIME, "assigneeSubjectId": ID, **MUT}, ["title", "targets", "clientToken"]), command_response("WorkItem"),
        lambda: {"title": "Review checkout resilience evidence", "targets": [identity("Service"), identity("Finding")], "clientToken": "create-work-item-demo-0001"},
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
                 "note": "Reviewed the retained evidence; the provider outcome remains unverified.", "clientToken": "update-work-item-demo-0001"},
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
             "Membership inputs contain only local system/journey IDs; the server stamps origin=LOCAL and source=null. Imported provenance is reserved to the trusted importer."])
        get("Get" + entity, entity, "workload", parents=parents)
        if entity == "Service":
            SAMPLES["GetService"]["request"] = lambda: {"serviceId": historical_record("Service")["serviceId"], "version": historical_record("Service")["version"]}
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
            ["Updates the named entity under its one expectedVersion and publishes the next immutable representation, including owned values. There is no separate configuration or overlay clock.",
             "Changes to separate Source, Observation or Projection identities do not change this entity. A material change to its own fields or verified bindings does advance its version.",
             "Omitted fields are unchanged; an empty description is a known empty value; supplied arrays replace their complete owned membership set.",
             "Service is the sole membership writer. Every journey must belong to its paired system; a journey update cannot set a second service list."])
    add("GetServiceStatus", "workload", "READ", "console:Read", ["Projection"], obj({"serviceId": ID}),
        obj({"projection": {"allOf": [model("Projection"), {"properties": {"profile": {"const": "SERVICE_STATUS"}}}]}}),
        lambda: {"serviceId": identifier("Service")},
        ["Returns the currently selected SERVICE_STATUS projection under its named rule, including evidence/freshness/coverage. Clients do not infer current state from newest receipt time.",
         "No current selected projection returns ResourceNotFoundException with code PROJECTION_NOT_AVAILABLE, never an invented healthy/default object.",
         "Runtime health, native assessed posture, collection quality and operator workflow remain distinct dimensions."],
        response_selector={"Projection": {"profile": "SERVICE_STATUS"}})
    add("GetWorkspaceSummary", "workload", "READ", "console:ReadWorkspace", ["Projection"], obj({}),
        obj({"projection": {"allOf": [model("Projection"), {"properties": {"profile": {"const": "WORKSPACE_SUMMARY"}}}]}}),
        lambda: {},
        ["Returns the current qualified WORKSPACE_SUMMARY for the trusted caller's authorized workload scope, including exact distinct contributor identities, denominator and rule.",
         "An empty authorized scope has null percentages. Retained historical evidence is separate from current usable coverage; no end-to-end journey compliance is inferred.",
         "A cached broader summary must be recomputed/selected for the authorized scope; hidden records cannot leak through counts."],
        response_selector={"Projection": {"profile": "WORKSPACE_SUMMARY"}})
    get("GetDependency", "Dependency", "workload", parents=("Service",))
    listing("ListDependencies", "Dependency", "workload", parents=("Service",))
    fields = {"serviceId": ID, "dependencyId": ID, "decision": enum("ALLOWED", "REVIEW", "DENIED"), "reason": string(1, 4096), **GUARDED}
    add("UpdateDependencyGovernance", "workload", "LOCAL_COMMAND", "console:ManageGovernance", ["Dependency", "Command"],
        obj(fields), command_response("Dependency"),
        lambda: {"serviceId": identifier("Service"), "dependencyId": identifier("Dependency"), "expectedVersion": record("Dependency")["version"],
                 "decision": "REVIEW", "reason": "Review the observed external dependency.", "clientToken": "governance-demo-0001"},
        ["expectedVersion addresses Dependency.version. The governance value has no independent version or CRUD lifecycle; changing it publishes the next Dependency representation.",
         "An allowed/denied decision is local governance. It neither changes DNS evidence nor grants/revokes network access."])


def add_health():
    get("GetHealthEvent", "HealthEvent", "health")
    listing("ListHealthEvents", "HealthEvent", "health", filters={"serviceCode": string(1, 128), "eventTypeCode": string(1, 256)})
    get("GetEventContext", "EventContext", "health", parents=("HealthEvent",))
    listing("ListEventContexts", "EventContext", "health", parents=("HealthEvent",), filters={"kind": enum("PUBLIC", "ACCOUNT", "ORG_SUMMARY")})
    get("GetEntityImpact", "EntityImpact", "health", parents=("HealthEvent", "EventContext"))
    listing("ListEntityImpacts", "EntityImpact", "health", parents=("HealthEvent", "EventContext"),
            semantics=["Account/public/organization-summary evidence never leaks between contexts. Counts remain qualified by collection coverage."])
    get("GetCommunication", "Communication", "health", parents=("HealthEvent", "EventContext"))
    listing("ListCommunications", "Communication", "health", parents=("HealthEvent", "EventContext"),
            semantics=["Conflicting and partial notification pages remain visible; delivery recipients do not redefine impacted account identity."])
    get("GetLifecycleEntry", "LifecycleEntry", "health")
    listing("ListLifecycleEntries", "LifecycleEntry", "health", filters={"catalogSnapshot": exact_ref("Snapshot"), "serviceCode": string(1, 128)},
            semantics=["catalogSnapshot, when supplied, is an exact LIFECYCLE_CATALOG capture. Entries are selected through that retained manifest, never through a later snapshot head; titles do not establish identity."])
    SAMPLES["ListLifecycleEntries"]["request"] = lambda: {"catalogSnapshot": eref("Snapshot", **{"kind": "LIFECYCLE_CATALOG"}), "maxResults": 20}
    get("GetComponentDeployment", "ComponentDeployment", "health", parents=("Resource",))
    listing("ListComponentDeployments", "ComponentDeployment", "health", parents=("Resource",),
            semantics=["Lifecycle exposure is a separate versioned projection using these observed component versions and a pinned lifecycle catalog."])


def native_fields(entity, parents=()):
    return {**{idfield(x): ID for x in (*parents, entity)}, "connection": exact_ref("Connection"), "expectedSource": exact_ref("Source"), **GUARDED}


def native_sample(name, entity, parents=(), **extra):
    return lambda: {**scoped_ids(entity, record(entity), parents), "connection": eref("Connection"),
                    "expectedVersion": record(entity)["version"], "expectedSource": source_for(entity), "clientToken": name.lower() + "-demo-0001", **extra}


NATIVE_NOTES = [
    "Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.",
    "expectedVersion guards the named entity head. expectedSource pins the exact source evidence for the native precondition; neither creates an AWS compare-and-swap guarantee.",
    "The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.",
    "The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's version or a stale unrelated summary is rejected even in the same workspace.",
    "The exact Connection version is recorded at admission; current permissions, revocation and material provider preconditions are checked again at dispatch.",
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
    listing("ListRecommendations", "Recommendation", "resilience", parents=("Service", "Finding"), filters={"source": exact_ref("Source")},
            semantics=["When no stable provider key exists, identity uses finding + exact Source version + group/ordinal. Repeated receipt observations of that same content do not create another recommendation; equal text alone cannot establish continuity across changed source versions."])
    add("StartResilienceAssessment", "resilience", "PROVIDER_COMMAND", "console:RunResilienceAssessment", ["Command", "ResilienceAssessment"],
        obj({"serviceId": ID, "connection": exact_ref("Connection"), **GUARDED}), command_response(),
        lambda: {"serviceId": identifier("Service"), "connection": eref("Connection"), "expectedVersion": record("Service")["version"], "clientToken": "start-resilience-demo-0001"},
        ["Pins the local Service version and Connection at admission, then requests native StartFailureModeAssessment. expectedVersion is a Service precondition, not an AWS conditional-write token.",
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
        [*NATIVE_NOTES, "Native criticality/comment and local allowed/denied governance have distinct commands and field authority; both materialize through ordinary versions of Dependency."], native=("UpdateDependency",))
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
              "estimate": model("RecommendationEstimate"), "note": TEXT,
              "clearFields": clear_fields("title", "effort", "estimate"), **GUARDED}
    add("UpdateRecommendationEnrichment", "resilience", "LOCAL_COMMAND", "console:ManageRecommendationMetadata", ["Recommendation", "Command"],
        obj(fields, ["serviceId", "findingId", "recommendationId", "expectedVersion", "clientToken"], anyOf=at_least_change(["title", "effort", "estimate", "note", "clearFields"])), command_response("Recommendation"),
        lambda: {"serviceId": identifier("Service"), "findingId": identifier("Finding"), "recommendationId": identifier("Recommendation"),
                 "expectedVersion": record("Recommendation")["version"], "note": "Estimate reviewed against the retained suggestion.", "clientToken": "enrich-recommendation-demo-0001"},
        ["expectedVersion refers to Recommendation.version. Enrichment is an owned value without a second version clock; the complete Recommendation receives the next version.",
         "Estimate amount/currency/basis/complexity/source/time/confidence are typed local information, separate from native assessment execution cost.",
         "Assignment, work state, completion and verification belong exclusively to a WorkItem targeting this recommendation. This operation cannot maintain a competing recommendation workflow.",
         "Local estimates do not establish provider remediation or recommendation identity across changed source versions."])


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
        obj({"agentSpaceId": ID, "connection": exact_ref("Connection"), "title": string(1, 400), "description": string(0, 10000),
             "priority": enum("CRITICAL", "HIGH", "MEDIUM", "LOW", "MINIMAL"), **GUARDED},
            ["agentSpaceId", "connection", "title", "priority", "expectedVersion", "clientToken"]), command_response(),
        lambda: {"agentSpaceId": identifier("AgentSpace"), "expectedVersion": record("AgentSpace")["version"], "connection": eref("Connection"), "title": "Investigate checkout latency", "priority": "HIGH", "clientToken": "start-investigation-demo-0001"},
        ["Requests CreateBacklogTask with taskType=INVESTIGATION; it is not a native operation named StartInvestigation.",
         "expectedVersion guards the AgentSpace head used for admission. The Connection version is pinned and current authority rechecked before dispatch.",
         "A task creation receipt does not prove execution started. Native task, execution and result observations are reconciled separately.",
         "The adapter maps the durable console intent to a stable provider token within native bounds; no raw tenant/actor is accepted."], native=("CreateBacklogTask",))
    decision = {"agentSpaceId": ID, "executionId": ID, "approvalRequestId": ID, "connection": exact_ref("Connection"),
                "expectedRequestSource": exact_ref("Source"), "expectedActionDigest": model("Digest"),
                "decision": enum("APPROVED", "REJECTED"), "singleUse": {"const": True}, "reason": string(0, 1024), **GUARDED}
    add("DecideApproval", "investigation", "PROVIDER_COMMAND", "console:DecideApproval", ["ApprovalRequest", "Command"],
        obj(decision, [k for k in decision if k not in ("reason", "singleUse")], allOf=[
            {"if": {"properties": {"decision": {"const": "APPROVED"}}}, "then": {"required": ["singleUse"]}},
            {"if": {"properties": {"decision": {"const": "REJECTED"}}}, "then": {"not": {"required": ["singleUse"]}}},
        ]), command_response(),
        lambda: {**scoped_ids("ApprovalRequest", record("ApprovalRequest"), ("AgentSpace", "Execution")),
                 "connection": eref("Connection"), "expectedVersion": record("ApprovalRequest")["version"], "expectedRequestSource": record("ApprovalRequest")["requestSource"],
                 "expectedActionDigest": record("ApprovalRequest")["actionDigest"], "decision": "REJECTED",
                 "reason": "The requested mutation is outside this investigation's intended scope.", "clientToken": "decide-approval-demo-0001"},
        ["First-release decision supports exact observed scope and single use only; reusable grants and pattern editing are explicitly deferred.",
         "expectedVersion guards ApprovalRequest; expectedRequestSource selects its exact retained request content. A version from another request or source object is rejected.",
         "APPROVED requires singleUse=true. REJECTED omits singleUse; the adapter also omits native pattern and TTL fields for rejection.",
         "Validates a complete authenticated chat request context and exact action digest, then invokes UpdateApprovalAction. It neither resumes the execution nor claims the tool ran.",
         "Admission records reconstructable Command.approvalDecision with the exact ApprovalRequest version, request Source, action digest, decision, singleUse and copied requested pattern. Only VALIDATED observed invocation context is dispatchable; missing or unsupported context is rejected.",
         "Native UpdateApprovalAction has no modeled idempotency token. A lost response is OUTCOME_UNKNOWN; local replay returns the receipt and must not repeat the remote mutation blindly.",
         "A successful rejection is a successful decision command, not a provider API failure."], native=("UpdateApprovalAction",))
    add("ResumeExecution", "investigation", "PROVIDER_COMMAND", "console:ResumeExecution", ["Execution", "ApprovalRequest", "Command"],
        obj({"agentSpaceId": ID, "executionId": ID, "approvalRequest": exact_ref("ApprovalRequest"), "decisionCommand": exact_ref("Command"), "connection": exact_ref("Connection"), **GUARDED}), command_response(),
        lambda: {**scoped_ids("ApprovalRequest", record("ApprovalRequest"), ("AgentSpace", "Execution"), include_entity=False),
                 "expectedVersion": record("Execution", executionId=record("ApprovalRequest")["executionId"])["version"], "approvalRequest": eref("ApprovalRequest"),
                 "decisionCommand": {"kind": "Command", "id": "cmd-decideapproval-demo", "version": 2}, "connection": eref("Connection"), "clientToken": "resume-execution-demo-0001"},
        ["Requires a definitively successful matching decision Command, valid current authorization and a validated approval/interrupt/tool-use context.",
         "Records Command.approvalResume with the exact request, successful decision Command, and native action identifiers. This dispatch receipt does not establish tool execution or action effect.",
         "expectedVersion guards Execution; approvalRequest and decisionCommand are exact retained representations. An ACCEPTED decision version is insufficient even if a later command version has succeeded.",
         "Constructs the native SendMessage APPROVAL_ACTION context from that retained request; the caller cannot substitute interrupt/tool IDs or widen approved scope.",
         "Decision, resume submission, credential redemption and actual tool outcome remain separate. Opening or completing a stream does not prove the tool succeeded.",
         "SendMessage has no modeled idempotency token. Persist stream fragments and unknown outcomes; do not blindly resend on disconnect."], native=("SendMessage",))


def add_workflow():
    add("CreateScenario", "workflow", "LOCAL_COMMAND", "console:AuthorScenario", ["Scenario", "Command"],
        obj({"name": string(1, 256), "description": TEXT, "definition": model("ScenarioDraft"), **MUT}, ["name", "definition", "clientToken"]), command_response("Scenario"),
        lambda: {"name": record("Scenario")["name"], "description": record("Scenario")["description"], "definition": record("Scenario", state="DRAFT")["definition"], "clientToken": "create-scenario-demo-0001"},
        ["Creates Scenario version 1 in DRAFT state. An author cannot set trusted operation locks, publication state, version, timestamps or digest."])
    get("GetScenario", "Scenario", "workflow")
    SAMPLES["GetScenario"]["request"] = lambda: {"scenarioId": record("Scenario", state="PUBLISHED")["scenarioId"], "version": record("Scenario", state="PUBLISHED")["version"]}
    listing("ListScenarios", "Scenario", "workflow", filters={"state": enum("DRAFT", "PUBLISHED", "ARCHIVED")})
    fields = {"scenarioId": ID, "name": string(1, 256), "description": TEXT, "definition": model("ScenarioDraft"), **GUARDED}
    add("UpdateScenario", "workflow", "LOCAL_COMMAND", "console:AuthorScenario", ["Scenario", "Command"],
        obj(fields, ["scenarioId", "expectedVersion", "clientToken"], anyOf=at_least_change(["name", "description", "definition"])), command_response("Scenario"),
        lambda: {"scenarioId": identifier("Scenario"), "expectedVersion": record("Scenario")["version"], "description": "Updated authoring note; earlier published versions remain immutable.", "definition": record("Scenario", state="DRAFT")["definition"], "clientToken": "update-scenario-demo-0001"},
        ["Publishes the next ordinary Scenario version in DRAFT state, under the current entity expectedVersion. Previously published versions and admitted Runs remain unchanged.",
         "Omitted fields preserve draft values. Reopening a PUBLISHED or ARCHIVED head requires an explicit authoring definition; the server never treats locked published content as an editable draft implicitly.",
         "Editing an ARCHIVED head is a deliberate guarded reopening. The newly created DRAFT version does not make itself executable; StartRun still requires an exact PUBLISHED version."])
    add("PublishScenario", "workflow", "LOCAL_COMMAND", "console:PublishScenario", ["Scenario", "Command"],
        obj({"scenarioId": ID, **GUARDED}), command_response("Scenario"),
        lambda: {"scenarioId": identifier("Scenario"), "expectedVersion": record("Scenario", state="DRAFT")["version"], "clientToken": "publish-scenario-demo-0001"},
        ["Compiles the exact current DRAFT representation, resolves immutable implementation/schema locks and creates the next PUBLISHED version of the same Scenario identity.",
         "Publication validates DAGs, dependency-scoped references, typed bindings, capability checks, required criteria, finalizers and fixed language/reducer semantics before any external work.",
         "The caller cannot submit a trusted lock or digest. A later alias change cannot alter a published version. Missing/revoked pinned artifacts reject future admission rather than substituting another implementation.",
         "GetScenario with version retrieves any retained representation; ListEntityVersions enumerates history. There is no ScenarioRevision resource or default revision pointer."])
    add("ArchiveScenario", "workflow", "LOCAL_COMMAND", "console:AuthorScenario", ["Scenario", "Command"],
        obj({"scenarioId": ID, **GUARDED}), command_response("Scenario"),
        lambda: {"scenarioId": identifier("Scenario"), "expectedVersion": record("Scenario")["version"], "clientToken": "archive-scenario-demo-0001"},
        ["Creates the next Scenario version in ARCHIVED state, retaining the prior definition and publication facts.",
         "A current ARCHIVED head blocks new Run admissions for every version of that Scenario. It does not redirect, cancel or change previously admitted Runs, and exact admission replay still returns its original receipt."])
    input_values = {"type": "object", "additionalProperties": model("JsonValue"), "maxProperties": 100}
    bindings = {"type": "object", "propertyNames": string(1, 64, pattern="^[a-z][a-z0-9_]*$"), "additionalProperties": exact_ref("Connection"), "maxProperties": 100}
    add("StartRun", "workflow", "EXECUTION_COMMAND", "console:StartRun", ["Run", "Snapshot", "StepRun", "Command"],
        obj({"scenario": exact_ref("Scenario"), "subject": model("EntityRef"),
             "inputs": input_values, "bindings": bindings, **MUT}),
        obj({"command": model("Command"), "run": model("Run"), "snapshot": model("Snapshot"), "steps": array(model("StepRun"), maximum=100)}),
        lambda: {"scenario": eref("Scenario", state="PUBLISHED"), "subject": eref("Service"),
                 "inputs": record("Snapshot", kind="RUN_INPUT")["contents"]["inputValues"], "bindings": {"aws": eref("Connection")}, "clientToken": "start-run-demo-0001"},
        ["Durably admits one Run at version 1, its StepRuns and a closed RUN_INPUT snapshot atomically; no claim that an AWS call has started.",
         "scenario pins an exact PUBLISHED Scenario version. The current Scenario head is checked separately: ARCHIVED blocks new admission; a newer DRAFT does not replace the explicitly selected published program.",
         "subject and connection bindings pin exact versions. Admission requires the subject and binding versions still meet the current admission preconditions; current authorization and material provider preconditions are rechecked at dispatch.",
         "inputs must pass the published version's pinned closed input schema; unknown binding names, raw secrets, undeclared operations or unauthorized scope are rejected.",
         "Admission fixes enabled steps and the required-criterion denominator. Runtime skips/cancellation cannot shrink it; inapplicable admission criteria remain recorded.",
         "A new execution intent uses a new clientToken. Neither a latest selector nor a mutable default pointer may select the executed program."])
    get("GetRun", "Run", "workflow")
    listing("ListRuns", "Run", "workflow", filters={"scenario": exact_ref("Scenario"), "phase": MODEL["$defs"]["Run"]["properties"]["phase"]})
    add("RequestRunCancellation", "workflow", "EXECUTION_COMMAND", "console:CancelRun", ["Run", "Command"],
        obj({"runId": ID, "reason": string(1, 4096), **GUARDED}, ["runId", "expectedVersion", "clientToken"]),
        obj({"command": model("Command"), "accepted": BOOL, "run": model("Run")}),
        lambda: {"runId": record("Run", phase="RUNNING")["runId"], "expectedVersion": record("Run", phase="RUNNING")["version"], "reason": "Stop this assessment and reconcile outstanding effects.", "clientToken": "cancel-run-demo-0001"},
        ["Under the supplied current Run.version, atomically records monotonic cancellation intent in the next version and fences new main dispatch. It does not set a remote effect to stopped.",
         "Exact replay is resolved before current-version checks. If the expectedVersion still matches an already sealed Run, the command returns accepted=false and that unchanged terminal representation.",
         "Finalizers reconcile active/unknown effects, including a lost Start response with no handle. A creating Start must never be reissued after cancellation just to discover its result.",
         "Concurrent cancellation intents converge on the first accepted intent after version/replay resolution. Cleanup, execution result and workload verdict remain independently visible."])
    get("GetStepRun", "StepRun", "workflow", parents=("Run",))
    owned_listing("ListRunSteps", "StepRun", "workflow", "Run", "steps",
                  semantics=["Includes every compiled step, including skipped zero-attempt steps. No independent retry/stop/status-update command exists."])
    get("GetStepAttempt", "StepAttempt", "workflow", parents=("Run", "StepRun"))
    owned_listing("ListStepAttempts", "StepAttempt", "workflow", "StepRun", "attempts", parents=("Run",),
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


def typed_refs(value, shape):
    """Find exact refs through model-declared fields, never through opaque JSON."""
    if value is None or not isinstance(shape, dict):
        return
    ref = shape.get("$ref")
    if ref:
        target = ref.rsplit("/", 1)[-1]
        if target in ("EntityRef", "EvidenceRef"):
            yield {key: value[key] for key in ("kind", "id", "version")}
            return
        if target in MODEL["$defs"]:
            yield from typed_refs(value, MODEL["$defs"][target])
    if isinstance(value, dict):
        for key, child in shape.get("properties", {}).items():
            if key in value:
                yield from typed_refs(value[key], child)
    elif isinstance(value, list) and isinstance(shape.get("items"), dict):
        for item in value:
            yield from typed_refs(item, shape["items"])
    for keyword in ("anyOf", "oneOf", "allOf"):
        for branch in shape.get(keyword, []):
            yield from typed_refs(value, branch)
    if "if" in shape:
        # Model conditions select typed profile/state fields by literal values.
        condition = shape["if"]
        matches = isinstance(value, dict) and all(
            key in value and ("const" not in test or value[key] == test["const"])
            for key, test in condition.get("properties", {}).items())
        yield from typed_refs(value, shape.get("then" if matches else "else", {}))


def reference_key(ref):
    return ref["kind"], ref["id"], ref["version"]


def closed_members(refs):
    pending = list(refs)
    found = {}
    while pending:
        ref = pending.pop()
        key = reference_key(ref)
        if key in found:
            continue
        found[key] = {name: ref[name] for name in ("kind", "id", "version")}
        row = resolve(ref)
        pending.extend(typed_refs(row, MODEL["$defs"][ref["kind"]]))
    return [found[key] for key in sorted(found)]


def snapshot_digest(row):
    return digest({key: value for key, value in row.items() if key != "manifestDigest"})


def guarded_entity(op):
    explicit = {"RecordReadAttempt": "ReadAttempt", "CompleteCollection": "Collection", "PublishProjection": "Projection",
                "UpdateDependencyGovernance": "Dependency", "UpdateDependencyClassification": "Dependency",
                "UpdateRecommendationEnrichment": "Recommendation", "RecordWorkItemVerification": "WorkItem",
                "UpdateFindingDisposition": "Finding", "UpdateResiliencePolicyConfiguration": "ResiliencePolicy",
                "UpdateResilienceServiceConfiguration": "Service", "StartResilienceAssessment": "Service",
                "StartInvestigation": "AgentSpace", "DecideApproval": "ApprovalRequest", "ResumeExecution": "Execution",
                "PublishScenario": "Scenario", "ArchiveScenario": "Scenario", "RequestRunCancellation": "Run", "StopExperiment": "Experiment"}
    if op["name"] in explicit:
        return explicit[op["name"]]
    if op["name"].startswith("Update") and op["name"][6:] in MODEL["x-entities"]:
        return op["name"][6:]
    return None


def command_example(op, request):
    result = record("Command")
    result.update({"commandId": "cmd-" + op["name"].lower() + "-demo", "operation": op["name"],
                   "version": 1, "createdAt": NOW, "updatedAt": NOW,
                   "clientToken": request["clientToken"], "requestDigest": digest(request),
                   "expectedVersion": request.get("expectedVersion"), "acceptedAt": NOW,
                   "state": "ACCEPTED" if op["kind"] == "PROVIDER_COMMAND" else "SUCCEEDED",
                   "attempts": [], "effects": [], "replayExpiresAt": NOW + (90 * 86400 if op["kind"] == "EXECUTION_COMMAND" else 86400),
                   "subjectRefs": [], "resultRefs": []})
    guarded = guarded_entity(op)
    for entity in MODEL["x-entities"]:
        key = idfield(entity)
        if key in request:
            selector = {key: request[key]}
            if entity == guarded and request.get("expectedVersion") is not None:
                selector["version"] = request["expectedVersion"]
            result["subjectRefs"].append(eref(entity, **selector))
    for key in ("subject", "connection", "scenario", "expectedSource", "expectedRequestSource", "approvalRequest", "decisionCommand"):
        if key in request:
            result["subjectRefs"].append(copy.deepcopy(request[key]))
    result["subjectRefs"] += copy.deepcopy(request.get("subjectRefs", []))
    result["subjectRefs"] += copy.deepcopy(list(request.get("bindings", {}).values()))
    refs = {reference_key(ref): ref for ref in result["subjectRefs"]}
    result["subjectRefs"] = [refs[key] for key in sorted(refs)]
    return result


def page_example(name):
    return {"traversalId": "page-" + name.lower() + "-demo", "asOfSequence": 1, "createdAt": NOW, "expiresAt": NOW + 900}


def structural_parent_value(kind, row, wanted, seen=None):
    """Follow identity-only ownership fields for illustrative list scoping."""
    if wanted in row:
        return row[wanted]
    seen = set() if seen is None else seen
    identity_key = kind, row[idfield(kind)]
    if identity_key in seen:
        return None
    seen.add(identity_key)
    for parent in MODEL["x-entities"]:
        field = idfield(parent)
        if parent not in (kind, "Workspace") and field in row:
            value = structural_parent_value(parent, record(parent, **{field: row[field]}), wanted, seen)
            if value is not None:
                return value
    return None


def list_heads(entity, request):
    heads = {}
    for row in RECORDS[entity]:
        identifier_value = row[idfield(entity)]
        if identifier_value not in heads or row["version"] > heads[identifier_value]["version"]:
            heads[identifier_value] = row
    rows = []
    ids = {idfield(item) for item in MODEL["x-entities"]}
    for row in heads.values():
        selected = True
        for field, value in request.items():
            if field in ids:
                selected &= structural_parent_value(entity, row, field) == value
            elif field in row and field not in ("maxResults", "nextToken"):
                selected &= row[field] == value
        if selected:
            rows.append(copy.deepcopy(row))
    ordering = {"Observation": ("observedAt", False), "Projection": ("generatedAt", True),
                "Snapshot": ("capturedAt", True), "Command": ("acceptedAt", True), "Run": ("admittedAt", True)}
    rows.sort(key=lambda row: row[idfield(entity)])
    if entity in ordering:
        field, descending = ordering[entity]
        rows.sort(key=lambda row: row[field], reverse=descending)
    return rows


def paged_example(name, request, items, **extra):
    size = request.get("maxResults", 20)
    result = {**extra, "items": items[:size], "page": page_example(name)}
    if len(items) > size:
        result["nextToken"] = "opaque-" + name.lower() + "-continuation-demo"
    return result


def create_response(op, request):
    name = op["name"]
    output = DEFS[name + "Response"]["properties"]
    selectors = SAMPLES[name]["responseSelector"]
    if name == "ListEntityVersions":
        entity = request["entity"]["kind"]
        rows = [row for row in RECORDS[entity] if row[idfield(entity)] == request["entity"]["id"]]
        return paged_example(name, request, [eref(entity, row=row) for row in sorted(rows, key=lambda row: -row["version"])])
    if "ownedParent" in SAMPLES[name]:
        spec = SAMPLES[name]["ownedParent"]
        entity = spec["entity"]
        selector = {idfield(entity): request[idfield(entity)]}
        if spec["versionField"] in request:
            selector["version"] = request[spec["versionField"]]
        parent = record(entity, **selector)
        return paged_example(name, request, [resolve(ref) for ref in parent[spec["field"]]], parent=eref(entity, row=parent))
    result = {}
    for key, shape in output.items():
        if key == "command" and op["mutating"]:
            continue
        if key == "nextToken":
            continue  # Set below when matching rows exceed the requested page.
        if key == "page":
            result[key] = page_example(name)
        elif key == "accepted":
            result[key] = True
        elif key == "steps":
            result[key] = []  # Filled atomically by the StartRun admission below.
        else:
            actual_shape = shape["items"] if key == "items" else shape
            if "$ref" in actual_shape:
                entity = actual_shape["$ref"].rsplit("/", 1)[1]
            elif "allOf" in actual_shape and "$ref" in actual_shape["allOf"][0]:
                entity = actual_shape["allOf"][0]["$ref"].rsplit("/", 1)[1]
            else:
                raise ValueError(f"No response generator for {name} {key}")
            if key == "items":
                result.update(paged_example(name, request, list_heads(entity, request)))
                continue
            selector = copy.deepcopy(selectors.get(entity, {}))
            entity_id_fields = {idfield(item) for item in MODEL["x-entities"]}
            for field, value in request.items():
                if field in entity_id_fields and field in MODEL["$defs"][entity]["properties"]:
                    selector[field] = value
            if not op["mutating"] and "version" in request:
                selector["version"] = request["version"]
            if op["mutating"] and entity == guarded_entity(op) and request.get("expectedVersion") is not None:
                selector["version"] = request["expectedVersion"]
            row = record(entity, **selector)
            result[key] = row

    # Each mutation example is independent and states its prior-head preconditions.
    for entity in ("System", "UserJourney", "Service", "Scenario", "Connection", "WorkItem"):
        if name in ("Create" + entity, "Update" + entity):
            row = result[lower(entity)]
            for key, value in request.items():
                if key in row and key not in (idfield(entity), "version", "createdAt", "updatedAt", "providerBindings"):
                    row[key] = copy.deepcopy(value)
            row["version"] = 1 if name.startswith("Create") else request["expectedVersion"] + 1
            row["updatedAt"] = NOW
            if name.startswith("Create"):
                row[idfield(entity)] = lower(entity) + "-created-demo"
                row["createdAt"] = NOW
            for key in request.get("clearFields", []):
                row[key] = None
            if name.startswith("Create") and "providerBindings" in row:
                row["providerBindings"] = []
            if "memberships" in request:
                row["memberships"] = [{**member, "origin": "LOCAL", "source": None} for member in request["memberships"]]
            if "assigneeSubjectId" in request:
                row["owner"] = {"issuer": "fixture-identity", "subject": request["assigneeSubjectId"], "kind": "HUMAN"}
            if entity == "Scenario":
                row.update({"state": "DRAFT", "publishedAt": None, "digest": None})
            if name == "CreateWorkItem":
                row.update({"state": "OPEN", "owner": None, "snoozedUntil": None, "resolutionEvidence": [], "actions": [],
                            "priority": request.get("priority", "MEDIUM"), "dueAt": request.get("dueAt"), "verificationState": "NOT_REQUESTED", "verificationEvidence": []})
    if name == "UpdateDependencyGovernance":
        row = result["dependency"]
        row.update({"version": request["expectedVersion"] + 1, "updatedAt": NOW})
        row["governance"].update({"decision": request["decision"], "reason": request["reason"], "updatedAt": NOW})
    if name == "UpdateRecommendationEnrichment":
        row = result["recommendation"]
        row.update({"version": request["expectedVersion"] + 1, "updatedAt": NOW})
        enriched = row["enrichment"]
        for key in ("title", "effort", "estimate", "note"):
            if key in request:
                enriched[key] = request[key]
        for key in request.get("clearFields", []):
            enriched[key] = None
        enriched["provenance"] = "LOCAL_OPERATOR_ENRICHMENT"
    if name == "RecordWorkItemVerification":
        result["workItem"].update({"version": request["expectedVersion"] + 1, "updatedAt": NOW,
                                  "verificationState": request["result"], "verificationEvidence": copy.deepcopy(request["evidenceRefs"])})
    if name == "PublishScenario":
        row = result["scenario"]
        row.update({"version": request["expectedVersion"] + 1, "updatedAt": NOW, "state": "PUBLISHED", "publishedAt": NOW,
                    "definition": record("Scenario", state="PUBLISHED")["definition"]})
        row["digest"] = digest(row["definition"])
    if name == "ArchiveScenario":
        result["scenario"].update({"version": request["expectedVersion"] + 1, "updatedAt": NOW, "state": "ARCHIVED"})
    if name == "StartCollection":
        result["collection"].update({"collectionId": "collection-started-demo", "version": 1, "createdAt": NOW, "updatedAt": NOW,
                                     "connection": copy.deepcopy(request["connection"]), "queries": copy.deepcopy(request["queries"]),
                                     "state": "RUNNING", "startedAt": NOW, "endedAt": None, "coverage": []})
    if name == "CompleteCollection":
        result["collection"].update({"state": "COMPLETED", "endedAt": NOW, "coverage": copy.deepcopy(request["coverage"]),
                                     "version": request["expectedVersion"] + 1, "updatedAt": NOW})
    if name == "RecordReadAttempt":
        row = result["readAttempt"]
        row.update({key: copy.deepcopy(value) for key, value in request.items() if key in row})
        row.update({"version": request["expectedVersion"] + 1, "updatedAt": NOW})
    if name == "PublishProjection":
        row = result["projection"]
        row.update({key: copy.deepcopy(value) for key, value in request.items() if key in row})
        row.update({"version": (request["expectedVersion"] or 0) + 1, "updatedAt": NOW, "generatedAt": NOW})
        if request["expectedVersion"] is None:
            row["createdAt"] = NOW
    if name == "CaptureSnapshot":
        row = result["snapshot"]
        row.update({"snapshotId": "snapshot-captured-demo", "version": 1, "createdAt": NOW, "updatedAt": NOW,
                    "capturedAt": NOW, "captureStartedAt": NOW, "captureFinishedAt": NOW,
                    "subjectRefs": copy.deepcopy(request["subjectRefs"]), "members": closed_members(request["members"] + request["subjectRefs"])})
        row["manifestDigest"] = snapshot_digest(row)
    if name == "IngestObservation":
        observation = record("Observation")
        result["source"] = resolve(observation["source"])
        result["observation"] = observation
    if name == "StartRun":
        row = result["run"]
        row.update({"runId": "run-admitted-demo", "version": 1, "createdAt": NOW, "updatedAt": NOW,
                    "scenario": copy.deepcopy(request["scenario"]), "phase": "ADMITTED", "executionOutcome": "PENDING",
                    "assessmentVerdict": "NOT_EVALUATED", "assessmentFinality": "PROVISIONAL", "finalizationState": "PENDING",
                    "effectState": "NONE", "cancellationIntent": None, "admittedAt": NOW, "terminalAt": None, "steps": [], "asOfSequence": 0})
        for old_step in sorted((step for step in RECORDS["StepRun"] if step["version"] == 1), key=lambda step: step["stepKey"]):
            step = copy.deepcopy(old_step)
            step.update({"stepRunId": "step-admitted-" + step["stepKey"] + "-demo", "runId": row["runId"],
                         "version": 1, "createdAt": NOW, "updatedAt": NOW, "phase": "PENDING", "outcome": None,
                         "attempts": [], "selectedAttempt": None, "skipReason": None})
            result["steps"].append(step)
            row["steps"].append(eref("StepRun", row=step))
        snap = record("Snapshot", kind="RUN_INPUT")
        snap.update({"snapshotId": "snapshot-run-admission-demo", "version": 1, "createdAt": NOW, "updatedAt": NOW,
                     "capturedAt": NOW, "captureStartedAt": NOW, "captureFinishedAt": NOW, "subjectRefs": [copy.deepcopy(request["subject"])]})
        snap["contents"].update({"scenario": copy.deepcopy(request["scenario"]), "scenarioDigest": resolve(request["scenario"])["digest"],
                                 "subjectRefs": [copy.deepcopy(request["subject"])], "inputValues": copy.deepcopy(request["inputs"]), "admittedAt": NOW})
        for binding in snap["contents"]["resolvedBindings"]:
            binding["connection"] = copy.deepcopy(request["bindings"][binding["bindingKey"]])
        initial = list(typed_refs(snap["contents"], MODEL["$defs"]["Admission"]))
        for coverage in snap["coverage"]:
            initial.extend(typed_refs(coverage, MODEL["$defs"]["Coverage"]))
        snap["members"] = closed_members(initial + snap["subjectRefs"])
        snap["manifestDigest"] = snapshot_digest(snap)
        result["snapshot"] = snap
        row["inputSnapshot"] = eref("Snapshot", row=snap)
    if name == "RequestRunCancellation":
        result["run"].update({"version": request["expectedVersion"] + 1, "updatedAt": NOW,
                              "phase": "FINALIZING", "finalizationState": "PENDING"})
    if "command" in output and op["mutating"]:
        result["command"] = command_example(op, request)
        if name == "RequestRunCancellation":
            result["run"]["cancellationIntent"] = {"commandId": result["command"]["commandId"], "acceptedAt": NOW,
                                                    "actor": result["command"]["actor"], "reason": request.get("reason", "")}
        if name == "UpdateWorkItem":
            result["workItem"]["actions"].append({"actionKey": "action-update-work-item-demo", "action": "UPDATE_WORK_ITEM",
                "actor": result["command"]["actor"], "at": NOW, "reason": request.get("note", ""), "evidenceRefs": request.get("resolutionEvidence", [])})
        if name == "RecordWorkItemVerification":
            result["workItem"]["actions"].append({"actionKey": "action-verify-work-item-demo", "action": "RECORD_VERIFICATION",
                "actor": result["command"]["actor"], "at": NOW, "reason": request["rationale"], "evidenceRefs": copy.deepcopy(request["evidenceRefs"])})
        result["command"]["resultRefs"] = [eref(entity, row=result[lower(entity)]) for entity in MODEL["x-entities"]
                                            if entity != "Command" and lower(entity) in result]
        if "steps" in result:
            result["command"]["resultRefs"] += [eref("StepRun", row=step) for step in result["steps"]]
    return result


def example_preconditions(op, request):
    notes = ["Independent design illustration, not a command to execute against the final model fixture heads."]
    heads = []
    guarded = guarded_entity(op)
    if guarded and request.get("expectedVersion") is not None:
        selector = {"version": request["expectedVersion"]}
        key = idfield(guarded)
        if key in request:
            selector[key] = request[key]
        if guarded == "Projection":
            selector["profile"] = request["profile"]
        before = record(guarded, **selector)
        heads.append(eref(guarded, row=before))
        notes.append("The listed exact representation is the current head at this illustration's admission; later fixture versions belong to another point in history.")
    if op["name"] == "ResumeExecution":
        notes.append("The requested decisionCommand version 2 is assumed definitively SUCCEEDED for this exact approval scope; the earlier ACCEPTED command version 1 is insufficient.")
    return {"currentHeads": heads, "notes": notes}


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
        put(rh, "Get" + entity, "Get" + entity + " GetSource", "CANONICAL_READ_WITH_NATIVE_FACET",
            "Local canonical identity is separate from the retained native profile; verified provider binding supplies the bridge.")
        put(rh, "List" + plural, "List" + plural + " ListSources", "CANONICAL_READ_WITH_NATIVE_FACET",
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
    put(rh, "ListInputSources", "ListSources GetSource", "RETAINED_TYPED_PROFILE", "Use aws.resilience-hub.input-source/v1 and exact service-scoped source identity.")
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
    put(rh, "GetServiceStatus", "GetServiceStatus", "QUALIFIED_PROJECTION_READ", "Returns currently selected SERVICE_STATUS Projection with its evidence and independent dimensions.")
    put(rh, "GetWorkspaceSummary", "GetWorkspaceSummary", "QUALIFIED_PROJECTION_READ", "Returns WORKSPACE_SUMMARY for authorized contributors, with denominator and rule.")
    put(rh, "ListEvents", "ListObservations ListSources", "SHARED_EVIDENCE_READ", "Filter exact subjects/profile/channel evidence; delivery ID never becomes a HealthEvent ID.")
    put(rh, "PutHealthObservation", "IngestObservation PublishProjection", "SHARED_TRUSTED_INGEST", "Retain runtime-health source evidence then derive SERVICE_STATUS. This is distinct from AWS Health Event ingestion.")
    put(rh, "IngestEvent", "IngestObservation StartCollection", "SHARED_TRUSTED_INGEST", "Retains raw channel evidence and schedules authorized read collection; event body cannot patch authoritative state.")
    for operation in ("GetScenario", "ListScenarios", "GetRun", "ListRuns", "RequestRunCancellation", "ListRunSteps", "ListStepAttempts"):
        put(wf, operation, operation, "RPC_REBINDING", "Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions.")
    put(wf, "GetScenarioRevision", "GetScenario", "UNIFORM_ENTITY_VERSION", "Resolve the migrated Scenario identity and exact version; no separate revision identity exists.")
    put(wf, "ListScenarioRevisions", "ListEntityVersions", "UNIFORM_ENTITY_HISTORY", "Enumerate exact Scenario version refs, then GetScenario with version. DRAFT, PUBLISHED and ARCHIVED share one entity history.")
    put(wf, "CreateScenario", "CreateScenario", "EXTENDED_AUTHORING_CONTRACT", "Creates metadata and a typed editable draft; trusted operation locks remain publication-owned.")
    put(wf, "UpdateScenario", "UpdateScenario", "RPC_REBINDING", "expectedVersion replaces If-Match; omission preserves and explicit allowed clears replace nullable PATCH ambiguity.")
    put(wf, "PublishScenarioRevision", "UpdateScenario PublishScenario", "DRAFT_THEN_PUBLISH", "Update the typed draft, then publish under expectedVersion; the server resolves trusted locks and creates the next version of the same Scenario.")
    put(wf, "StartRun", "StartRun", "RPC_REBINDING", "Pins canonical subject, exact published Scenario version, validated inputs and authorized connection versions; retains immutable admission and criterion denominator.")
    put(wf, "ListRunEvidence", "ListObservations ListSources ListProjections", "SHARED_TYPED_EVIDENCE", "Filter the exact Run subject/producer references; raw source, receipt and derived evidence types stay explicit.")
    put(wf, "GetEvidence", "GetSource GetObservation GetProjection GetSnapshot", "SHARED_TYPED_EVIDENCE", "Resolve the discriminated EvidenceRef kind; evidence is not collapsed into an untyped payload.")
    put(wf, "ListOperations", "GetScenario", "DYNAMIC_DISCOVERY_DEFERRED", "An exact published Scenario version exposes its locks. Authorized discovery of executable adapter aliases is later registry work; facade operations.json is not that adapter registry.")
    assert sum(x["sourcePackage"] == rh for x in rows) == 44
    assert sum(x["sourcePackage"] == wf for x in rows) == 16
    prior = "consolidated-operations-console/api@db142c84bcfd691d5c71071681731cac81a52c7b"
    renamed = {
        "GetSourceRevision": ("GetSource", "Stable Source identity plus version replaces the revision ID."),
        "ListSourceRevisions": ("ListSources ListEntityVersions", "List current Source heads; enumerate a Source identity's versions through the common history operation."),
        "GetProjectionRevision": ("GetProjection", "Stable Projection identity plus version replaces the revision ID."),
        "ListProjectionRevisions": ("ListProjections ListEntityVersions", "List current Projection heads and enumerate exact historical versions separately."),
        "GetScenarioRevision": ("GetScenario", "The published program is a Scenario representation selected by version."),
        "ListScenarioRevisions": ("ListEntityVersions", "One Scenario history includes draft, published and archived representations."),
        "PublishScenarioRevision": ("PublishScenario", "Publication creates the next version of the same Scenario; no revision resource or alias is retained."),
        "UpdateScenario": ("UpdateScenario ArchiveScenario", "Editing creates a DRAFT version; archival is an explicit guarded intent; defaultRevisionId is removed."),
        "UpdateDependencyGovernance": ("UpdateDependencyGovernance", "expectedVersion guards Dependency.version, including its owned governance value."),
        "UpdateRecommendationEnrichment": ("UpdateRecommendationEnrichment CreateWorkItem UpdateWorkItem", "Metadata uses Recommendation.version; assignment and work state move to WorkItem with its own identity/version."),
        "CompleteCollection": ("CompleteCollection", "expectedVersion replaces expectedProjectionVersion; completion creates the next Collection version."),
        "StartRun": ("StartRun", "Exact scenario/subject/connection references replace revision IDs and optional subject guards; admission returns matching run, snapshot and step representations."),
        "GetAsset": ("GetAsset", "Each Asset version carries nativeVersion/source/files directly; the embedded versions array is removed."),
    }
    for operation in V1_OPERATION_NAMES:
        targets, note = renamed.get(operation, (operation, "Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility."))
        put(prior, operation, targets, "BREAKING_CONTRACT_V2", note)
    assert len({(x["sourcePackage"], x["sourceOperation"]) for x in rows}) == 161
    available = {op["name"] for op in OPS}
    assert all(set(row["newOperations"]) <= available for row in rows)
    return rows


def generate_docs(catalog):
    lines = ["# Consolidated operations console — RPC operations", "",
             f"API date **2026-11-05** · **contract revision 2** · namespace `{NAMESPACE}` · **{len(OPS)} operations**", "",
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
              "Every entity has one `version`, `createdAt` and `updatedAt`. `Get<Entity>` accepts optional `version`: explicit means exact, omitted means current head; no historical read falls back to latest. `ListEntityVersions` returns exact reference values for one logical identity. Evidence references contain `{kind,id,version}`; live navigation uses the distinct `{kind,id}` EntityIdentity value.", "",
              "`clientToken` is required for every mutation. `expectedVersion` guards the whole named entity, including owned metadata; there are no nested overlay clocks. `expectedSource` pins native evidence and is never an AWS conditional-write guarantee. `maxResults` is 1–100, default 20; `nextToken` binds an authorization-scoped retained publication. No JSON body can choose the acting user, role or authenticated workspace.", "",
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
              "This table accounts for every operation in the 44-operation Resilience facade, 16-operation workflow proposal and 101-operation consolidated V1 proposal. V2 intentionally breaks the first consolidated contract; no misleading legacy revision-resource aliases are provided. Changes of scope, transport, version ownership and supported fields are explicit.", "",
              "| Source | Prior operation | Consolidated operation(s) | Disposition and meaning |", "| --- | --- | --- | --- |"]
    for entry in catalog["predecessorMappings"]:
        source = "Resilience" if "resilience-hub" in entry["sourcePackage"] else "Workflow" if entry["sourcePackage"].startswith("aws/") else "Console V1"
        targets = ", ".join("`" + name + "`" for name in entry["newOperations"]) or "Deferred"
        lines.append(f"| {source} | `{entry['sourceOperation']}` | {targets} | `{entry['disposition']}`. {entry['notes']} |")
    lines += ["", "## Deliberately deferred command families", "",
              "The previous service packages remain the detailed native API references. This first consolidation defines a narrow provider mutation surface; the rest remain typed source profiles and explicit later adapter work:", "",
              "| Family | Retained now | Later command work |", "| --- | --- | --- |",
              "| Resilience provider systems/journeys/services/policies | Versioned Source records, verified canonical bindings and selected configuration commands | Native creates/deletes, association replacement/detachment, permission/report/input-source configuration and destructive clears |",
              "| FIS templates/catalog/resource types/safety lever | Typed source profiles; experiment reads and whole-experiment stop | Template CRUD and scope-wide safety-lever mutation after dedicated authorization and adapter semantics |",
              "| DevOps registration/association/webhook/goal/recommendation/trigger/operator/private connection | Typed source DTOs and their exact scopes through Source reads | Provider management commands; no native recommendation is conflated with Resilience recommendation identity |",
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
              "x-contractVersion": 2, "$defs": DEFS}
    catalog = {"apiVersion": "2026-11-05", "contractVersion": 2, "namespace": NAMESPACE, "maturity": "CONTRACT_ONLY", "operationCount": len(OPS),
               "supersedes": {"namespace": "ConsolidatedOperationsConsole_20261105", "commit": "db142c84bcfd691d5c71071681731cac81a52c7b", "compatibility": "BREAKING_PROPOSED_CONTRACT_CORRECTION"},
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
            example = {"operation": op["name"], "request": request, "response": response}
            if op["mutating"]:
                example["preconditions"] = example_preconditions(op, request)
            examples.append(example)
        errors = [
            {"name": "stale-local-configuration", "operation": "UpdateService", "status": 409,
             "response": {"__type": "VersionConflictException", "code": "EXPECTED_VERSION_MISMATCH", "message": "The service configuration changed; read it before issuing a new intent.", "requestId": "req-stale-demo", "retryable": False}},
            {"name": "expired-snapshot-cursor", "operation": "ListFindings", "status": 410,
             "response": {"__type": "PaginationTokenExpiredException", "code": "CURSOR_EXPIRED", "message": "Begin a new explicit list traversal.", "requestId": "req-expired-demo", "retryable": False}},
            {"name": "token-payload-conflict", "operation": "StartRun", "status": 409,
             "response": {"__type": "IdempotencyConflictException", "code": "TOKEN_INTENT_MISMATCH", "message": "The token already identifies a different request.", "requestId": "req-token-demo", "retryable": False}},
        ]
        outputs["examples.json"] = {"schemaVersion": "consolidated-rpc-examples/2", "synthetic": True,
                                    "notice": "Independent schema-valid design examples with explicit prior-head preconditions; they are not one chronological transaction log or calls against the final model fixture heads. No operation was invoked; receipts and outcomes are illustrative.",
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
