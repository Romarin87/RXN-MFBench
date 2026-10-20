# Models

Download weights from [GitHub Release `models-v1.0.0`](https://github.com/Romarin87/RXN-MFBench/releases/tag/models-v1.0.0). The release contains 52 files: four architectures × (one pretrained model + four protocols × three seeds).

## Architectures and filenames

| Architecture | Runtime | Higher-fidelity filename | Pretrained filename |
|---|---|---|---|
| DPA2 | DeePMD PyTorch | `DPA2-<protocol>-seed<seed>.pt` | `DPA2-pretrain.pt` |
| DPA3 | DeePMD PyTorch | `DPA3-<protocol>-seed<seed>.pt` | `DPA3-pretrain.pt` |
| DPA4-Neo | DeePMD PyTorch | `DPA4-Neo-<protocol>-seed<seed>.pt` | `DPA4-Neo-pretrain.pt` |
| MACE | MACE | `MACE-<protocol>-seed<seed>.model` | `MACE-pretrain.model` |

Choose protocol `S`, `F`, `D`, or `DF` and seed `123`, `456`, or `789`. DPA3 is single-task. Each architecture has one shared pretrained starting model for its `F` and `DF` fine-tuning runs; the filename seeds identify the higher-fidelity runs.

## Training targets and inference

The target method is **ωB97X-D/def2-TZVP**; the low-fidelity method is **GFN2-xTB**. Models are intended for nonperiodic, neutral, closed-shell molecules containing C, H, N, and O.

| Protocol | Initialization and training target | Calculator to use |
|---|---|---|
| `pretrain` | GFN2-xTB total energies and forces | Direct |
| `S` | From scratch; DFT total energies and forces | Direct |
| `F` | GFN2-xTB pretraining; fine-tune on DFT total energies and forces | Direct |
| `D` | From scratch; DFT − GFN2-xTB energy and force residuals | Δ + GFN2-xTB |
| `DF` | GFN2-xTB pretraining; fine-tune on DFT − GFN2-xTB energy and force residuals | Δ + GFN2-xTB |

For `D` and `DF`, inference combines the learned correction with an online GFN2-xTB calculation at the same geometry:

```text
E = E(GFN2-xTB) + ΔE(model)
F = F(GFN2-xTB) + ΔF(model)
```

A native calculator used alone on a `D` or `DF` weight returns the learned residual. The provided Δ interfaces perform the addition. A pretrained model used directly predicts the low-fidelity total.

## Download and verify

Run these commands from the repository root to download a specific file:

```bash
gh release download models-v1.0.0 \
  --repo Romarin87/RXN-MFBench \
  --pattern DPA4-Neo-DF-seed123.pt \
  --dir model
```

For MACE, choose a `.model` asset, for example:

```bash
gh release download models-v1.0.0 \
  --repo Romarin87/RXN-MFBench \
  --pattern MACE-F-seed123.model \
  --dir model
```

Files can also be downloaded individually from the release page. Load model files only from sources you trust, and verify their checksums before loading.

The machine-readable [models.json](models.json) uses schema version `1`, with top-level `release_tag`, `release_url`, and `models` fields. Each model record contains:

- `architecture`, `protocol`, and `seed` (`null` for pretrained models).
- `filename`, `bytes`, `sha256`, and `url`.
- `prediction`: `direct` or `delta_plus_xtb`.
- `target`: `GFN2-xTB` or `ωB97X-D/def2-TZVP`.

[SHA256SUMS](SHA256SUMS) provides the same checksums in standard checksum-file format. To verify one downloaded file using only Python's standard library:

```python
import hashlib
import json
from pathlib import Path

filename = "DPA4-Neo-DF-seed123.pt"
catalog = json.loads(Path("model/models.json").read_text())
entry = next(item for item in catalog["models"] if item["filename"] == filename)
path = Path("model") / filename
assert path.stat().st_size == entry["bytes"], "File size mismatch"
digest = hashlib.sha256()
with path.open("rb") as handle:
    for block in iter(lambda: handle.read(1024 * 1024), b""):
        digest.update(block)
assert digest.hexdigest() == entry["sha256"], "SHA-256 mismatch"
print("Verified:", filename)
```

Continue with the [ASE examples](../ase_interface/README.md) or [ASH examples](../ash_interface/README.md).

## Earlier model files

The five earlier weights retain their original filenames and mappings for compatibility:

| Original filename | Original mapping |
|---|---|
| `DPA-3-F.pt` | Direct DFT-level model |
| `DPA-3-DF.pt` | DFT-level Δ model |
| `DPA-3-F@DeePHF.pt` | Direct DeePHF-level model |
| `DPA-3-DF@DeePHF.pt` | DeePHF-level Δ model |
| `DPA-3-pretrain.pt` | Pretrained model |

For the earlier DeePHF models, the explicitly selected head is `CC`. The versioned release uses the architecture/protocol/seed naming scheme above.
