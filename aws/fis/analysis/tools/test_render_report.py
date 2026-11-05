#!/usr/bin/env python3
"""Regression checks for report provenance, using isolated temporary copies."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1]


class ReportArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix='fis-report-check-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        for name in ('report.md', 'sources.json', 'aws_fis_experiment_action_model.pdf'):
            shutil.copy2(SOURCE / name, self.base / name)
        shutil.copytree(SOURCE / 'diagrams', self.base / 'diagrams')
        (self.base / 'tools').mkdir()
        for name in ('render_report.py', 'render-manifest.json'):
            shutil.copy2(SOURCE / 'tools' / name, self.base / 'tools' / name)

    def run_renderer(self, *arguments: str, succeeds: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(self.base / 'tools/render_report.py'), *arguments],
            capture_output=True, text=True, check=False,
        )
        if succeeds:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, 'Invalid artifacts were accepted')
        return result

    def artifact_hashes(self) -> dict[str, str]:
        paths = [*self.base.glob('diagrams/*.svg'), self.base / 'aws_fis_experiment_action_model.pdf',
                 self.base / 'tools/render-manifest.json']
        return {str(path.relative_to(self.base)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in paths}

    def test_check_does_not_modify_or_regenerate_artifacts(self) -> None:
        before = self.artifact_hashes()
        self.run_renderer('--check')
        self.assertEqual(self.artifact_hashes(), before)

    def test_svg_only_preserves_pdf_record_and_exposes_staleness(self) -> None:
        report = self.base / 'report.md'
        revised, count = re.subn(r'^version:.*$', 'version: "9.9"', report.read_text(), count=1, flags=re.M)
        self.assertEqual(count, 1)
        report.write_text(revised)
        before_pdf = (self.base / 'aws_fis_experiment_action_model.pdf').read_bytes()
        old = json.loads((self.base / 'tools/render-manifest.json').read_text())['report']
        self.run_renderer('--svg-only')
        manifest = json.loads((self.base / 'tools/render-manifest.json').read_text())
        self.assertEqual(manifest['report']['status'], 'stale')
        self.assertEqual(manifest['report']['sha256'], old['sha256'])
        self.assertEqual(manifest['report']['inputHashes'], old['inputHashes'])
        self.assertEqual((self.base / 'aws_fis_experiment_action_model.pdf').read_bytes(), before_pdf)
        self.run_renderer('--check', succeeds=False)
        self.run_renderer()
        self.run_renderer('--check')
        rebuilt = json.loads((self.base / 'tools/render-manifest.json').read_text())
        self.assertEqual(rebuilt['report']['version'], '9.9')

    def test_svg_only_checks_embedded_diagrams_before_writing(self) -> None:
        source = self.base / 'diagrams/01_execution.mmd'
        source.write_text(source.read_text().replace('string reason', 'string reasonText'))
        before = self.artifact_hashes()
        result = self.run_renderer('--svg-only', succeeds=False)
        self.assertIn('Markdown/Mermaid content mismatch', result.stderr)
        self.assertEqual(self.artifact_hashes(), before)

    def test_duplicate_source_urls_are_rejected(self) -> None:
        source_path = self.base / 'sources.json'
        register = json.loads(source_path.read_text())
        previous_url = register['sources'][1]['url']
        duplicate_url = register['sources'][0]['url']
        register['sources'][1]['url'] = duplicate_url
        source_path.write_text(json.dumps(register))
        report = self.base / 'report.md'
        report.write_text(report.read_text().replace(previous_url, duplicate_url))
        result = self.run_renderer('--check', succeeds=False)
        self.assertIn('Source URLs must be unique', result.stderr)

    def test_unknown_citations_are_rejected(self) -> None:
        report = self.base / 'report.md'
        report.write_text(report.read_text() + '\nAn unsupported statement. [S999]\n')
        result = self.run_renderer('--check', succeeds=False)
        self.assertIn('Unknown source citation: S999', result.stderr)

    def test_pdf_bytes_cannot_change_without_detection(self) -> None:
        output = self.base / 'aws_fis_experiment_action_model.pdf'
        output.write_bytes(output.read_bytes() + b'\n% changed artifact\n')
        before_manifest = (self.base / 'tools/render-manifest.json').read_bytes()
        self.run_renderer('--check', succeeds=False)
        self.assertEqual((self.base / 'tools/render-manifest.json').read_bytes(), before_manifest)

    def test_renderer_change_invalidates_the_pdf_build_record(self) -> None:
        renderer = self.base / 'tools/render_report.py'
        renderer.write_text(renderer.read_text() + '\n# Changed renderer input.\n')
        self.run_renderer('--check', succeeds=False)
        self.run_renderer('--svg-only')
        manifest = json.loads((self.base / 'tools/render-manifest.json').read_text())
        self.assertEqual(manifest['report']['status'], 'stale')
        self.run_renderer('--check', succeeds=False)


if __name__ == '__main__':
    unittest.main()
