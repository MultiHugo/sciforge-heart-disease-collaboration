"""Reproduce original numerical results without requiring a SciForge service."""
from pathlib import Path
import contextlib
import hashlib
import io
import json
import math
import runpy
import sys
import urllib.request
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'local_baseline.py'

def check_equal(actual, expected, label):
    if isinstance(expected, float):
        ok = math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-12)
    else:
        ok = actual == expected
    if not ok:
        raise ValueError(f'{label}: expected {expected!r}, received {actual!r}')

def main():
    work = ROOT / 'reproduced'
    checks = {}
    for center in ('cleveland', 'hungarian', 'va'):
        expected = json.loads((ROOT / 'results' / 'original' / f'{center}.json').read_text(encoding='utf-8'))
        check_equal(hashlib.sha256(SCRIPT.read_bytes()).hexdigest(), expected['script_sha256'], 'script SHA-256')
        folder = work / center
        folder.mkdir(parents=True, exist_ok=True)
        data = folder / f'processed.{center}.data'
        if not data.exists():
            with urllib.request.urlopen(expected['source'], timeout=30) as response:
                raw = response.read()
            check_equal(hashlib.sha256(raw).hexdigest(), expected['raw_sha256'], f'{center} download SHA-256')
            data.write_bytes(raw)
        check_equal(hashlib.sha256(data.read_bytes()).hexdigest(), expected['raw_sha256'], f'{center} data SHA-256')
        saved_argv = sys.argv
        try:
            sys.argv = [str(SCRIPT), center, str(folder)]
            with contextlib.redirect_stdout(io.StringIO()):
                ns = runpy.run_path(str(SCRIPT), run_name='__main__')
        finally:
            sys.argv = saved_argv
        actual = ns['metrics']
        for field in ('center', 'source', 'raw_sha256', 'raw_rows', 'retained_rows', 'train_rows', 'test_rows', 'positive_rate', 'auroc', 'accuracy', 'seed', 'protocol', 'script_sha256'):
            check_equal(actual[field], expected[field], f'{center}.{field}')
        checks[center] = {'status': 'PASS', 'auroc': actual['auroc'], 'accuracy': actual['accuracy']}
        if center == 'va':
            y = ns['y'][ns['test']]
            pred = ns['scores'] >= .5
            audit = dict(retained_positive=int(ns['y'].sum()), retained_total=len(ns['y']),
                test_total=len(y), test_positive=int(y.sum()), test_negative=int((y == 0).sum()),
                test_positive_rate=float(y.mean()), predicted_positive=int(pred.sum()),
                predicted_negative=int((~pred).sum()), predicted_positive_rate=float(pred.mean()),
                true_positive=int(((y == 1) & pred).sum()), false_negative=int(((y == 1) & ~pred).sum()),
                true_negative=int(((y == 0) & ~pred).sum()), false_positive=int(((y == 0) & pred).sum()),
                accuracy=float((pred == y).mean()), auroc=ns['auc'], all_positive_accuracy=float(y.mean()))
            original_audit = json.loads((ROOT / 'results/supplementary/va-test-distribution-20261122.json').read_text(encoding='utf-8'))
            for field, value in audit.items():
                check_equal(value, original_audit[field], f'va-audit.{field}')
            (work / 'va-test-distribution.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
            checks['va_supplementary'] = {'status': 'PASS', **audit}
        print(f'{center}: PASS (AUROC={actual["auroc"]:.4f}, accuracy={actual["accuracy"]:.4f})')
    report = {'status': 'PASS', 'numpy': np.__version__, 'original_numpy': '2.4.1', 'checks': checks}
    (work / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('VA supplementary distribution: PASS; all numerical checks passed.')

if __name__ == '__main__':
    main()
