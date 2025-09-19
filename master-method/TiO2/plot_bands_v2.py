#!/usr/bin/env python3
import argparse, numpy as np, matplotlib.pyplot as plt

def read_gnu(fname):
    segs, x, y = [], [], []
    with open(fname) as f:
        for line in f:
            if not line.strip():
                if x: segs.append((np.array(x), np.array(y))); x, y = [], []
                continue
            a, b = line.split()[:2]
            x.append(float(a)); y.append(float(b))
    if x: segs.append((np.array(x), np.array(y)))
    return segs

def read_rap(fname):
    # QE bands.rap format: x  label
    xs, labs = [], []
    try:
        with open(fname) as f:
            for line in f:
                s = line.strip()
                if not s: continue
                parts = s.split()
                x = float(parts[0])
                lab = parts[-1]
                # map G -> Γ
                lab = r"$\Gamma$" if lab.upper() in ("G","\\GAMMA","GAMMA") else lab
                xs.append(x); labs.append(lab)
    except FileNotFoundError:
        return None, None
    return xs, labs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gnu", default="TiO2.bands.shifted.gnu")
    ap.add_argument("--rap", default="TiO2.bands.rap")
    ap.add_argument("--out", default="TiO2_bands_clean.png")
    ap.add_argument("--shifted", action="store_true")
    ap.add_argument("--vbm", type=float)
    ap.add_argument("--fermi", type=float)
    ap.add_argument("--gap", type=float)
    ap.add_argument("--mono", action="store_true", help="single color lines")
    ap.add_argument("--ylim", default=None, help="ymin,ymax in eV (e.g. -6,30)")
    args = ap.parse_args()

    segs = read_gnu(args.gnu)

    # shift if requested
    if not args.shifted:
        if args.vbm is not None:
            vbm = args.vbm
        elif args.fermi is not None and args.gap is not None:
            vbm = args.fermi - 0.5*args.gap
        else:
            raise SystemExit("Provide --vbm or (--fermi and --gap), or pass --shifted.")
        segs = [(x, y - vbm) for (x, y) in segs]

    # ticks from .rap (Γ–X–… positions)
    kxs, klabs = read_rap(args.rap)

    plt.figure(figsize=(12,7))
    if args.mono:
        for x,y in segs: plt.plot(x,y, lw=1.8)
    else:
        for i,(x,y) in enumerate(segs): plt.plot(x,y, lw=1.6)

    if kxs:
        for xb in kxs: plt.axvline(x=xb, ls="--", lw=0.8, color="0.7")
        plt.xticks(kxs, klabs)
    else:
        # fallback: just set min/max
        xs = np.concatenate([s[0] for s in segs])
        plt.xticks([xs.min(), xs.max()])

    plt.xlabel("k-path")
    plt.ylabel("Energy (eV) relative to VBM")
    plt.grid(axis="y", alpha=0.3, ls=":")
    if args.ylim:
        y0,y1 = [float(v) for v in args.ylim.split(",")]
        plt.ylim(y0,y1)
    # zero line at VBM
    plt.axhline(0, lw=0.8, color="0.5", ls=":")
    plt.tight_layout()
    plt.savefig(args.out, dpi=220)
    print(f"Wrote {args.out}")
if __name__ == "__main__":
    main()
