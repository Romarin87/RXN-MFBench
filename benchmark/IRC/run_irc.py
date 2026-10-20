#!/usr/bin/env python3
"""Run from benchmark/IRC with a first-order saddle in ts_optimized.xyz."""

import sys
from pathlib import Path

import ash

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))
from ash_interface.interface_DPA4_xTB import DPA4_xTBTheory

model = repo_root / "model" / "DPA4-Neo-DF-seed123.pt"
theory = DPA4_xTBTheory(DPAdir=str(model), numcores=1)
ts = ash.Fragment(xyzfile="ts_optimized.xyz", charge=0, mult=1)

frequency = ash.NumFreq(
    theory=theory, fragment=ts, npoint=2, runmode="serial", numcores=1,
)
ash.Optimizer(
    theory=theory, fragment=ts, irc=True,
    hessian=frequency.hessian, maxiter=500,
)
