# ASH NEB

Complete the [shared setup](../README.md). Place preoptimized reactant and product geometries in `initial.xyz` and `final.xyz` in this directory. They must contain the same atoms in matching atom order.

From the repository root:

```bash
cd benchmark/NEB
python run_neb.py
```

`ash.NEB` runs climbing-image NEB with seven intermediate images (nine images including the endpoints). The saddle-point fragment is saved as `ts_guess.xyz`; if ASH returns no saddle-point fragment, the script raises an error. Inspect NEB convergence before using this guess.

To continue with [TS optimization](../TSOpt/README.md), from this directory:

```bash
cp ts_guess.xyz ../TSOpt/ts_guess.xyz
cd ../TSOpt
python run_tsopt.py
```
