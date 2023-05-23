import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import qcelemental as qcel
import pickle
from io import StringIO
from qm_tools_aw import tools
from glob import glob
from pprint import pprint as pp


def read_preproccessed_mol(
    fn,
) -> qcel.models.Molecule:
    """
    read_preproccessed_mol reads mol that has dimer split to
    make qcelemental Molecule object
    """
    with open(fn, "r") as f:
        data = f.read()
    data = data.split("symmetry")[0]
    return qcel.models.Molecule.from_data(data)


def name_process_3ACX(
    path: str,
) -> str:
    """
    name_process_3ACX parses identifying information from 3ACX files
    """
    name = path.split("/")[-1].split(".")[0]
    size = name.split("_")[-1]
    return size


def read_protein_files(
    path: str,
    label: str,
    name_process_func=name_process_3ACX,
    process_func=read_preproccessed_mol,
) -> ([str], [int], [str], [qcel.models.Molecule]):
    """
    read_protein_files takes path to protein files and
    produces list of qcelemental Molecule objects
    """
    mol_files = glob(f"{path}/*.mol")
    labels, sys_indices, names, mols = [], [], [], []
    for sys_index, i in enumerate(mol_files):
        mol = process_func(i)
        name = name_process_3ACX(i)
        labels.append(label)
        sys_indices.append(sys_index)
        names.append(name)
        mols.append(mol)
    return labels, sys_indices, names, mols

