# SPDX-License-Identifier: LGPL-3.0-or-later
"""ASE calculator interface module."""


from ase.calculators.calculator import (
    Calculator,
    all_changes,
)
from pathlib import (
    Path,
)
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Optional,
    Union,
)
if TYPE_CHECKING:
    from ase import (
        Atoms,
    )
from xtb.ase.calculator import XTB
from mace.calculators import MACECalculator




class MACE_xTB(Calculator):
    name = "MACE_xTB"
    implemented_properties: ClassVar[list[str]] = [
        "energy",
        "free_energy",
        "forces",
    ]
    def __init__(
        self,
        model_path: Union[str, "Path"],
        method="GFN2-xTB",
        label: str = "MACE_xTB",
        device: str = "cpu",
        **kwargs,
    ) -> None:
        Calculator.__init__(self, label=label, **kwargs)
        self.mace = MACECalculator(model_paths=model_path, device=device)
        self.xtb = XTB(method=method)


    def calculate(
        self,
        atoms: Optional["Atoms"] = None,
        properties: list[str] = ["energy", "forces"],
        system_changes: list[str] = all_changes,
    ) -> None:

        if atoms is not None:
            self.atoms = atoms.copy()

        self.atoms.calc = self.xtb
        xtb_e, xtb_f = self.atoms.get_potential_energy(), self.atoms.get_forces()
        self.atoms.calc = self.mace
        mace_e, mace_f = self.atoms.get_potential_energy(), self.atoms.get_forces()
        self.results["energy"] = mace_e + xtb_e
        self.results["free_energy"] = mace_e + xtb_e
        self.results["forces"] = mace_f + xtb_f
        self.xtb.reset()

