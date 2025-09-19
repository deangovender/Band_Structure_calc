#!/usr/bin/env python3
import argparse, numpy as np, matplotlib.pyplot as plt

def read_gnu(fname):
    segs, x, y = [], [], []
    with open(fname) as f:
        for line in f:
            s = line.strip()
            if not s:
                if x: segs.append((np.array(x), np.array(y))); x, y = [], []
                continue
            a, b = s.split()[:2]
            x.append(float(a)); y.append(float(b))
    if x: segs.append((np.array(x), np.array(y)))
    return segs

def kbreaks_from_first_band(segs, tol=1e-9):
    """Use the FIRST band's x to find Γ–X–… boundaries (places where x decreases)."""
    x = segs[0][0]
    br = [x[0]]
    for i in range(1, len(x)):
        if x[i] + tol < x[i-1]:
            br.append(x[i])
    br.append(x[-1])
    # uniq with tolerance
    out = []
    for v in br:
        if not any(abs(v-u)<1e-8 for u in out): out.append(v)
    return out

def main():
    ap = argparse.ArgumentParser(description="QE bands: VBM=0, auto k-path ticks, nice styling.")
    ap.add_argument("--gnu", default="TiO2.bands.shifted.gnu")
    ap.add_argument("--out", default="TiO2_bands_clean.png")
    ap.add_argument("--labels", default="G X M G Z R A Z",
                    help="tick labels (space-separated)")
    ap.add_argument("--shifted", action="store_true")
    ap.add_argument("--vbm", type=float)
    ap.add_argument("--fermi", type=float)
    ap.add_argument("--gap", type=float)
    ap.add_argument("--ymin", type=float, default=None)
    ap.add_argument("--ymax", type=float, default=None)
    ap.add_argument("--mono", action="store_true")
    ap.add_argument("--lw", type=float, default=1.6)
    args = ap.parse_args()

    segs = read_gnu(args.gnu)

    # shift if needed
    if not args.shifted:
        if args.vbm is not None:
            vbm = args.vbm
        elif args.fermi is not None and args.gap is not None:
            vbm = args.fermi - 0.5*args.gap
        else:
            raise SystemExit("Provide --vbm or (--fermi and --gap), or pass --shifted.")
        segs = [(x, y - vbm) for (x, y) in segs]

    # k-path ticks from first band
    kxs = kbreaks_from_first_band(segs)
    labs = args.labels.split()
    if len(labs) != len(kxs):
        labs = ["" for _ in kxs]
    labs = [r"$\Gamma$" if L.upper()=="G" else L for L in labs]

    # plot
    plt.figure(figsize=(12,7))
    if args.mono:
        for x,y in segs: plt.plot(x,y, lw=args.lw, color="black")
    else:
        for x,y in segs: plt.plot(x,y, lw=args.lw)

    for xb in kxs: plt.axvline(x=xb, ls="--", lw=0.8, color="0.7")
    plt.xticks(kxs, labs)
    plt.axhline(0, lw=0.8, color="0.5", ls=":")
    plt.xlabel("k-path"); plt.ylabel("Energy (eV)  ")
    plt.grid(axis="y", alpha=0.3, ls=":")

    if args.ymin is not None or args.ymax is not None:
        plt.ylim(args.ymin, args.ymax)

    plt.tight_layout()
    plt.savefig(args.out, dpi=240)
    print(f"Wrote {args.out}")
if __name__ == "__main__":
    main()
