# Band_Structure_calc

Input and output files for calculating the electronic band structure of TiO₂ with Quantum ESPRESSO (QE).

> **Update (2025-09-19)**  
> The folder **`master-method/`** contains the **correct, recommended pipeline** for this project.  
> The folder **`legacy-method-a/`** preserves the earlier workflow for transparency but is **deprecated**.

## What changed (why this repo has two methods)
- The **legacy method** performed *relaxed geometric optimization* (`calculation='relax'`) but **not** *variable-cell relaxation* (`'vc-relax'`). That froze the cell shape/volume and led to incorrect lattice parameters and shifted band energies.  
- The **master method** uses **variable-cell relaxation (vc-relax)** followed by SCF and bands post-processing on a documented k-path. This is the method used for the report’s final results.

If you need to reproduce the “almost-right” numbers for comparison, see `legacy-method-a/` and cite the older release/commit.

