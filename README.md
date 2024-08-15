# DLPNO-Testing

- testing with ORCA vs. psi4 against S22
- testing with psi4 on NBC10 for dispersion correction

## NBC10 Dispersion Corrections

DLPNO-CCSD(T) with aDZ and aTZ are run on NBC10 using hrcl_jobs and qm_db. Error statistics
against CCSD(T)/CBS are shown in plot below where DLPNO-CCSD(T)/aTZ with normal PNO_CONVERGENCE
performs similarly to TIGHT PNO_CONVERGENCE (at reduced costs).

![dlpno_nbc10_dispersion_test_img](./plots/dlpno_nbc10_testing_violin.jpg)

### Objectives - Dispersion correction

- [x] DLPNO-CCSD(T)/aug-cc-pVDZ \[PNO=Normal] on NBC10 
- [x] DLPNO-CCSD(T)/aug-cc-pVTZ \[PNO=Tight]  on NBC10 
- [x] DLPNO-CCSD(T)/aug-cc-pVTZ \[PNO=Normal] on NBC10 
- [ ] DLPNO-CCSD(T)/aug-cc-pVTZ \[PNO=Tight]  on NBC10 
- [ ] run DLPNO-CCSD(T)/CBS:
  - does that mean...
    1.  "MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvdz"
    2.  "MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvtz"
    3.  "MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvdz" PNO=TIGHT
    4.  "MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvtz" PNO=TIGHT
    5.  "DLPNO-MP2/aug-cc-pV[T,Q]Z + D:DLPNO-CCSD(T)/cc-pvdz" PNO=NORMAL
