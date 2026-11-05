"""Counterexamples for the proposed contract; no cloud or scheduler simulation."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import contract


class ScenarioContractTests(unittest.TestCase):
    def setUp(self):
        self.document = contract.read_document(ROOT / "examples/alarm-delivery.yaml")

    def reject(self, pattern):
        with self.assertRaisesRegex(contract.ContractError, pattern):
            contract.validate_document(self.document)

    def test_complete_examples_and_committed_locks(self):
        for path in (ROOT / "examples").glob("*.yaml"):
            with self.subTest(example=path.name):
                doc = contract.read_document(path)
                contract.validate_document(doc)
                contract.validate_lock(doc, json.loads(path.with_suffix(".lock.json").read_text()))

    def test_duplicate_yaml_keys_cannot_discard_a_step(self):
        with self.assertRaisesRegex(contract.ContractError, "duplicate YAML key"):
            contract.yaml.load("steps:\n  inject: one\n  inject: two\n", Loader=contract.UniqueLoader)

    def test_yaml_retry_on_is_a_string_key(self):
        parsed = contract.yaml.load("retry:\n  on: [throttled]\nactive: true\n", Loader=contract.UniqueLoader)
        self.assertEqual(parsed, {"retry": {"on": ["throttled"]}, "active": True})

    def test_cycle_is_rejected(self):
        self.document["steps"]["baseline"]["needs"] = ["inject"]
        self.reject("cycle")

    def test_main_cannot_depend_on_finalizer(self):
        self.document["steps"]["inject"]["needs"].append("stop_injection")
        self.reject("not in its main graph")

    def test_sibling_output_does_not_imply_an_order(self):
        self.document["steps"]["baseline"]["with"]["alarmArn"] = "${{ steps.capture.outputs.capture }}"
        self.reject("non-ancestor")

    def test_unknown_output_does_not_become_null(self):
        self.document["steps"]["baseline_ok"]["with"]["observation"] = "${{ steps.baseline.outputs.missing }}"
        self.reject("undeclared output")

    def test_unknown_input_binding_is_rejected(self):
        self.document["steps"]["inject"]["with"]["templateId"] = "${{ inputs.templteId }}"
        self.reject("undeclared input")

    def test_unknown_connection_binding_is_rejected(self):
        self.document["steps"]["inject"]["with"]["connection"] = "${{ bindings.arbitraryRole }}"
        self.reject("undeclared binding")

    def test_required_criterion_cannot_change_applicability_from_run_data(self):
        self.document["steps"]["alarm_transition"]["enabledWhen"] = 'steps.collect.execution.outcome == "succeeded"'
        self.reject("enabledWhen")

    def test_mutation_cannot_choose_its_own_observer_capability(self):
        self.document["steps"]["inject"]["effect"] = "observe"
        self.reject("Additional properties")

    def test_mutation_cannot_relax_failed_dependencies(self):
        self.document["steps"]["inject"]["after"] = "settled"
        self.reject("settled main mutation")

    def test_finalizer_cannot_skip_ambiguous_start_by_missing_output(self):
        self.document["finally"]["stop_injection"]["if"] = "has(steps.inject.outputs.experiment)"
        self.reject("unconditional cleanup")

    def test_non_check_cannot_claim_criterion_role(self):
        self.document["steps"]["inject"]["assessmentRole"] = "criterion"
        self.reject("requires a check operation")

    def test_unbounded_retry_and_false_assertion_retry_are_rejected(self):
        self.document["steps"]["alarm_transition"]["retry"] = {"maxAttempts": 2, "on": ["throttled"]}
        self.reject("assertion retries")

    def test_non_monotone_predicate_cannot_claim_witness_proof(self):
        self.document["steps"]["notification_received"]["with"]["expect"] = "size(value.records) == 1"
        self.reject("exactly one operation input form")

    def test_bad_literal_is_rejected_before_admission(self):
        self.document["steps"]["capture"]["with"]["leaseSeconds"] = "900"
        self.reject("not of type")

    def test_unknown_writable_input_is_rejected(self):
        self.document["steps"]["inject"]["with"]["outcome"] = "succeeded"
        self.reject("unknown fields")

    def test_alias_rotation_does_not_change_a_published_revision(self):
        lock = contract.make_lock(self.document)
        changed = copy.deepcopy(contract.CATALOGUE)
        old_ref = changed["aliases"]["aws/fis.start@1"]
        new_ref = "sha256:" + "0" * 64
        changed["revisions"][new_ref] = {**changed["revisions"][old_ref], "implementationDigest": new_ref}
        changed["aliases"]["aws/fis.start@1"] = new_ref
        contract.validate_lock(self.document, lock, changed)
        self.assertEqual(lock["operations"]["aws/fis.start@1"]["implementationDigest"], old_ref)
        self.assertNotEqual(contract.make_lock(self.document, changed), lock)

    def test_missing_or_revoked_pinned_artifact_never_substitutes_current_alias(self):
        lock = contract.make_lock(self.document)
        ref = lock["operations"]["aws/fis.start@1"]["implementationDigest"]
        for state in ("missing", "revoked"):
            changed = copy.deepcopy(contract.CATALOGUE)
            if state == "missing":
                del changed["revisions"][ref]
            else:
                changed["revokedDigests"].append(ref)
            with self.subTest(state=state), self.assertRaisesRegex(contract.ContractError, "unavailable or revoked"):
                contract.validate_lock(self.document, lock, changed)

    def test_available_observation_requires_value_and_unavailable_omits_it(self):
        operation = contract.alias_operations(contract.CATALOGUE)["aws/cloudwatch.alarm.read@1"]
        observation = {"collection": "unavailable", "coverage": "unknown", "windowClosed": True, "evidenceIds": [], "scope": "alarm", "observedAt": "2026-11-05T09:00:00Z", "source": {"namespace": "aws/cloudwatch", "identity": "alarm", "authenticated": True}}
        contract.check_json({"observation": observation}, operation["outputSchema"], "output")
        with self.assertRaises(contract.ContractError):
            contract.check_json({"observation": {**observation, "value": {"state": "OK", "alarmArn": "arn:test"}}}, operation["outputSchema"], "output")
        with self.assertRaises(contract.ContractError):
            contract.check_json({"observation": {**observation, "collection": "complete"}}, operation["outputSchema"], "output")

    def test_no_dispatch_cleanup_does_not_require_an_invented_effect_key(self):
        operation = contract.alias_operations(contract.CATALOGUE)["aws/fis.ensure-stopped@1"]
        noop = {"remoteDisposition": "none", "step": {"runId": "run_a", "stepKey": "inject"}, "reasonCode": "NOT_DISPATCHED", "evidenceIds": []}
        contract.check_json(noop, operation["outputSchema"], "output")
        with self.assertRaises(contract.ContractError):
            contract.check_json({**noop, "remoteDisposition": "unknown"}, operation["outputSchema"], "output")

    def test_policy_and_input_schema_are_part_of_locked_program(self):
        lock = contract.make_lock(self.document)
        self.document["policies"]["timeoutSeconds"] += 1
        with self.assertRaisesRegex(contract.ContractError, "fixed program"):
            contract.validate_lock(self.document, lock)

    def test_object_order_does_not_change_content_digest(self):
        self.assertEqual(contract.digest({"a": 1, "b": [2, 3]}), contract.digest({"b": [2, 3], "a": 1}))
        self.assertNotEqual(contract.digest({"a": [1, 2]}), contract.digest({"a": [2, 1]}))

    def test_malformed_predicate_result_is_not_a_false_assertion(self):
        with self.assertRaisesRegex(contract.ContractError, "typed boolean"):
            contract.proof({"proof": "complete", "collection": "complete", "coverage": "sufficient", "sourceTrusted": True, "windowClosed": True, "predicateValue": "false"})

    def test_boolean_is_not_an_evidence_record_count(self):
        with self.assertRaisesRegex(contract.ContractError, "nonnegative integer"):
            contract.proof({"proof": "witness", "collection": "partial", "coverage": "unknown", "sourceTrusted": True, "windowClosed": False, "matchingRecords": True})

    def test_duplicate_criterion_cannot_inflate_denominator(self):
        with self.assertRaisesRegex(contract.ContractError, "duplicate required criterion"):
            contract.assessment({"final": True, "requiredCriteria": ["a", "a"], "results": {"a": "passed"}})

    def test_local_finalization_deadline_without_remote_effect_is_not_indeterminate(self):
        result = contract.termination({"unresolvedEffects": 0, "substantiveFailure": False, "deadlineTermination": True, "cancellationAccepted": False, "preconditionBlocked": False, "requiredFinalizersSucceeded": False})
        self.assertEqual(result, {"outcome": "timed_out", "finalizationStatus": "incomplete", "retainScopeHold": False})

    def test_incomplete_cleanup_cannot_silently_succeed(self):
        with self.assertRaisesRegex(contract.ContractError, "needs a failure"):
            contract.termination({"unresolvedEffects": 0, "substantiveFailure": False, "deadlineTermination": False, "cancellationAccepted": False, "preconditionBlocked": False, "requiredFinalizersSucceeded": False})


class IndependentReviewCases(unittest.TestCase):
    """Expected facts were authored by a separate reviewer before these helpers."""


def make_case_test(case):
    def test(self):
        self.assertEqual(contract.DECISIONS[case["category"]](case["input"]), case["expected"], case["reason"])
    test.__doc__ = case["reason"]
    return test


for review_case in json.loads((ROOT / "review-cases.json").read_text())["cases"]:
    setattr(IndependentReviewCases, f"test_{review_case['id']}_{review_case['category']}", make_case_test(review_case))


if __name__ == "__main__":
    unittest.main()
