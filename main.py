import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import hrcl_jobs as hrcl
import os
from pprint import pprint as pp
from qcelemental import constants

h2kcalmol = constants.hartree2kcalmol


def collect_dlpno_df():
    db_pw_path = os.path.expanduser("~/dbs/qmdb_pw.txt")
    port = 5434
    dbname = "qm_db"
    con = hrcl.pgsql.connect_to_db(
        db_pw_path, port=port, ip_db="localhost", dbname=dbname, return_con=True
    )
    cur = con.cursor()
    cur.execute(
        """SELECT * FROM los.los_all JOIN los.schriber ON los.los_all.id = los.schriber.original_id
        where "benchmark ref energy" is not null;"""
    )
    df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
    for col in df.columns:
        if isinstance(df.iloc[0], list):
            df[col] = df[col].apply(lambda x: np.array(x))
    df.to_pickle("./dfs/los_all.pkl")
    return df


def plot_dlpno_results(df, limit_to_column_not_nan=None):
    if limit_to_column_not_nan is not None:

        size_prior = len(df)
        df = df[df[limit_to_column_not_nan].notna()].copy()
        print(
            f"Limiting to {limit_to_column_not_nan} not NaN: {size_prior} -> {len(df)}"
        )
    reference = "benchmark ref energy"
    copy_cols_start = [
        "DB",
        "system_id",
        "benchmark ref energy",
        ## DLPNO-CCSD
        # adz normal
        # "DLPNO_CCSD_IE_adz",
        # "DLPNO_CCSD_IE_adz_CCSD_E",
        # "DLPNO_CCSD_IE_adz_CCSD_Cor",
        # "DLPNO_CCSD_IE_adz_CCSD_T_E",
        # "DLPNO_CCSD_IE_adz_CCSD_T_Cor",
        # "DLPNO_CCSD_IE_adz_CCSD_Disp",
        # "DLPNO_CCSD_IE_TIGHT_adz",
        # # adz tight
        # "DLPNO_CCSD_IE_TIGHT_adz_CCSD_E",
        # "DLPNO_CCSD_IE_TIGHT_adz_CCSD_Cor",
        # "DLPNO_CCSD_IE_TIGHT_adz_CCSD_T_E",
        # "DLPNO_CCSD_IE_TIGHT_adz_CCSD_T_Cor",
        # "DLPNO_CCSD_IE_TIGHT_adz_CCSD_Disp",
        # # atz normal
        # "DLPNO_CCSD_IE_atz",
        # "DLPNO_CCSD_IE_atz_CCSD_E",
        # "DLPNO_CCSD_IE_atz_CCSD_Cor",
        # "DLPNO_CCSD_IE_atz_CCSD_T_E",
        # "DLPNO_CCSD_IE_atz_CCSD_T_Cor",
        # "DLPNO_CCSD_IE_atz_CCSD_Disp",
        # # atz tight
        # "DLPNO_CCSD_IE_TIGHT_atz",
        # "DLPNO_CCSD_IE_TIGHT_atz_CCSD_E",
        # "DLPNO_CCSD_IE_TIGHT_atz_CCSD_Cor",
        # "DLPNO_CCSD_IE_TIGHT_atz_CCSD_T_E",
        # "DLPNO_CCSD_IE_TIGHT_atz_CCSD_T_Cor",
        # "DLPNO_CCSD_IE_TIGHT_atz_CCSD_Disp",
        ## DLPNO-CCSD(T)
        # adz normal
        "DLPNO_CCSD_T_IE_adz",
        "DLPNO_CCSD_T_IE_adz_CCSD_E",
        "DLPNO_CCSD_T_IE_adz_CCSD_Cor",
        "DLPNO_CCSD_T_IE_adz_CCSD_T_E",
        "DLPNO_CCSD_T_IE_adz_CCSD_T_Cor",
        "DLPNO_CCSD_T_IE_adz_CCSD_Disp",
        "DLPNO_CCSD_T_IE_TIGHT_adz",
        # adz tight
        "DLPNO_CCSD_T_IE_TIGHT_adz_CCSD_E",
        "DLPNO_CCSD_T_IE_TIGHT_adz_CCSD_Cor",
        "DLPNO_CCSD_T_IE_TIGHT_adz_CCSD_T_E",
        "DLPNO_CCSD_T_IE_TIGHT_adz_CCSD_T_Cor",
        "DLPNO_CCSD_T_IE_TIGHT_adz_CCSD_Disp",
        # atz normal
        "DLPNO_CCSD_T_IE_atz",
        "DLPNO_CCSD_T_IE_atz_CCSD_E",
        "DLPNO_CCSD_T_IE_atz_CCSD_Cor",
        "DLPNO_CCSD_T_IE_atz_CCSD_T_E",
        "DLPNO_CCSD_T_IE_atz_CCSD_T_Cor",
        "DLPNO_CCSD_T_IE_atz_CCSD_Disp",
        # atz tight
        "DLPNO_CCSD_T_IE_TIGHT_atz",
        "DLPNO_CCSD_T_IE_TIGHT_atz_CCSD_E",
        "DLPNO_CCSD_T_IE_TIGHT_atz_CCSD_Cor",
        "DLPNO_CCSD_T_IE_TIGHT_atz_CCSD_T_E",
        "DLPNO_CCSD_T_IE_TIGHT_atz_CCSD_T_Cor",
        "DLPNO_CCSD_T_IE_TIGHT_atz_CCSD_Disp",
    ]
    # df["DLPNO_CCSD_IE adz"] = df["DLPNO_CCSD_IE_adz"]
    # df["DLPNO_CCSD_IE atz"] = df["DLPNO_CCSD_IE_atz"]
    # df["DLPNO_CCSD_IEIGHT adz"] = df["DLPNO_CCSD_IEIGHT_adz"]
    # df["DLPNO_CCSD_IEIGHT atz"] = df["DLPNO_CCSD_IEIGHT_atz"]
    # df["DLPNO_CCSD_IE_DISP adz"] = (
    #     df["DLPNO_CCSD_IE_adz"] + df["DLPNO_CCSD_IE_adz_CCSD_Disp"]
    # )
    # df["DLPNO_CCSD_IE_DISP atz"] = (
    #     df["DLPNO_CCSD_IE_atz"] + df["DLPNO_CCSD_IE_atz_CCSD_Disp"]
    # )
    # df["DLPNO_CCSD_IE_DISPIGHT adz"] = (
    #     df["DLPNO_CCSD_IEIGHT_adz"] + df["DLPNO_CCSD_IEIGHT_adz_CCSD_Disp"]
    # )
    # df["DLPNO_CCSD_IE_DISPIGHT atz"] = (
    #     df["DLPNO_CCSD_IEIGHT_atz"] + df["DLPNO_CCSD_IEIGHT_atz_CCSD_Disp"]
    # )

    df["DLPNO_CCSD_T_IE adz"] = (
        df["DLPNO_CCSD_T_IE_adz"] - df["DLPNO_CCSD_T_IE_adz_CCSD_Disp"]
    )
    df["DLPNO_CCSD_T_IE atz"] = (
        df["DLPNO_CCSD_T_IE_atz"] - df["DLPNO_CCSD_T_IE_atz_CCSD_Disp"]
    )
    df["DLPNO_CCSD_T_IE_TIGHT adz"] = (
        df["DLPNO_CCSD_T_IE_TIGHT_adz"] - df["DLPNO_CCSD_T_IE_TIGHT_adz_CCSD_Disp"]
    )
    df["DLPNO_CCSD_T_IE_TIGHT atz"] = (
        df["DLPNO_CCSD_T_IE_TIGHT_atz"] - df["DLPNO_CCSD_T_IE_TIGHT_atz_CCSD_Disp"]
    )

    df["DLPNO_CCSD_T_IE_DISP adz"] = df["DLPNO_CCSD_T_IE_adz"]
    df["DLPNO_CCSD_T_IE_DISP atz"] = df["DLPNO_CCSD_T_IE_atz"]
    df["DLPNO_CCSD_T_IE_DISP_TIGHT adz"] = df["DLPNO_CCSD_T_IE_TIGHT_adz"]
    df["DLPNO_CCSD_T_IE_DISP_TIGHT atz"] = df["DLPNO_CCSD_T_IE_TIGHT_atz"]


    ie_methods = [
        # "DLPNO_CCSD_IE adz",
        # "DLPNO_CCSD_IE atz",
        # "DLPNO_CCSD_IE_TIGHT adz",
        # "DLPNO_CCSD_IE_TIGHT atz",
        # "DLPNO_CCSD_IE_DISP adz",
        # "DLPNO_CCSD_IE_DISP atz",
        # "DLPNO_CCSD_IE_DISP_TIGHT adz",
        # "DLPNO_CCSD_IE_DISP_TIGHT atz",
        #
        "DLPNO_CCSD_T_IE",
        "DLPNO_CCSD_T_IE_TIGHT",
        "DLPNO_CCSD_T_IE_DISP",
        "DLPNO_CCSD_T_IE_DISP_TIGHT",
        "MP2 IE",
    ]

    copy_cols = copy_cols_start.copy()
    copy_cols.extend([f"{c} adz" for c in ie_methods])
    pp(copy_cols)
    df_adz = df[copy_cols].copy()
    df_adz.columns = [c.replace(" adz", "") for c in df_adz.columns]

    # reference energies come from
    # https://pubs.aip.org/aip/jcp/article/135/19/194102/189840/Basis-set-convergence-of-the-coupled-cluster
    df_adz['ref'] = df_adz[reference] / h2kcalmol

    print(
        df_adz[[
            "ref",
            "MP2 IE",
            "DLPNO_CCSD_T_IE_DISP",
            "DLPNO_CCSD_T_IE_adz",
            "DLPNO_CCSD_T_IE_adz_CCSD_Disp",
        ]] * h2kcalmol
    )

    copy_cols = copy_cols_start.copy()
    copy_cols.extend([f"{c} atz" for c in ie_methods])
    df_atz = df[copy_cols].copy()
    df_atz.columns = [c.replace(" atz", "") for c in df_atz.columns]

    for i in ie_methods:
        df_adz[f"{i} Error"] = df_adz[i] * h2kcalmol - df_adz[reference]
        df_atz[f"{i} Error"] = df_atz[i] * h2kcalmol - df_atz[reference]

    dfs = [
        {"df": df_adz, "label": "aug-cc-pVDZ", "ylim": [-3, 3]},
        {"df": df_atz, "label": "aug-cc-pVTZ", "ylim": [-3, 3]},
    ]
    df_labels_and_columns = {
        "MP2": "MP2 IE Error",
        # "DLPNO-CCSD": "DLPNO_CCSD_IE Error",
        "DLPNO-CCSD(T)": "DLPNO_CCSD_T_IE Error",
        "DLPNO-CCSD(T) [DISP]": "DLPNO_CCSD_T_IE_DISP Error",

        # "DLPNO-CCSD (TIGHT)": "DLPNO_CCSD_IE_TIGHT Error",
        "DLPNO-CCSD(T) (TIGHT)": "DLPNO_CCSD_T_IE_TIGHT Error",
        "DLPNO-CCSD(T) [DISP] (TIGHT)": "DLPNO_CCSD_T_IE_DISP_TIGHT Error",
    }

    import cdsg_plot

    cdsg_plot.error_statistics.violin_plot_table_multi(
        dfs,
        df_labels_and_columns,
        f"./plots/dlpno_nbc10_testing.jpg",
        table_fontsize=8,
        usetex=True,
        legend_loc="lower right",
        ylabel=r"Error (kcal$\cdot$mol$^{-1}$)" + "\n[CCSD(T)/CBS ref.]",
        figure_size=(7, 7),
        error_labels_position=(-0.3, 0.25),
        grid_heights=[
            0.38,
            2.0,
            0.38,
            2.0,
        ],
        # grid_widths=None,
    )
    return


def main():
    df = collect_dlpno_df()
    # pp(df.columns.tolist())
    plot_dlpno_results(
        df, limit_to_column_not_nan="DLPNO_CCSD_T_IE_TIGHT_atz_CCSD_Disp"
    )
    # print(df)
    # df_ccsd_energies = pd.read_csv("./data/dlpno_ccsd_out.csv")
    # # print(df_ccsd_energies)
    # pp(df_ccsd_energies.columns.values.tolist())
    # df_ccsd_t_energies = pd.read_csv("./data/ccsd_T_out.csv")
    # # print(df_ccsd_t_energies)
    # pp(df_ccsd_t_energies.columns.values.tolist())
    return


if __name__ == "__main__":
    main()
