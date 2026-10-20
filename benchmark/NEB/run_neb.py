#!/usr/bin/env python3
"""Run from benchmark/NEB with preoptimized initial.xyz and final.xyz."""

import sys
from pathlib import Path

import ash

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))
from ash_interface.interface_DPA4_xTB import DPA4_xTBTheory

model = repo_root / "model" / "DPA4-Neo-DF-seed123.pt"
theory = DPA4_xTBTheory(DPAdir=str(model), numcores=1)
reactant = ash.Fragment(xyzfile="initial.xyz", charge=0, mult=1)
product = ash.Fragment(xyzfile="final.xyz", charge=0, mult=1)

# ASH counts intermediate images: seven here, plus the two endpoints.
result = ash.NEB(
    reactant=reactant, product=product, theory=theory,
    images=7, CI=True, runmode="serial", numcores=1,
)
if result.saddlepoint_fragment is None:
    raise RuntimeError("NEB returned no saddle-point fragment; inspect convergence.")
result.saddlepoint_fragment.write_xyzfile(xyzfilename="ts_guess.xyz")
