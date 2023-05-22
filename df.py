import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import qcelemental as qcel


def main():
    """
    Read in s22 df for analysis
    """
    df = pd.read_pickle("s22.pkl")
    print(df.columns.values)
    energy_cols = [
        "dlpno_ccsd_adz",
        "dlpno_ccsd_adz_orca_loosePNO",
        "dlpno_ccsd_adz_orca_normalPNO",
        "dlpno_ccsd_adz_orca_tightPNO",
    ]
    conv = qcel.constants.conversion_factor("hartree", "kcal/mol")
    df[energy_cols] = df[energy_cols] * conv
    # Energy cell = [IE Energy, Dimer Energy, Monomer 1 Energy, Monomer 2 Energy]
    energy_cols_ie = [f"{i}_IE" for i in energy_cols]
    for n, i in enumerate(energy_cols):
        df[energy_cols_ie[n]] = df[i].apply(lambda x: x[0])
    print(df[['sys_ind', *energy_cols_ie]])
    return


if __name__ == "__main__":
    main()
