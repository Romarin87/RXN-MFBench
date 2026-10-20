# ASH interface

These interfaces expose DeePMD models as ASH theory objects for nonperiodic, neutral, closed-shell CHON molecules. Coordinates supplied to ASH are in Å. Returned energies are in hartree and gradients are in hartree/bohr.

## Setup and model selection

Follow the official [ASH setup guide](https://ash.readthedocs.io/en/latest/setup.html) and [DeePMD-kit installation guide](https://docs.deepmodeling.com/projects/deepmd/en/stable/install/index.html), selecting the PyTorch backend. The Δ interface also requires [xtb-python](https://xtb-python.readthedocs.io/en/latest/installation.html). The release environment uses ASH `0.99` at source revision [`f43c421f3bca48e3740bab7a10acb5a2676246a0`](https://github.com/RagnarB83/ash/tree/f43c421f3bca48e3740bab7a10acb5a2676246a0); see the [ASE guide](../ase_interface/README.md#dependencies) for the accompanying inference dependencies.

Run examples from the repository root and download the required weights into `model/` using the [model guide](../model/README.md).

| Interface | Model protocol | Output |
|---|---|---|
| `DPA4Theory(DPAdir=..., numcores=1)` | `S`, `F`, or `pretrain` | Direct model energy and gradient |
| `DPA4_xTBTheory(DPAdir=..., xtbmethod="GFN2-xTB", numcores=1)` | `D` or `DF` | Model residual + online GFN2-xTB energy and gradient |

`DPAdir` is the path to a model file. The retained class names use “DPA4”; the implementation loads DPA-family weights through DeePMD. ASH validation primarily covers DPA4-Neo. For MACE, use the [ASE interface](../ase_interface/README.md).

## Direct target-level calculation

```python
import ash
from ash_interface.interface_DPA4 import DPA4Theory

fragment = ash.Fragment(
    coordsstring="""O  0.000000  0.000000  0.000000
H  0.758602  0.000000  0.504284
H -0.758602  0.000000  0.504284""",
    charge=0,
    mult=1,
)
theory = DPA4Theory(
    DPAdir="model/DPA4-Neo-F-seed123.pt",
    numcores=1,
)
result = ash.Singlepoint(fragment=fragment, theory=theory, Grad=True)
print("Energy (hartree):", result.energy)
print("Gradient (hartree/bohr):", result.gradient)
```

The same interface loads `S` models for direct target-level prediction and `pretrain` models for direct GFN2-xTB-level prediction.

## Δ calculation with online GFN2-xTB

Using the same `fragment`, select a residual model and the matching theory object:

```python
from ash_interface.interface_DPA4_xTB import DPA4_xTBTheory

theory = DPA4_xTBTheory(
    DPAdir="model/DPA4-Neo-DF-seed123.pt",
    xtbmethod="GFN2-xTB",
    numcores=1,
)
result = ash.Singlepoint(fragment=fragment, theory=theory, Grad=True)
print("Energy (hartree):", result.energy)
print("Gradient (hartree/bohr):", result.gradient)
```

The Δ theory adds the learned energy and gradient residuals to the online baseline. Keep `xtbmethod="GFN2-xTB"` for these weights.

The theory objects' `run` methods return energy alone for `Grad=False` or `(energy, gradient)` for `Grad=True`. Gradients are converted from ASE forces using `gradient = -forces × Bohr / Hartree`. Their `charge` and `mult` arguments are accepted by `run` but are not forwarded to the xTB baseline; use the documented neutral closed-shell scope (`charge=0`, `mult=1`).
