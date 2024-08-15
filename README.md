# DLPNO-Testing 
- testing with ORCA vs. psi4 against S22
- testing with psi4 on NBC10 for dispersion correction

# Objectives - Dispersion correction
[./plots/dlpno_nbc10_testing_violin.jpg]
- [ ] Finish TIGHT
- [ ] run DLPNO-CCSD(T)/CBS: 
    - does that mean:
       1. "MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvdz"
       2. "MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvtz"
       3. "MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvdz" PNO=TIGHT
       4. "MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvtz" PNO=TIGHT
