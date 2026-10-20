# ASE interface

Use these calculators for nonperiodic, neutral, closed-shell CHON molecules. Coordinates are in Å, energies in eV, and forces in eV/Å. Forces are the negative energy gradient.

## Dependencies

Install [ASE](https://docs.ase-lib.org/), plus the runtime for the selected architecture: [DeePMD-kit with its PyTorch backend](https://docs.deepmodeling.com/projects/deepmd/en/stable/install/index.html) for DPA2, DPA3, and DPA4-Neo, or [MACE](https://mace-docs.readthedocs.io/en/latest/guide/installation.html). Δ inference additionally requires [xtb-python and its xTB library](https://xtb-python.readthedocs.io/en/latest/installation.html).

The release smoke checks used these environments:

| Runtime | Model package | PyTorch | ASE | xtb-python |
|---|---|---|---|---|
| DPA | DeePMD-kit `3.2.0` | `2.11.0+cu128` | `3.29.0` | `22.1` |
| MACE | mace-torch `0.3.16` | `2.8.0+cu126` | `3.29.0` | `22.1` |

Use the official installation guides to select dependencies compatible with your hardware. Run the examples from the repository root, with the selected weights downloaded into `model/` as described in the [model guide](../model/README.md).

## Choose a calculator

| Model protocol | DPA2 / DPA3 / DPA4-Neo | MACE |
|---|---|---|
| `S`, `F`, or `pretrain` | `ase_interface.deepmd_direct.DPCalculator` | `ase_interface.mace_direct.MACECalculator` |
| `D` or `DF` | `ase_interface.deepmd_xtb.DP_xTB` | `ase_interface.mace_xtb.MACE_xTB` |

The direct modules re-export the native DeePMD and MACE calculators. Direct `S`/`F` models predict the target DFT total; direct `pretrain` models predict the GFN2-xTB total.

## Direct prediction

DPA example:

```python
from ase.build import molecule
from ase_interface.deepmd_direct import DPCalculator

atoms = molecule("H2O")
atoms.calc = DPCalculator(
    model="model/DPA4-Neo-F-seed123.pt",
    device="cpu",
)
print("Energy (eV):", atoms.get_potential_energy())
print("Forces (eV/Å):", atoms.get_forces())
```

MACE example:

```python
from ase.build import molecule
from ase_interface.mace_direct import MACECalculator

atoms = molecule("H2O")
atoms.calc = MACECalculator(
    model_paths="model/MACE-F-seed123.model",
    device="cpu",
)
print("Energy (eV):", atoms.get_potential_energy())
print("Forces (eV/Å):", atoms.get_forces())
```

## Δ prediction with online GFN2-xTB

The `D` and `DF` weights predict DFT − GFN2-xTB residuals. These wrappers add both the energy correction and the force correction to an online GFN2-xTB calculation.

DPA example:

```python
from ase.build import molecule
from ase_interface.deepmd_xtb import DP_xTB

atoms = molecule("H2O")
atoms.calc = DP_xTB(model="model/DPA4-Neo-DF-seed123.pt")
print("Energy (eV):", atoms.get_potential_energy())
print("Forces (eV/Å):", atoms.get_forces())
```

`DP_xTB` delegates device selection to DeePMD's `DeepPot`; its extra keyword arguments do not set the `DeepPot` device. To restrict a script named `example.py` to CPU, set GPU visibility before Python starts:

```bash
CUDA_VISIBLE_DEVICES="" python example.py
```

MACE example:

```python
from ase.build import molecule
from ase_interface.mace_xtb import MACE_xTB

atoms = molecule("H2O")
atoms.calc = MACE_xTB(
    model_path="model/MACE-DF-seed123.model",
    device="cpu",
)
print("Energy (eV):", atoms.get_potential_energy())
print("Forces (eV/Å):", atoms.get_forces())
```

Both Δ wrappers default to `method="GFN2-xTB"`, matching the training baseline. Their implemented properties are `energy`, `free_energy`, and `forces`; `free_energy` equals `energy`. Stress is not implemented. Model and xTB calculation errors propagate to the caller.

To read your own nonperiodic geometry, replace `molecule("H2O")` with `ase.io.read("structure.xyz")`, then attach the selected calculator. Keep the molecule neutral and closed-shell and preserve its intended atom order.
