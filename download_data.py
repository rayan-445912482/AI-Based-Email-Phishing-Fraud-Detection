import argparse
import sys
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = RAW_DIR / "emails.csv"

DATASET_URLS = [
    "https://huggingface.co/datasets/zefang-liu/phishing-email-dataset/resolve/main/Phishing_Email.csv",
]

MAX_ROWS = 82_000

TEXT_CANDIDATES = ["text_combined", "text", "email text", "body", "message", "email"]
LABEL_CANDIDATES = ["label", "email type", "class", "target"]

PHISHING = {"1", "1.0", "phishing", "phishing email", "phish", "fraud", "malicious"}
LEGIT = {"0", "0.0", "legitimate", "safe", "safe email", "ham", "benign"}


def download_file(url: str, target: Path) -> bool:
    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"[!] Download failed: {exc}")
        return False

    total = int(response.headers.get("content-length", 0)) or None
    with open(target, "wb") as handle, tqdm(
        desc=target.name, total=total, unit="B", unit_scale=True, unit_divisor=1024
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024 * 128):
            if chunk:
                handle.write(chunk)
                bar.update(len(chunk))
    return True


def map_label(value):
    text = str(value).strip().lower()
    if text in PHISHING:
        return "phishing"
    if text in LEGIT:
        return "legitimate"
    return None


def normalize(raw_path: Path, output_path: Path) -> None:
    print(f"[+] Reading {raw_path} ...")
    frame = pd.read_csv(raw_path, low_memory=False)

    lookup = {str(c).strip().lower(): c for c in frame.columns}
    text_col = next((lookup[c] for c in TEXT_CANDIDATES if c in lookup), None)
    label_col = next((lookup[c] for c in LABEL_CANDIDATES if c in lookup), None)

    if not text_col or not label_col:
        raise RuntimeError(f"Could not identify columns. Available: {list(frame.columns)}")

    data = frame[[text_col, label_col]].copy()
    data.columns = ["text", "label"]
    data["label"] = data["label"].map(map_label)
    data["text"] = (
        data["text"].fillna("").astype(str)
        .str.replace(r"\s+", " ", regex=True).str.strip()
    )

    data = data[
        (data["text"].str.len() > 20)
        & (data["text"].str.len() < 100_000)
        & data["label"].notna()
    ]
    data = data.drop_duplicates(subset=["text"]).reset_index(drop=True)

    legitimate = data[data["label"] == "legitimate"]
    phishing = data[data["label"] == "phishing"]

    n_per_class = min(len(legitimate), len(phishing), MAX_ROWS // 2)
    if n_per_class < 500:
        raise RuntimeError(
            f"Not enough data. legitimate={len(legitimate)}, phishing={len(phishing)}"
        )

    balanced = (
        pd.concat(
            [
                legitimate.sample(n=n_per_class, random_state=42),
                phishing.sample(n=n_per_class, random_state=42),
            ],
            ignore_index=True,
        )
        .sample(frac=1.0, random_state=42)
        .reset_index(drop=True)
    )

    balanced.to_csv(output_path, index=False)
    print(f"[+] Saved {len(balanced):,} rows to {output_path}")
    print(f"    legitimate: {(balanced['label'] == 'legitimate').sum():,}")
    print(f"    phishing:   {(balanced['label'] == 'phishing').sum():,}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to a manually downloaded CSV")
    args = parser.parse_args()

    if OUTPUT_PATH.exists():
        answer = input(f"[i] {OUTPUT_PATH} exists. Overwrite? [y/N]: ").strip().lower()
        if answer != "y":
            return 0

    if args.file:
        source = Path(args.file)
        if not source.exists():
            print(f"[X] File not found: {source}")
            return 1
        normalize(source, OUTPUT_PATH)
        print("[+] Dataset ready.")
        return 0

    temp = RAW_DIR / "_download.csv"
    print("[+] Downloading dataset ...")
    ok = any(download_file(url, temp) for url in DATASET_URLS)

    if not ok:
        print("[X] Automatic download failed.")
        print("    Download a phishing email CSV manually, then run:")
        print("    python download_data.py --file path\\to\\file.csv")
        return 1

    try:
        normalize(temp, OUTPUT_PATH)
    except RuntimeError as exc:
        print(f"[X] {exc}")
        return 1
    finally:
        if temp.exists():
            temp.unlink()

    print("[+] Dataset ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
