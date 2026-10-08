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
were run with `python -W error` from a fresh `git archive` copy of the repository (8 October 2026); scripts write
their outputs in the current directory unless `--out-dir` is given.

```bash
python code/v3_exact_check.py          # 2 s; ALL CHECKS: PASS (q = 101, 211; n <= 7; exhaustive)
python code/amirror_mixed_coeff.py     # <1 s; ALL PASS
python code/amirror_jet_certify.py     # <1 s; ALL PASS
python code/amirror_recon.py           # <1 s; recon (see below)
python code/wn_recon.py                # <1 s; recon (see below)

# Quick mode of the sampled campaign (smoke test, 2 s)
python code/trajectory_branching.py --primes 29 --T 2000 --out-dir traj_quick

# Full campaign of the figure (about 3.5 min in total on one core), bit-for-bit the stored data
python code/trajectory_branching.py --primes 29 211 --T 100000 --out-dir traj_outputs
python code/trajectory_branching.py --primes 61 101 --T 20000 --out-dir traj_outputs
python code/trajectory_branching.py --primes 29 61 101 211 --plot-only --out-dir traj_outputs
```

Mapping of the scripts to the results of the note:

| script | supports | check |
|---|---|---|
| `code/v3_exact_check.py` | Table `tab:v3-count` (distinct V3 profiles 7, 19, 47, 107, 231, 483 for n = 2..7 at q = 101 and 211) and the checks C1-C5 of Section 6 (Gabor rank, geodesic death, outward geodesic count, closed-form class count, Chebotarev witness) | the printed table equals the tex table |
| `code/trajectory_branching.py` | Section "Numerical Evidence": Figure `fig:trajectory-branching` (`code/trajectory_branching_h.pdf`; the plot-only command above regenerates it, identical when rendered), the V1/V2/V3 estimator tables, the V3 rank sequence | `symbols` of q = 211 equal the stored data exactly, those of q = 29, 61, 101 to 5e-8 (float32); all estimators equal |
| `code/amirror_mixed_coeff.py`, `code/amirror_jet_certify.py` | Remark `rem:amirror-certification` (epsilon^2 identity, kernel formula for S, moment reduction, vanishing at the orthogonal point, Hermitian jets) | `ALL PASS`, relative errors of order 1e-6 at eps = 1e-3 |
| `code/amirror_recon.py` | recon behind Section 6.5 (real-Fourier collapse to the Burnside count 4, 10, 24, 54, 116; single-edge degeneracy; two-edge separation); no number of it is printed in the note | exploratory |
| `code/wn_recon.py` | recon behind the qualitative statements of the equation-of-state section (finite-n correction, candidate count-to-density mappings); its w values are not in the note | exploratory |
| `code/spectral_O12.py` | vendored dependency of `trajectory_branching.py` (verbatim copy, origin and sha256 in the file header and in `code/PROVENANCE.md`) | `tail -n +16 code/spectral_O12.py \| shasum -a 256` |

The recon scripts `amirror_recon.py` and `wn_recon.py` support no retained numerical result of the note; they are
kept for history.

Known debt (scripts):

- No committed script computes the distinct-b-sequence and distinct-profile columns of Table `tab:pell`, nor the
  post-hoc refinement epsilon = 10^-3 quoted for q = 211 in Section V2. Both were recomputed ad hoc on 8 October 2026
  from the stored q = 211 data with the functions of `trajectory_branching.py` and agree with the note
  (8096, 18675, 37394 at n = 10, 11, 12; h_2 = 0.885, 0.881, 0.877 at n = 5, 6, 7).
- The note states T = 2 x 10^4 for q <= 101; the stored q = 29 data have T = 10^5 (hence the command above).
- `amirror_mixed_coeff.py` cites in its docstring a recovery note that is not in this repository; the docstrings of
  `v3_exact_check.py` and `amirror_recon.py` announce "a few minutes", the measured runtime is seconds.
- The stored campaign data (`q{q}_traj.npz`, 9 MB) are not versioned; the commands above regenerate them.

## Status

Deposited on Zenodo, concept DOI [10.5281/zenodo.21197757](https://doi.org/10.5281/zenodo.21197757)
(last deposited version 1.3.0: conditional equation-of-state no-go, arithmetic and memory-depth remarks;
v1.3.1 is a local candidate).
Web page: https://cosmochrony.org/science/cosmology/trajectory-branching/
