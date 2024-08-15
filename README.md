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

# DLPNO-CCSD Interaction Energy Notes
## PNO Extrapolations
[Neese extrapolation PNO paper](https://pubs.acs.org/doi/10.1021/acs.jctc.0c00344) 
DLPNO-CCSD(T) energies in Figure 4 in section 3.2. Seems like the Extr.(6/7)
meaning T_cutPNO = 10^-6 and T_cutPNO = 10^-7 is the best with only a little
improvement from aDZ to aQZ. 

[A recent Herbert paper (2024)](https://pubs.aip.org/aip/jcp/article/161/5/054114/3306675)
investigates this Neese extrapolation further on much larger systems (S12L, L7,
PAHs, and graphanes) along with S66.
