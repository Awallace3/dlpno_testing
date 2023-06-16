import hrcl_jobs
from hrcl_jobs.parallel import ms_sl
import hrcl_jobs_orca
import qcelemental as qcel
import pandas as pd
import data
import os
import numpy as np
from mpi4py import MPI


def read_s22() -> None:
    """
    read_s22
    """
    geoms = data.s22.s22_db()
    RAs, RBs, ZAs, ZBs, charges = [], [], [], [], []
    for i, geom in enumerate(geoms):
        mol = qcel.models.Molecule.from_data(geom)
        mA, mB = mol.fragments_[0], mol.fragments_[1]
        RAs.append(mol.geometry[mA, :])
        RBs.append(mol.geometry[mB, :])
        ZAs.append(mol.atomic_numbers[mA])
        ZBs.append(mol.atomic_numbers[mB])
        c = np.array(
            [
                [int(mol.molecular_charge), mol.molecular_multiplicity],
                [int(mol.fragment_charges_[0]), mol.fragment_multiplicities_[0]],
                [int(mol.fragment_charges_[1]), mol.fragment_multiplicities_[1]],
            ]
        )
        charges.append(c)

    sys_inds = [i for i in range(1, len(geoms) + 1)]
    DB = ["s22" for i in range(len(geoms))]
    return DB, sys_inds, RAs, ZAs, RBs, ZBs, charges


def read_3ACX() -> None:
    labels, sys_indices, names, geoms = data.protein.read_protein_files(
        "data/3ACX_starting", "3ACX"
    )
    RAs, RBs, ZAs, ZBs, charges = [], [], [], [], []
    for i, mol in enumerate(geoms):
        mA, mB = mol.fragments_[0], mol.fragments_[1]
        # ensure protein is always fragment A
        if len(mA) < len(mB):
            mA, mB = mB, mA
        print(len(mA), len(mB))
        RAs.append(mol.geometry[mA, :])
        RBs.append(mol.geometry[mB, :])
        ZAs.append(mol.atomic_numbers[mA])
        ZBs.append(mol.atomic_numbers[mB])
        c = np.array(
            [
                [int(mol.molecular_charge), mol.molecular_multiplicity],
                [int(mol.fragment_charges_[0]), mol.fragment_multiplicities_[0]],
                [int(mol.fragment_charges_[1]), mol.fragment_multiplicities_[1]],
            ]
        )
        charges.append(c)
    DB = ["3ACX" for i in range(len(geoms))]
    t = sorted(zip(names, RAs, RBs, ZAs, ZBs, charges), key=lambda x: int(x[0]))
    names, RAs, RBs, ZAs, ZBs, charges = [], [], [], [], [], []
    for i in t:
        names.append(i[0])
        RAs.append(i[1])
        RBs.append(i[2])
        ZAs.append(i[3])
        ZBs.append(i[4])
        charges.append(i[5])
    print(names)
    sizes = [int(i) for i in names]
    for i in zip(sys_indices, sizes):
        print(i)
    return DB, sys_indices, sizes, RAs, ZAs, RBs, ZBs, charges


def create_s22_table() -> None:
    """
    create_s22_table creates SQL table for running parallel jobs
    """
    table_cols = {
        "id": "INTEGER PRIMARY KEY",
        "DB": "text",
        "sys_ind": "integer",
        "RA": "array",
        "ZA": "array",
        "RB": "array",
        "ZB": "array",
        "charges": "array",
        "dlpno_ccsd_adz": "array",
        "dlpno_ccsd_adz_orca_loosePNO": "array",
        "dlpno_ccsd_adz_orca_normalPNO": "array",
        "dlpno_ccsd_adz_orca_tightPNO": "array",
        "dlpno_ccsd_adz_orca_veryTightPNO": "array",
        "dlpno_ccsd_adz_CP": "array",
        "dlpno_ccsd_adz_orca_loosePNO_CP": "array",
        "dlpno_ccsd_adz_orca_normalPNO_CP": "array",
        "dlpno_ccsd_adz_orca_tightPNO_CP": "array",
        "dlpno_ccsd_adz_orca_veryTightPNO_CP": "array",

        "dlpno_ccsd_t_adz_orca_loosePNO": "array",
        "dlpno_ccsd_t_adz_orca_normalPNO": "array",
        "dlpno_ccsd_t_adz_orca_tightPNO": "array",
        "dlpno_ccsd_t_adz_orca_veryTightPNO": "array",
        "dlpno_ccsd_t_adz_CP": "array",
        "dlpno_ccsd_t_adz_orca_loosePNO_CP": "array",
        "dlpno_ccsd_t_adz_orca_normalPNO_CP": "array",
        "dlpno_ccsd_t_adz_orca_tightPNO_CP": "array",
        "dlpno_ccsd_t_adz_orca_veryTightPNO_CP": "array",
    }
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:
        db_path = "db/dlpno.db"
        table_name = "s22"
        table_exists = hrcl_jobs.sqlt.new_table(db_path, table_name, table_cols)
        con, cur = hrcl_jobs.sqlt.establish_connection(db_path)
        if table_exists:
            data = read_s22()
            insertion = ["DB", "sys_ind", "RA", "ZA", "RB", "ZB", "charges"]
            for r in zip(*read_s22()):
                print(r)
                hrcl_jobs.sqlt.insert_new_row(cur, con, table_name, insertion, r)
        else:
            hrcl_jobs.sqlt.table_add_columns(con, table_name, table_cols)
            print("Skipping Insertions...")
    MPI.Comm.Barrier(comm)
    return


def create_3ACX_table() -> None:
    """
    create_s22_table creates SQL table for running parallel jobs
    """
    table_cols = {
        "id": "INTEGER PRIMARY KEY",
        "DB": "text",
        "sys_ind": "integer",
        "sizes": "integer",
        "RA": "array",
        "ZA": "array",
        "RB": "array",
        "ZB": "array",
        "charges": "array",
        # "dlpno_ccsd_adz_orca_loosePNO": "array",
        # "dlpno_ccsd_adz_orca_normalPNO": "array",
        "dlpno_ccsd_adz_orca_tightPNO": "array",
        # "dlpno_ccsd_adz_orca_veryTightPNO": "array",
    }
    db_path = "db/dlpno.db"
    table_name = "t3ACX"
    table_exists = hrcl_jobs.sqlt.new_table(db_path, table_name, table_cols)
    con, cur = hrcl_jobs.sqlt.establish_connection(db_path)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:
        if table_exists:
            # data = read_3ACX()
            insertion = ["DB", "sys_ind", "sizes", "RA", "ZA", "RB", "ZB", "charges"]
            for r in zip(*read_3ACX()):
                print(r)
                hrcl_jobs.sqlt.insert_new_row(cur, con, table_name, insertion, r)
        else:
            hrcl_jobs.sqlt.table_add_columns(con, table_name, table_cols)
            print("Skipping Insertions...")
    MPI.Comm.Barrier(comm)
    return


def run_s22_dlpno():
    """
    Runs s22 db jobs with DLPNO-CCSD(T)
    """
    db_path = "db/dlpno.db"
    table_name = "s22"
    create_s22_table()
    con, cur = hrcl_jobs.sqlt.establish_connection(db_path)
    TCutPNO, TCutPairs, TCutMKN = 1e-8, 1e-5, 1e-3  # Andy's params
    PNO_params = {
        # [TCutPNO, TCutPairs, TCutMKN, TCutDO]
        # "_orca_loosePNO": [1e-6, 1e-3, 1e-3, 2e-2],
        # "_orca_normalPNO": [3.33e-7, 1e-4, 1e-3, 1e-2],
        # "_orca_tightPNO": [1e-7, 1e-5, 1e-3, 5e-3],
        "_orca_veryTightPNO": [1E-08, 1E-06, 1E-04, 5e-3]
    }

    for k, v in PNO_params.items():
        # lt = ["DLPNO-CCSD cc-pVDZ cc-pVDZ/C RIJCOSX def2/J TIGHTSCF", *v]
        lt = ["DLPNO-CCSD cc-pVDZ cc-pVDZ/C TIGHTSCF", k.split("_")[-1], *v]
        output_col = "dlpno_ccsd_adz"
        # lt = ["DLPNO-CCSD(T) cc-pVDZ cc-pVDZ/C TIGHTSCF", k.split("_")[-1], *v]
        # output_col = "dlpno_ccsd_t_adz"
        if k != "andy":
            output_col += k
        id_list = hrcl_jobs.sqlt.query_columns_for_values(
            # cur, table_name, id_names=["id"], matches={"DB": ["s22"]}
            cur,
            table_name,
            id_names=["id"],
            matches={output_col: ["NULL"]},
        )
        # id_list = [i for i in id_list if i != 19]
        print(id_list)
        if len(id_list) == 0:
            print("No jobs to run")
        else:
            print(f"Starting jobs for {output_col}")
            hrcl_jobs.parallel.ms_sl_extra_info(
                id_list=id_list,
                db_path=db_path,
                run_js_job=hrcl_jobs_orca.orca_inps.orca_dlpno_ccsd_ie,
                headers_sql=hrcl_jobs_orca.jobspec.dlpno_ie_sql_headers(),
                js_obj=hrcl_jobs_orca.jobspec.dlpno_ie_js,
                ppm="12000",
                table=table_name,
                id_label="id",
                output_columns=[output_col],
                extra_info=[lt],
            )
        output_col += "_CP"
        print(f"Starting CP jobs for {output_col}")
        id_list = hrcl_jobs.sqlt.query_columns_for_values(
            # cur, table_name, id_names=["id"], matches={"DB": ["s22"]}
            cur,
            table_name,
            id_names=["id"],
            matches={output_col: ["NULL"]},
        )
        print(id_list)
        if len(id_list) == 0:
            print("No jobs to run")
        else:
            hrcl_jobs.parallel.ms_sl_extra_info(
                id_list=id_list,
                db_path=db_path,
                run_js_job=hrcl_jobs_orca.orca_inps.orca_dlpno_ccsd_ie_CP,
                headers_sql=hrcl_jobs_orca.jobspec.dlpno_ie_sql_headers(),
                js_obj=hrcl_jobs_orca.jobspec.dlpno_ie_js,
                ppm="12000",
                table=table_name,
                id_label="id",
                extra_info=[lt],
                output_columns=[output_col],
            )
    # hrcl_jobs.sqlt.table_to_df_csv(db_path, table_name, "s22.csv")
    # hrcl_jobs.sqlt.table_to_df_pkl(db_path, table_name, "s22.pkl")
    return


def run_3ACX_dlpno():
    """
    Runs s22 db jobs with DLPNO-CCSD(T)
    """
    db_path = "db/dlpno.db"
    table_name = "t3ACX"
    create_3ACX_table()
    # return
    con, cur = hrcl_jobs.sqlt.establish_connection(db_path)
    PNO_params = {
        # [TCutPNO, TCutPairs, TCutMKN, TCutDO]
        # "_orca_loosePNO": [1e-6, 1e-3, 1e-3, 2e-2],
        # "_orca_normalPNO": [3.33e-7, 1e-4, 1e-3, 1e-2],
        "_orca_tightPNO": [1e-7, 1e-5, 1e-3, 5e-3],
        # "_orca_veryTightPNO": [1E-08, 1E-06, 1E-04, 5e-3]
    }

    for k, v in PNO_params.items():
        # lt = ["DLPNO-CCSD cc-pVDZ cc-pVDZ/C RIJCOSX def2/J TIGHTSCF", *v]
        lt = ["DLPNO-CCSD cc-pVDZ cc-pVDZ/C TIGHTSCF", k.split("_")[-1], *v]
        output_col = "dlpno_ccsd_adz"
        if k != "andy":
            output_col += k
        id_list = hrcl_jobs.sqlt.query_columns_for_values(
            # cur, table_name, id_names=["id"], matches={"DB": ["s22"]}
            cur,
            table_name,
            id_names=["id"],
            matches={output_col: ["NULL"]},
        )
        # id_list = [i for i in id_list if i != 19]
        print(id_list)
        if len(id_list) == 0:
            print("No jobs to run")
        else:
            print(f"Starting jobs for {output_col}")
            hrcl_jobs.parallel.ms_sl_extra_info(
                id_list=id_list,
                db_path=db_path,
                run_js_job=hrcl_jobs_orca.orca_inps.orca_dlpno_ccsd_ie_no_run,
                headers_sql=hrcl_jobs_orca.jobspec.dlpno_ie_sql_headers(),
                js_obj=hrcl_jobs_orca.jobspec.dlpno_ie_js,
                ppm="8100",
                table=table_name,
                id_label="id",
                output_columns=[output_col],
                extra_info=[lt],
            )
    return

DB_PATH = 'db/dlpno.db'

def main():
    run_s22_dlpno()
    # hrcl_jobs.sqlt.table_to_df_pkl(DB_PATH, 's22', "s22.pkl")
    # run_3ACX_dlpno()
    # geoms = data.s22.s22_db()
    # print(geoms[12])
    return


if __name__ == "__main__":
    main()
