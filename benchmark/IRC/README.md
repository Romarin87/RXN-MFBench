# ASH IRC

Complete the [shared setup](../README.md). Place an optimized first-order saddle in `ts_optimized.xyz` in this directory, for example from the [TS optimization example](../TSOpt/README.md).

From the repository root:

```bash
cd benchmark/IRC
python run_irc.py
```

`ash.NumFreq` calculates the numerical Hessian, which is passed to `ash.Optimizer(..., irc=True)` for geomeTRIC IRC propagation. Inspect the reported frequencies: the TS should have exactly one imaginary vibrational mode along the intended reaction coordinate.

The IRC trajectory is written to `geometric_OPTtraj_irc.xyz`. Inspect the path and confirm that its endpoints connect to the intended reactant and product.
