from pathlib import Path
import re

import h5py
import numpy as np
from scipy.io import savemat


def h5_tree(val, pre: None = "") -> None:
    """
    with h5py.File(file) as hf:
        print(hf)
        h5_tree(hf)
    """
    items_cnt = len(val)
    for key, val in val.items():
        items_cnt -= 1
        if items_cnt == 0:
            # the last item
            if isinstance(val, h5py._hl.group.Group):
                print(f"{pre}└── {key}")
                h5_tree(val, f"{pre}    ")
            else:
                try:
                    if h5py.check_string_dtype(val.dtype):
                        print(f"{pre}└── {key} ({val})")
                    else:
                        print(f"{pre}└── {key} ({val.shape})")
                except TypeError:
                    print(f"{pre}└── {key} (scalar)")
        else:
            if isinstance(val, h5py._hl.group.Group):
                print(f"{pre}├── {key}")
                h5_tree(val, f"{pre}│   ")
            else:
                try:
                    if h5py.check_string_dtype(val.dtype):
                        print(f"{pre}├── {key} ({val})")
                    else:
                        print(f"{pre}├── {key} ({val.shape})")
                except TypeError:
                    print(f"{pre}├── {key} (scalar)")


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


def main() -> None:
    root: Path = Path(r"Y:\241016_LCLS\cube") # 데이터 위치
    save_root: Path = Path(r".\data") # 저장 위치
    runs: list[int] = [366, 367]

    save_root.mkdir(parents=True, exist_ok=True)
    for run_n in runs:
        files: Path = get_run_files(run_n, root)
        if files == []:
            print(f"No files found for run {run_n:04d}.")
            continue
        for file in files:
            print(f"Found file: \"{file}\"")
            save_file: Path = save_root / (file.name + ".mat")
            save_lcls2mat(file, save_file)
            print(f"Saved to \"{save_file}\".")


if __name__ == "__main__":
    main()
