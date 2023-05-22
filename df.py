import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import qcelemental as qcel


def main():
    """
    Read in s22 df for analysis
    """
    df = pd.read_pickle("s22.pkl")
    energy_cols = [
        "dlpno_ccsd_adz",
        "dlpno_ccsd_adz_orca_loosePNO",
        "dlpno_ccsd_adz_orca_normalPNO",
        "dlpno_ccsd_adz_orca_tightPNO",
    ]
    conv = qcel.constants.conversion_factor("hartree", "kcal/mol")
    df[energy_cols] = df[energy_cols] * conv
    # Energy cell = [IE Energy, Dimer Energy, Monomer 1 Energy, Monomer 2 Energy]
    print(df['dlpno_ccsd_adz_orca_tightPNO'])
    return


if __name__ == "__main__":
    main()
