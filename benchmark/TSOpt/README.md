# ASH transition-state optimization

Complete the [shared setup](../README.md). Place a transition-state guess in `ts_guess.xyz` in this directory, for example the output of the [NEB example](../NEB/README.md).

From the repository root:

```bash
cd benchmark/TSOpt
python run_tsopt.py
```

`ash.Optimizer(..., TSOpt=True)` refines the guess with geomeTRIC and saves `ts_optimized.xyz`. Check convergence and confirm a first-order saddle: exactly one imaginary vibrational mode corresponding to the intended reaction.

To continue with [IRC](../IRC/README.md), from this directory:

```bash
cp ts_optimized.xyz ../IRC/ts_optimized.xyz
cd ../IRC
python run_irc.py
```
