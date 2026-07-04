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
The full-history Gabor channel shows additional projective compression and is retained as the open candidate
for an evolving effective equation of state.

Central result channel: V2 (generic probe, O12 basis).
Open front: V3 (full-history Gabor channel), not used as a canonical cosmological mechanism.

## Build

```bash
bash compile.sh
# Output: out/TrajectoryBranching.pdf
```

## Numerical companion

Script and data: `simulation/spectral/trajectory-entropy/trajectory_branching.py` (same workspace),
outputs in `traj_outputs/` (q{q}_traj.npz, trajectory_branching_h.pdf).

## Status

Draft; not yet deposited.
