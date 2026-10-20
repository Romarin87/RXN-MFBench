import os
import numpy as np
from ash.functions.functions_general import ashexit, blankline,reverse_lines, print_time_rel,BC, print_line_with_mainheader,print_if_level
import ase.atoms
from ase.units import Bohr,Hartree
import warnings
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
class DPA4Theory:
    def __init__(self, DPAdir=None,numcores=1):
        self.theorynamelabel="DPA4"
        self.theorytype="NN"

        self.numcores=numcores
        self.DPAdir=DPAdir



        print_line_with_mainheader("DPA4 INTERFACE")
        print("DPA4 model", self.DPAdir)
        print("DPA4 object numcores:", self.numcores)

        os.environ["OMP_NUM_THREADS"] = str(self.numcores)
        os.environ ['OPENBLAS_NUM_THREADS'] = str(self.numcores)
        os.environ ['MKL_NUM_THREADS'] = str(self.numcores)
        os.environ ['VECLIB_MAXIMUM_THREADS'] = str(self.numcores)
        os.environ ['NUMEXPR_NUM_THREADS'] = str(self.numcores)
        os.environ ['TF_INTRA_OP_PARALLELISM_THREADS'] = str(self.numcores)
        os.environ ['TF_INTER_OP_PARALLELISM_THREADS'] = str(self.numcores)

        try:
            from deepmd.pt.utils.ase_calc import DPCalculator
            self.calc_dp = DPCalculator(model = self.DPAdir)
        except Exception as e:
            print("Problem importing DPA4.")
            print("Full error message:", e)
            ashexit(code=9)
    
    def set_numcores(self, numcores):
        self.numcores = numcores

    def run(self, current_coords=None, elems=None, numcores=None, label=None, Grad=False, charge=None, mult=None):

        if numcores is None:
            numcores=self.numcores

        assert len(current_coords) == len(elems)        
        aseatom = ase.atoms.Atoms(elems,positions=np.array(current_coords))

        aseatom.calc = self.calc_dp
        aseatom.set_cell([10,10,10])
        self.energy_dp,self.grad_dp = aseatom.get_potential_energy()/Hartree, aseatom.get_forces()*Bohr/Hartree*-1
        if Grad:
            return self.energy_dp, self.grad_dp
        return self.energy_dp
