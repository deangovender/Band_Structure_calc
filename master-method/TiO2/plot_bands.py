#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt

def read_gnu(fname):
    segs, x, y = [], [], []
    with open(fname) as f:
        for line in f:
            if not line.strip():
                if x:
                    segs.append((np.array(x), np.array(y)))
                    x, y = [], []
                continue
            a, b = line.split()[:2]
            x.append(float(a)); y.append(float(b))
    if x:
        segs.append((np.array(x), np.array(y)))
    return segs

def detect_kbreaks(segs, tol=1e-9):
    xs = np.concatenate([s[0] for s in segs])
    breaks = [xs[0]]
    for i in range(1, len(xs)):
        if xs[i] + tol < xs[i-1]:
            breaks.append(xs[i])
    breaks.append(xs[-1])
    # unique-ish
    uniq = []
    for v in breaks:
        if not any(abs(v-u) < 1e-6 for u in uniq):
            uniq.append(v)
    return uniq

def shift_to_vbm(segs, vbm_eV):
    return [(x, y - vbm_eV) for (x, y) in segs]

def parse_args():
    p = argparse.ArgumentParser(description="Clean band plot with auto ticks; VBM=0 optional.")
    p.add_argument("--gnu", default="TiO2.bands.dat.gnu",
                   help="Input bands .gnu (QE bands.x output)")
    p.add_argument("--out", default="TiO2_bands_clean.png",
                   help="Output PNG filename")
    p.add_argument("--labels", default="G X M G Z R A Z",
                   help='High-symmetry labels, space-separated')
    p.add_argument("--shifted", action="store_true",
                   help="Input already shifted so that VBM=0 eV")
    p.add_argument("--vbm", type=float, default=None,
                   help="VBM energy (eV) to subtract if not shifted")
    p.add_argument("--fermi", type=float, default=None,
                   help="Fermi energy (eV); with --gap, VBM=EF-gap/2")
    p.add_argument("--gap", type=float, default=None,
                   help="Band gap (eV); used with --fermi")
    return p.parse_args()

def main():
    args = parse_args()
    segs = read_gnu(args.gnu)
    kbreaks = detect_kbreaks(segs)
    labels = args.labels.split()

    # Shift energies if needed
    if not args.shifted:
        if args.vbm is not None:
            vbm = args.vbm
        elif args.fermi is not None and args.gap is not None:
            vbm = args.fermi - 0.5*args.gap
        else:
            raise SystemExit("Provide --vbm or (--fermi and --gap), or pass --shifted.")
        segs = shift_to_vbm(segs, vbm)

    plt.figure(figsize=(10,6))
    for x, y in segs:
        plt.plot(x, y, lw=1.8)
    for xb in kbreaks:
        plt.axvline(x=xb, ls="--", lw=0.8, color="0.7")

    # xticks with labels if counts match
    if len(labels) == len(kbreaks):
        ticklabs = [r"$\Gamma$" if lab.upper()=="G" else lab for lab in labels]
        plt.xticks(kbreaks, ticklabs)
    else:
        plt.xticks(kbreaks)

    plt.ylabel("Energy (eV) relative to VBM")
    plt.xlabel("k-path")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(args.out, dpi=220)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
