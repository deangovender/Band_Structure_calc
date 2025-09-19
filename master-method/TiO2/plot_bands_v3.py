#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt

def read_gnu(fname):
    segs, x, y = [], [], []
    with open(fname) as f:
        for line in f:
            s = line.strip()
            if not s:
                if x:
                    segs.append((np.array(x), np.array(y)))
                    x, y = [], []
                continue
            a, b = s.split()[:2]
            x.append(float(a)); y.append(float(b))
    if x:
        segs.append((np.array(x), np.array(y)))
    return segs

def ticks_from_segments(segs):
    """Tick at start of each segment, plus the very last x."""
    if not segs:
        return []
    xs = [segs[0][0][0]]  # first x of first segment
    for i in range(1, len(segs)):
        xs.append(segs[i][0][0])  # first x of each next segment
    xs.append(segs[-1][0][-1])   # last x overall
    return xs

def main():
    ap = argparse.ArgumentParser(description="QE bands plot with VBM=0 and auto high-symmetry ticks.")
    ap.add_argument("--gnu", default="TiO2.bands.shifted.gnu", help="bands .gnu file")
    ap.add_argument("--out", default="TiO2_bands_clean.png", help="output PNG")
    ap.add_argument("--labels", default="G X M G Z R A Z", help="tick labels (space-separated)")
    ap.add_argument("--shifted", action="store_true", help="input already VBM-shifted")
    ap.add_argument("--vbm", type=float, help="VBM energy (eV) to subtract if not shifted")
    ap.add_argument("--fermi", type=float, help="Fermi energy (eV); with --gap, VBM=EF-gap/2")
    ap.add_argument("--gap", type=float, help="Band gap (eV); used with --fermi")
    ap.add_argument("--mono", action="store_true", help="use a single line color")
    ap.add_argument("--ylim", default=None, help='ymin,ymax (e.g. "-6,30")')
    args = ap.parse_args()

    segs = read_gnu(args.gnu)

    # Shift if needed
    if not args.shifted:
        if args.vbm is not None:
            vbm = args.vbm
        elif args.fermi is not None and args.gap is not None:
            vbm = args.fermi - 0.5*args.gap
        else:
            raise SystemExit("Provide --vbm or (--fermi and --gap), or pass --shifted.")
        segs = [(x, y - vbm) for (x, y) in segs]

    # Ticks & labels
    kxs = ticks_from_segments(segs)
    labs = args.labels.split()
    if len(labs) != len(kxs):
        labs = ["" for _ in kxs]
    labs = [r"$\Gamma$" if l.upper()=="G" else l for l in labs]

    # Plot
    plt.figure(figsize=(12,7))
    if args.mono:
        for x,y in segs:
            plt.plot(x,y, lw=1.8)
    else:
        for i,(x,y) in enumerate(segs):
            plt.plot(x,y, lw=1.6)

    for xb in kxs:
        plt.axvline(x=xb, ls="--", lw=0.8, color="0.7")
    plt.xticks(kxs, labs)
    plt.axhline(0, lw=0.8, color="0.5", ls=":")
    plt.xlabel("k-path")
    plt.ylabel("Energy (eV) relative to VBM")
    plt.grid(axis="y", alpha=0.3, ls=":")

    if args.ylim:
        try:
            y0, y1 = (float(v) for v in args.ylim.split(","))
            plt.ylim(y0, y1)
        except Exception:
            pass

    plt.tight_layout()
    plt.savefig(args.out, dpi=220)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
