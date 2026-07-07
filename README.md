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

## Numerical companion

Script and data: `simulation/spectral/trajectory-entropy/trajectory_branching.py` (same workspace),
outputs in `traj_outputs/` (q{q}_traj.npz, trajectory_branching_h.pdf).
Exhaustive verification of the V3 theorem (all non-backtracking words, machine precision):
`simulation/spectral/trajectory-entropy/v3_exact_check.py`.
Certification of the mixed two-anchor coefficient (eps^2 identity, moment reduction, Hermitian jets):
`simulation/spectral/trajectory-entropy/amirror_mixed_coeff.py` and `amirror_jet_certify.py`.

## Status

Deposited on Zenodo, concept DOI [10.5281/zenodo.21197757](https://doi.org/10.5281/zenodo.21197757)
(latest version 1.3.0: conditional equation-of-state no-go, arithmetic and memory-depth remarks).
Web page: https://cosmochrony.org/science/cosmology/trajectory-branching/
