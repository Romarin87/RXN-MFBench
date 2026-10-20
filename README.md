# RXN-MFBench

Models and simulation interfaces for reactive molecular systems containing carbon, hydrogen, nitrogen, and oxygen. RXN-MFBench compares direct and Δ-learning approaches to the target level **ωB97X-D/def2-TZVP**, using **GFN2-xTB** as the low-fidelity reference. The intended application is nonperiodic, neutral, closed-shell CHON chemistry.

## Start here

- [Models and downloads](model/README.md): architectures, training protocols, seeds, and checksums.
- [ASE interface](ase_interface/README.md): direct and Δ-model energy/force calculations with DeePMD and MACE.
- [ASH interface](ash_interface/README.md): DeePMD-based energy and gradient calculations.
- [ASH reaction-path examples](benchmark/README.md): NEB, transition-state optimization, and IRC.
- [Dataset on Hugging Face](https://huggingface.co/datasets/Romarin87/RXN-MFBench): training and evaluation data, units, provenance, and loading examples.

## Model release

[Release `models-v1.0.0`](https://github.com/Romarin87/RXN-MFBench/releases/tag/models-v1.0.0) contains **52 model files** across **DPA2, DPA3, DPA4-Neo, and MACE**. Each architecture provides one GFN2-xTB pretrained model and four higher-fidelity protocols with seeds `123`, `456`, and `789`.

| Protocol | Training | Inference |
|---|---|---|
| `pretrain` | GFN2-xTB total energies and forces | Direct low-fidelity prediction |
| `S` | From-scratch training on target DFT energies and forces | Direct target-level prediction |
| `F` | GFN2-xTB pretraining followed by direct DFT fine-tuning | Direct target-level prediction |
| `D` | From-scratch training on DFT − GFN2-xTB residuals | Learned residual + online GFN2-xTB |
| `DF` | GFN2-xTB pretraining followed by residual fine-tuning | Learned residual + online GFN2-xTB |

The `F` and `DF` seeds for an architecture share its released pretrained starting model. The DPA3 models in this release are single-task models.

For example, download one direct DPA4-Neo model from the repository root using the GitHub CLI:

```bash
gh release download models-v1.0.0 \
  --repo Romarin87/RXN-MFBench \
  --pattern DPA4-Neo-F-seed123.pt \
  --dir model
```

The [model catalog](model/models.json) records each filename, download URL, file size, SHA-256 checksum, and inference mode. See [model/SHA256SUMS](model/SHA256SUMS) for checksums.

## Related preprint

The earlier work is described in [*General reactive machine learning potentials for CHON elements* (2025)](https://chemrxiv.org/engage/chemrxiv/article-details/684ffe583ba0887c33dad39b).

```bibtex
@article{li2025general,
  title={General reactive machine learning potentials for CHON elements},
  author={Li, Bowen and Mi, Sixuan and Xiao, Jin and Zhang, Duo and Zhang, Shuwen and Zhang, John and Wang, Han and Zhu, Tong},
  year={2025}
}
```
