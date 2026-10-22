#!/usr/bin/env python3
"""Run native guided acceptance; retain bounded selector diagnostics on failure.

The existing assertions and CSP are unchanged. No credentials or form values
outside the two AWS read selectors are captured.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import Locator, Browser

ROOT = Path(__file__).resolve().parents[1]
original_select = Locator.select_option
original_page = Browser.new_page
errors = []


def page_with_errors(self, *args, **kwargs):
    page = original_page(self, *args, **kwargs)
    page.on('pageerror', lambda error: errors.append(str(error)[:1500]))
    return page


def inspected_select(self, *args, **kwargs):
    try:
        return original_select(self, *args, **kwargs)
    except Exception:
        details = {'page_errors': errors[-8:]}
        try:
            details['selectors'] = self.page.locator(
                'select[aria-label="AWS read service"], '
                'select[aria-label="Read operation"]').evaluate_all(
                    '(nodes)=>nodes.map(n=>({label:n.getAttribute("aria-label"),'
                    'value:n.value,disabled:n.disabled,options:[...n.options].map(o=>o.value)}))')
        except Exception as error:
            details['diagnostic_error'] = type(error).__name__
        target = ROOT/'validation'/'setup-selector-diagnostics.json'
        target.parent.mkdir(exist_ok=True)
        target.write_text(json.dumps(details, indent=2)+'\n', encoding='utf-8')
        print('SETUP SELECTOR DIAGNOSTICS '+json.dumps(details), flush=True)
        raise


if __name__ == '__main__':
    Locator.select_option = inspected_select
    Browser.new_page = page_with_errors
    from setup_browser_checks import main
    sys.argv = [sys.argv[0], '--native']
    main()
