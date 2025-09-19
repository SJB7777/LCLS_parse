from pathlib import Path

from LCLS_parse import get_run_files, save_lcls2mat


def main() -> None:
    root: Path = Path(r"Y:\241016_LCLS\cube") # 데이터 위치
    save_root: Path = Path(r"D:\New folder") # 저장 위치
    runs: list[int] = [366, 367]

    save_root.mkdir(parents=True, exist_ok=True)
    for run_n in runs:
        files: Path = get_run_files(run_n, root)
        if not files:
            print(f"No files found for run {run_n:04d}.")
            continue
        for file in files:
            print(f"Found file: \"{file}\"")
            save_file: Path = save_root / (file.name + ".mat")
            save_lcls2mat(file, save_file)
            print(f"Saved to \"{save_file}\".")


if __name__ == "__main__":
    main()
