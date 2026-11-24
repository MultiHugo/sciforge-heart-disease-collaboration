"""CPU baseline for SciForge workflow validation; not an official FLamby score."""
from pathlib import Path
import csv, hashlib, json, sys, urllib.request
import numpy as np

center, folder = sys.argv[1:3]
root = Path(folder)
root.mkdir(parents=True, exist_ok=True)
source = 'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.' + center + '.data'
data_path = root / ('processed.' + center + '.data')
if not data_path.exists():
    data_path.write_bytes(urllib.request.urlopen(source, timeout=20).read())
raw = data_path.read_bytes()
rows = list(csv.reader(raw.decode().splitlines()))
# FLamby removes columns 10-12 before dropping missing rows. Fixed category
# vocabulary makes the input schema consistent without sharing patient rows.
kept = [r[:10] + r[13:] for r in rows if '?' not in r[:10] + r[13:]]
a = np.asarray(kept, dtype=float)
y = (a[:, -1] > 0).astype(int)
numeric = [0, 1, 3, 4, 5, 7, 8, 9]
x = np.column_stack([a[:, numeric]] + [(a[:, 2] == v).astype(float) for v in [2, 3, 4]] + [(a[:, 6] == v).astype(float) for v in [1, 2]])
rng = np.random.default_rng(43)
train, test = [], []
for label in [0, 1]:
    ix = rng.permutation(np.flatnonzero(y == label))
    cut = int(np.floor(len(ix) * .66))
    train.extend(ix[:cut]); test.extend(ix[cut:])
train, test = np.array(train), np.array(test)
mean, std = x[train].mean(0), x[train].std(0)
std[std < 1e-9] = 1
xt = np.c_[np.ones(len(train)), (x[train] - mean) / std]
xv = np.c_[np.ones(len(test)), (x[test] - mean) / std]
w = np.zeros(xt.shape[1])
for _ in range(100):
    p = 1 / (1 + np.exp(-np.clip(xt @ w, -40, 40)))
    regularizer = np.diag([0] + [.01] * (len(w) - 1))
    grad = xt.T @ (p - y[train]) / len(train) + regularizer @ w
    hess = (xt.T * (p * (1-p))) @ xt / len(train) + regularizer
    delta = np.linalg.solve(hess + np.eye(len(w))*1e-10, grad)
    w -= delta
    if np.linalg.norm(delta) < 1e-9: break
scores = 1 / (1 + np.exp(-np.clip(xv @ w, -40, 40)))
positive, negative = scores[y[test] == 1], scores[y[test] == 0]
auc = float(((positive[:, None] > negative).sum() + .5*(positive[:, None] == negative).sum()) / (len(positive)*len(negative)))
metrics = dict(center=center, source=source, raw_sha256=hashlib.sha256(raw).hexdigest(), raw_rows=len(rows), retained_rows=len(a), train_rows=len(train), test_rows=len(test), positive_rate=float(y.mean()), auroc=auc, accuracy=float(((scores >= .5) == y[test]).mean()), seed=43, protocol='FLamby-inspired; custom NumPy stratified split, fixed categorical vocabulary, L2 logistic regression; NOT official FLamby scores', numpy=np.__version__, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(root/'metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
(root/'local-report.md').write_text('# '+center+' local baseline\n\n```json\n'+json.dumps(metrics, indent=2)+'\n```\n\nOnly aggregate metrics are approved for project delivery. Raw patient rows remain local. No federated training was executed.\n', encoding='utf-8')
print(json.dumps(metrics))
