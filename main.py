import hrcl_jobs
from hrcl_jobs.parallel import ms_sl
import hrcl_jobs_orca
import qcelemental as qcel
import pandas as pd
from data import s22
import os
import numpy as np


def read_s22() -> None:
    """
    read_s22
    """
    geoms = s22.s22_db()
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
    }
    db_path = "db/dlpno.db"
    table_name = "s22"
    table_exists = hrcl_jobs.sqlt.new_table(db_path, table_name, table_cols)
    if table_exists:
        data = read_s22()
        con, cur = hrcl_jobs.sqlt.establish_connection(db_path)
        insertion = ["DB", "sys_ind", "RA", "ZA", "RB", "ZB", "charges"]
        for r in zip(*read_s22()):
            print(r)
            hrcl_jobs.sqlt.insert_new_row(cur, con, table_name, insertion, r)
    else:
        print("Skipping Insertions...")
    return


def main():
    """
    Runs s22 db jobs with DLPNO-CCSD(T)
    """
    db_path = "db/dlpno.db"
    table_name = "s22"
    create_s22_table()
    con, cur = hrcl_jobs.sqlt.establish_connection(db_path)
    id_list = hrcl_jobs.sqlt.query_columns_for_values(
        cur, table_name, id_names=["id"], matches={"DB": ["s22"]}
    )
    print(id_list)
    # id_list = [1]
    TCutPNO, TCutPairs, TCutMKN = 1e-8, 1e-5, 1e-3
    ms_sl(
        id_list=id_list,
        db_path=db_path,
        run_js_job=hrcl_jobs_orca.orca_inps.orca_dlpno_ccsd_ie,
        headers_sql=hrcl_jobs_orca.jobspec.dlpno_ie_sql_headers(),
        js_obj=hrcl_jobs_orca.jobspec.dlpno_ie_js,
        ppm="4gb",
        table=table_name,
        id_label="id",
        # level_theory=["DLPNO-CCSD cc-pVDZ cc-pVDZ/C RIJCOSX def2/J TIGHTSCF"],
        level_theory=[
            [
                "DLPNO-CCSD cc-pVDZ cc-pVDZ/C RIJCOSX def2/J TIGHTSCF",
                TCutPNO,
                TCutPairs,
                TCutMKN,
            ]
        ],
        output_columns=[
            "dlpno_ccsd_adz",
        ],
    )
    return


if __name__ == "__main__":
    main()
