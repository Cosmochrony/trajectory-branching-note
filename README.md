# Projective Trajectory Branching and the de Sitter Limit

Short result note of the Cosmochrony programme (bib key `Beau2026tb`).

The transfer of the spectral admissibility cascade from LPS expanders to the Heisenberg graph Heis3(Z/qZ)
destroys exponential growth at the level of endpoint volumes (Bass-Guivarc'h degree 4), but not at the level
of projectively distinguishable histories.
The note defines a hierarchy of trajectory distinguishability notions (D1-D4), proves the endpoint no-go,
proves that the canonical O12-compatible residual channel is b-only (the central charge is unconditionally
erased from mono-path norms), and pins the canonical branching rate exactly: the distinguishable-history
count is the Pell count N(n) = 2N(n-1) + N(n-2), with asymptotic rate h_b = log(1+sqrt(2)).
Profile separation is proved for a generic probe (finite union of proper hypersurfaces) and witnessed exactly
on the sampled multi-prime campaign (q in {29, 61, 101, 211}).
The full-history Gabor channel (V3) is itself a theorem since v1.1.0: the Gabor span exhausts the abelian
l1 disk shell by shell, so nonzero symbols are confined to l1-outward geodesics (geodesic death: one inward
step erases the profile permanently), and for a generic probe (Lawrence-Pfander-Walnut full spark plus a
Chebotarev-based separation lemma) the distinguishable-history count is exact: since v1.2.0,
N(n) = (N_class+2)/2 = 2^(n+2) - 4n - 1 is a theorem on the window q > (4n-1)(2n+3), n >= 2.
The last separation step (a-mirror pairs at equal |b|) is closed by proving generic non-vanishing of a
mixed two-anchor coefficient -- a Hermitian jet at the orthogonal point of an anchor moment domain --
combined with a Klein rigidity property of outward geodesics; the channel has positive and exactly pinned
symbolic entropy log 2, strictly below the canonical rate log(1+sqrt(2)).
The count is witnessed exhaustively at q in {101, 211}.
The finite-n compression profile is retained as the candidate input for an evolving effective equation of
state, now gated by a conditional no-go (since v1.3.0): under the rank-time dictionary hypothesis and the
minimal count-to-density mapping class, the exact counts do not supply an observable evolving equation of
state -- their observable content is confined to the early low-rank window; the remaining evolving-w routes
are rank-dependent dictionary corrections or the spectral-equilibrium route.
Version 1.3.0 also adds two arithmetic remarks (Pell-equation identity of the canonical count;
transfer-matrix formulation with effective memory depth one) and a labelled doubling-bracket reading.

Central result channel: V2 (generic probe, O12 basis), rate log(1+sqrt(2)).
Full-history channel: V3 (Gabor basis), proved strictly compressive, rate log 2.

## Build

```bash
bash compile.sh
# Output: out/TrajectoryBranching.pdf
```

## Reproduction

Everything below runs from a clone of this repository alone (Python 3.14 with `numpy` and `matplotlib`, see
`code/requirements.txt`; the dependency `spectral_O12` is vendored in `code/`). Provenance of the vendored module,
seeds, data inputs and a per-script description are in [`code/PROVENANCE.md`](code/PROVENANCE.md). All commands
were run with `python -W error` from a fresh `git archive` copy of the repository (8 October 2026). Only
`trajectory_branching.py` writes files: its default output directory is `code/traj_outputs/` (next to the script, not
the current directory; `--out-dir` overrides it, and the commands below pass it explicitly); the other scripts write
nothing.

```bash
python code/v3_exact_check.py          # 2 s; ALL CHECKS: PASS (q = 101, 211; n <= 7; exhaustive)
python code/amirror_mixed_coeff.py     # <1 s; ALL PASS
python code/amirror_jet_certify.py     # <1 s; ALL PASS
python code/amirror_recon.py           # <1 s; recon (see below)
python code/wn_recon.py                # <1 s; recon (see below)

# Quick mode of the sampled campaign (smoke test, 2 s)
python code/trajectory_branching.py --primes 29 --T 2000 --out-dir traj_quick

# Full campaign of the figure (about 3.5 min in total on one core); parameters per prime as run:
# T = 10^5 for q = 29 and 211, T = 2 x 10^4 for q = 61 and 101 (three conjugate block pairs, seed 42)
python code/trajectory_branching.py --primes 29 211 --T 100000 --out-dir traj_outputs
python code/trajectory_branching.py --primes 61 101 --T 20000 --out-dir traj_outputs
python code/trajectory_branching.py --primes 29 61 101 211 --plot-only --out-dir traj_outputs

# Table tab:pell and the eps = 1e-3 refinement (reads traj_outputs/q211_traj.npz written above, about 17 s;
# use --regenerate instead of --data-dir to recompute the q = 211 symbols in memory, about 2 min)
python code/pell_counts.py --data-dir traj_outputs
```

Fidelity to the stored campaign data (workspace `simulation/spectral/trajectory-entropy/traj_outputs/`, 4 July 2026):
the regenerated `q211_traj.npz` is bit-identical for `symbols` (and for every other field); for q = 29, 61, 101 the
regenerated float32 `symbols` differ from the stored ones by at most 4.3 x 10^-8 (float32 noise), while all the other
fields and all estimators h_2, h_low, h_up (every variant, every epsilon) are identical.

Mapping of the scripts to the results of the note:

| script | supports | check |
|---|---|---|
| `code/v3_exact_check.py` | Table `tab:v3-count` (distinct V3 profiles 7, 19, 47, 107, 231, 483 for n = 2..7 at q = 101 and 211) and the checks C1-C5 of Section 6 (Gabor rank, geodesic death, outward geodesic count, closed-form class count, Chebotarev witness) | the printed table equals the tex table |
| `code/trajectory_branching.py` | Section "Numerical Evidence": Figure `fig:trajectory-branching` (`code/trajectory_branching_h.pdf`; the plot-only command above writes `traj_outputs/trajectory_branching_h.pdf`, identical to it when rendered; copy it to `code/` to replace the committed figure), the V1/V2/V3 estimator tables, the V3 rank sequence | `symbols` of q = 211 equal the stored data exactly, those of q = 29, 61, 101 to 4.3e-8 (float32); all estimators equal |
| `code/pell_counts.py` | Table `tab:pell` (exact N_b(n) by Pell recursion, transfer matrix and enumeration; sampled distinct b-sequences and distinct V2 profiles at q = 211, n = 1..12) and the refinement epsilon = 10^-3 of Section V2 (h_2 = 0.885, 0.881, 0.877 at n = 5, 6, 7) | prints the table and `PASS`; exit status 1 if any number differs from the note; no randomness beyond the seed-42 path ensemble |
| `code/amirror_mixed_coeff.py`, `code/amirror_jet_certify.py` | Remark `rem:amirror-certification` (epsilon^2 identity, kernel formula for S, moment reduction, vanishing at the orthogonal point, Hermitian jets) | `ALL PASS`, relative errors below 2e-5 at eps = 1e-3 |
| `code/amirror_recon.py` | recon behind Section 6.5 (real-Fourier collapse to the Burnside count 4, 10, 24, 54, 116; single-edge degeneracy; two-edge separation); no number of it is printed in the note | exploratory |
| `code/wn_recon.py` | recon behind the qualitative statements of the equation-of-state section (finite-n correction, candidate count-to-density mappings); its w values are not in the note | exploratory |
| `code/spectral_O12.py` | vendored dependency of `trajectory_branching.py` (verbatim copy, origin and sha256 in the file header and in `code/PROVENANCE.md`) | `tail -n +16 code/spectral_O12.py \| shasum -a 256` |

The recon scripts `amirror_recon.py` and `wn_recon.py` support no retained numerical result of the note; they are
kept for history.

Known debt (scripts):

- `amirror_mixed_coeff.py` cites in its docstring a recovery note that is not in this repository; the docstrings of
  `v3_exact_check.py` and `amirror_recon.py` announce "a few minutes", the measured runtime is seconds.
- The stored campaign data (`q{q}_traj.npz`, 9 MB) are not versioned; the commands above regenerate them.

## Status

Deposited on Zenodo, concept DOI [10.5281/zenodo.21197757](https://doi.org/10.5281/zenodo.21197757)
(last deposited version 1.3.0: conditional equation-of-state no-go, arithmetic and memory-depth remarks;
v1.3.1 is a local candidate).
Web page: https://cosmochrony.org/science/cosmology/trajectory-branching/
