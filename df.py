import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import qcelemental as qcel


def sum_energies(e):
    if type(e) == float:
        return e
    else:
        return e[0]


def s22_df():
    df = pd.read_pickle("s22.pkl")
    print("CCSD data")
    energy_cols = [
        # "dlpno_ccsd_adz",
        "dlpno_ccsd_adz_orca_loosePNO",
        "dlpno_ccsd_adz_orca_normalPNO",
        "dlpno_ccsd_adz_orca_tightPNO",
        "dlpno_ccsd_adz_orca_veryTightPNO",
    ]
    pd.set_option("display.max_columns", None)
    conv = qcel.constants.conversion_factor("hartree", "kcal/mol")
    df[energy_cols] = df[energy_cols] * conv
    # Energy cell = [IE Energy, Dimer Energy, Monomer 1 Energy, Monomer 2 Energy]
    energy_cols_ie = [f"{i}_IE" for i in energy_cols]
    for n, i in enumerate(energy_cols):
        df[energy_cols_ie[n]] = df[i].apply(lambda x: x[0])
    print(df[["sys_ind", *energy_cols_ie]])

    print("CCSD CP data")
    energy_cols = [
        # "dlpno_ccsd_adz",
        "dlpno_ccsd_adz_orca_loosePNO_CP",
        "dlpno_ccsd_adz_orca_normalPNO_CP",
        "dlpno_ccsd_adz_orca_tightPNO_CP",
        "dlpno_ccsd_adz_orca_veryTightPNO_CP",
    ]
    conv = qcel.constants.conversion_factor("hartree", "kcal/mol")
    df[energy_cols] = df[energy_cols] * conv
    # Energy cell = [IE Energy, Dimer Energy, Monomer 1 Energy, Monomer 2 Energy]
    energy_cols_ie = [f"{i}_IE" for i in energy_cols]
    for n, i in enumerate(energy_cols):
        df[energy_cols_ie[n]] = df[i].apply(lambda x: sum_energies(x))
    print(df[["sys_ind", *energy_cols_ie]])

    print("CCSD(T) data")
    energy_cols = [
        # "dlpno_ccsd_adz",
        "dlpno_ccsd_t_adz_orca_loosePNO",
        "dlpno_ccsd_t_adz_orca_normalPNO",
        "dlpno_ccsd_t_adz_orca_tightPNO",
        "dlpno_ccsd_t_adz_orca_veryTightPNO",
    ]
    conv = qcel.constants.conversion_factor("hartree", "kcal/mol")
    df[energy_cols] = df[energy_cols] * conv
    # Energy cell = [IE Energy, Dimer Energy, Monomer 1 Energy, Monomer 2 Energy]
    energy_cols_ie = [f"{i}_IE" for i in energy_cols]
    for n, i in enumerate(energy_cols):
        df[energy_cols_ie[n]] = df[i].apply(lambda x: sum_energies(x))
    print(df[["sys_ind", *energy_cols_ie]])

    print("CCSD(T) CP data")
    energy_cols = [
        # "dlpno_ccsd_adz",
        "dlpno_ccsd_t_adz_orca_loosePNO_CP",
        "dlpno_ccsd_t_adz_orca_normalPNO_CP",
        "dlpno_ccsd_t_adz_orca_tightPNO_CP",
        "dlpno_ccsd_t_adz_orca_veryTightPNO_CP",
    ]
    conv = qcel.constants.conversion_factor("hartree", "kcal/mol")
    df[energy_cols] = df[energy_cols] * conv
    # Energy cell = [IE Energy, Dimer Energy, Monomer 1 Energy, Monomer 2 Energy]
    energy_cols_ie = [f"{i}_IE" for i in energy_cols]
    for n, i in enumerate(energy_cols):
        df[energy_cols_ie[n]] = df[i].apply(lambda x: sum_energies(x))
    print(df[["sys_ind", *energy_cols_ie]])
    return


def main():
    """
    Read in s22 df for analysis
    """
    s22_df()
    return


if __name__ == "__main__":
    main()
