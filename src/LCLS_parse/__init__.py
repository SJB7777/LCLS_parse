from pathlib import Path
import re

import h5py
import numpy as np
from scipy.io import savemat


def h5_tree(hf: h5py.File) -> None:
    """
    Usage:
    with h5py.File(file) as hf:
        h5_tree(hf)
    """
    def tree(val, pre: str = "") -> None:
        items_cnt = len(val)
        for key, obj in val.items():
            items_cnt -= 1
            branch = "└──" if items_cnt == 0 else "├──"
            next_pre = f"{pre}    " if items_cnt == 0 else f"{pre}│   "

            if isinstance(obj, h5py.Group):
                print(f"{pre}{branch} {key}")
                tree(obj, next_pre)
            elif isinstance(obj, h5py.Dataset):
                try:
                    if h5py.check_string_dtype(obj.dtype):
                        print(f"{pre}{branch} {key} ({obj[()]})")
                    else:
                        print(f"{pre}{branch} {key} {obj.shape}")
                except TypeError:
                    print(f"{pre}{branch} {key} (scalar)")
            else:
                print(f"{pre}{branch} {key} (unknown type)")
    print(Path(hf.filename).name)
    tree(hf)


def save_lcls2mat(load_file: Path | str, save_file: Path | str) -> None:
    load_file = Path(load_file)
    save_file = Path(save_file)
    if not load_file.exists():
        raise FileNotFoundError(f"File \"{load_file}\" does not exist!")

    data = {}
    with h5py.File(load_file, "r") as hf:
        if "delay" in hf:
            data["delay"] = hf["delay"][()]
        data["images"] = hf["jungfrau512k_data"][()]

    data["images"] = np.transpose(data["images"], (1, 2, 0))
    savemat(save_file, data)


def get_run_files(run: int, root: Path | str) -> list[Path]:
    root = Path(root)
    if not root.exists():
        raise FileNotFoundError(f"Root path \"{root}\" does not exist!")

    matched_files = []
    pattern = re.compile(rf".*_Run{run:04d}_.*\.h5$")
    for file in root.rglob("*.h5"):
        if pattern.match(file.name):
            matched_files.append(file)

    return matched_files
