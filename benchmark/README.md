# ASH reaction-path examples

Minimal editable examples for nonperiodic, neutral, closed-shell CHON systems:

- [NEB](NEB/README.md): reactant and product → `ts_guess.xyz`.
- [TS optimization](TSOpt/README.md): TS guess → `ts_optimized.xyz`.
- [IRC](IRC/README.md): optimized TS → reaction-path trajectory.

## Setup

Install the dependencies described in the [ASH interface guide](../ash_interface/README.md), including ASH and geomeTRIC. See the [model guide](../model/README.md) for model choices and checksums. From the repository root, download the default Δ-learning model:

```bash
gh release download models-v1.0.0 \
  --repo Romarin87/RXN-MFBench \
  --pattern DPA4-Neo-DF-seed123.pt \
  --dir model
```

The scripts load `model/DPA4-Neo-DF-seed123.pt` relative to the repository root and read geometry files from the current working directory. Supply your own XYZ inputs and run each script from its stage directory. All examples use `charge=0`, `mult=1`, and one core; edit the Python scripts to change settings.

The D/DF weights require `DPA4_xTBTheory`, which combines the learned correction with online GFN2-xTB. For a direct S/F model, replace the theory import and initialization, for example:

```python
from ash_interface.interface_DPA4 import DPA4Theory

model = repo_root / "model" / "DPA4-Neo-F-seed123.pt"
theory = DPA4Theory(DPAdir=str(model), numcores=1)
```

Download that model separately before running. Use a consistent model throughout the path calculation. Check optimization convergence, confirm that the TS has exactly one imaginary vibrational mode along the intended reaction coordinate, and check that the IRC endpoints connect to the intended reactant and product.

ASH documentation: [NEB](https://ash.readthedocs.io/en/latest/neb.html) and [geomeTRIC optimization/IRC](https://ash.readthedocs.io/en/latest/geometric_interface.html).
