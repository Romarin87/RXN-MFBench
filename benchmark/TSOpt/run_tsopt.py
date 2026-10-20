#!/usr/bin/env python3
"""Run from benchmark/TSOpt with a transition-state guess in ts_guess.xyz."""

import sys
from pathlib import Path

import ash

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))
from ash_interface.interface_DPA4_xTB import DPA4_xTBTheory

model = repo_root / "model" / "DPA4-Neo-DF-seed123.pt"
theory = DPA4_xTBTheory(DPAdir=str(model), numcores=1)
ts = ash.Fragment(xyzfile="ts_guess.xyz", charge=0, mult=1)

ash.Optimizer(theory=theory, fragment=ts, TSOpt=True)
ts.write_xyzfile(xyzfilename="ts_optimized.xyz")
