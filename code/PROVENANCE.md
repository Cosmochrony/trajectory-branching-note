# code/ -- provenance, dependencies and per-script description

Everything in this directory runs from a clone of this repository alone; no sibling repository, no workspace path
and no external module is needed (the one former external dependency, `spectral_O12`, is vendored, see below).
Reproduction commands and the mapping script -> result of the note are in the top-level `README.md`
(section "Reproduction").

## Dependencies

- Python 3.14.5 (all runs reported below), numpy 2.4.0, matplotlib 3.10.8 (the workspace environment
  `simulation/.venv` also carries scipy 1.16.3, which no script of this directory imports).
- `code/requirements.txt`: `numpy>=2.4.0`, `matplotlib>=3.7`. The standard library covers the rest
  (`wn_recon.py` uses only `math`).
- Every run was made with `python -W error` (warnings are errors) from a fresh `git archive` copy.

## Vendored dependency: `spectral_O12.py`

`trajectory_branching.py` imports six names from the module `spectral_O12` (`EPS_GS`, `build_generators`,
`fingerprint_vectors_batch`, `gram_schmidt_batch`, `heisenberg_mul`, `make_psi_table`; transitively
`heisenberg_mul_batch` and `weil_batch_lut`, called by `fingerprint_vectors_batch`).

| field | value |
|---|---|
| origin repository | `Cosmochrony/spectral-o25` (https://github.com/Cosmochrony/spectral-o25), workspace `admissibility/o25` |
| origin path | `code/spectral_O12.py` |
| origin commit | `d8f494a1c99eff4341ae7fd85c72143d258e9c8c` (2026-04-22, last commit touching the file); repository HEAD at copy time `52a39d7415978bc3959e0ba9feb12ff09eb7bc1a`, working tree clean for the file |
| sha256 of the original | `6cd3788ba178a335313efdac02d3ebc2a1596d2d4f83e25a1da481867e3c95b4` (992 lines) |
| copied on | 2026-10-08 |
| author / licence | J. Beau, Cosmochrony programme (module of the O12 paper); no separate licence file for the module; copied unchanged by the same author |
| form | verbatim copy preceded by a 15-line `#` header; `tail -n +16 code/spectral_O12.py \| shasum -a 256` returns the sha256 above |

Why this copy. Nine copies of `spectral_O12.py` exist in the workspace (O12-O15 are byte-identical, sha256 `5e513726...`; O25, O26,
O32, Q1 and Q5a differ in other parts of the file, sha256 respectively `6cd3788b...`, `1eb44b7e...`, `6bb281e3...`,
`4710ccb0...`, `95973960...`). The six functions and the constant used by `trajectory_branching.py` (and the helpers
they call, `heisenberg_mul_batch`, `weil_batch_lut`) have identical source text in all nine copies (checked function by function), so the choice
of copy does not influence any result of this note. The O25 copy is the one the script originally pointed to
(`../o25`). Only the function bodies listed above are exercised; the rest of the file (the O12 campaign driver,
figures, tables) is dead code for this repository and is kept so that the file stays a verbatim copy.

Change to `trajectory_branching.py` accompanying the vendoring: the line `sys.path.insert(0, HERE/../o25)` now
inserts `HERE` (the directory of the script), and the `REQUIRES` line of the docstring names the vendored module.
No computation changed.

## Seeds and data inputs

- No external data file is read. All inputs are generated: Heisenberg graph `Heis_3(Z/qZ)` by BFS, seeded random
  paths and probes.
- `trajectory_branching.py`: `--seed` default 42; path/block RNG `default_rng(seed + q)`; probe
  `|phi0>` = seeded complex Gaussian with seed `777000 + q` (stored in the npz); `symbols` are float32.
- `v3_exact_check.py`: seeds 1 (q = 101) and 2 (q = 211). `amirror_recon.py`: seed 7. `amirror_mixed_coeff.py`:
  seed 11. `amirror_jet_certify.py`: seed 17. `wn_recon.py`: deterministic.
- Stored campaign outputs (not versioned here, 9 MB): the four `q{q}_traj.npz` of the workspace directory
  `simulation/spectral/trajectory-entropy/traj_outputs/` (4 July 2026). `trajectory_branching.py` regenerates them
  (the reproduction check of 8 October 2026 reproduces every metadata field, `phi0`, `cs`, `ranks_o12`,
  `ranks_gab` and `shell_sizes` exactly; `symbols` bit-identically for q = 211, and for q = 29, 61, 101 to at most
  4.3e-8 absolute (float32 noise), with all estimators h_2, h_low, h_up identical for every variant and epsilon).
- Parameters actually used by the campaign, as stored in the `npz` metadata (all: seed 42, `--n-blocks` 3, i.e. three
  conjugate block pairs, `symbols` of shape (3 variants, 3 blocks, T, n_steps)):

  | q | T | n_steps (script constant) | conjugate-pair indices c | command |
  |---|---|---|---|---|
  | 29 | 100000 (= script default) | 8 | 1, 1, 1 | `--primes 29 211 --T 100000` |
  | 61 | 20000 | 12 | 17, 20, 22 | `--primes 61 101 --T 20000` |
  | 101 | 20000 | 14 | 32, 32, 50 | `--primes 61 101 --T 20000` |
  | 211 | 100000 | 12 (fallback constant) | 33, 82, 30 | `--primes 29 211 --T 100000` |

  The script default `--T` is 100000, so q = 29 and 211 are the runs at the default and q = 61, 101 the runs with
  `--T 20000`; the note states these values per prime (Section "Numerical Evidence").
- Default output directory of `trajectory_branching.py`: `code/traj_outputs/` (`OUTPUT_DIR = HERE/traj_outputs`);
  `--out-dir` overrides it. `.gitignore` excludes the regenerated `code/traj_outputs/*.npz`.
- `trajectory_branching_h.pdf` (the figure of the note, `\includegraphics{../code/trajectory_branching_h}`) is the
  output of the 4 July 2026 campaign, committed as a binary; `traj_outputs/trajectory_branching_h.pdf` is a byte-identical
  duplicate. The command that regenerates the figure is given in the README.

## Per-script description

| script | inputs / arguments | outputs | seed | claim supported |
|---|---|---|---|---|
| `trajectory_branching.py` | `--primes` (default 29 61 101), `--T` (default 100000), `--n-blocks` (3), `--seed` (42), `--out-dir` (default `code/traj_outputs/`), `--force`, `--plot-only`; imports `spectral_O12` | `q{q}_traj.npz`, `trajectory_branching_h.pdf`, entropy-rate tables on stdout | 42 (+q), phi0: 777000+q | Section "Numerical Evidence": the figure, the V1 collapse control, the V2 rate approaching log(1+sqrt 2), the V3 rank sequence 1, 5, 13, 25, ...; it generates the q = 211 data read by `pell_counts.py` |
| `pell_counts.py` | `--data-dir` (default `code/traj_outputs/`; reads `q211_traj.npz`), `--regenerate` (recompute the q = 211 symbols in memory), `--exact-only`; imports `trajectory_branching` | table and `PASS` on stdout, exit status 1 on any mismatch with the note | deterministic exact part; sampled part: path ensemble `default_rng(42 + 211)` (the generator state `run_one_prime` uses first), symbols from the npz | Table `tab:pell` (exact N_b(n) by Pell recursion, transfer matrix and enumeration; distinct sampled b-sequences and distinct V2 profiles, q = 211, n = 1..12; 8096, 18675, 37394 at n = 10, 11, 12) and the epsilon = 10^-3 refinement h_2 = 0.885, 0.881, 0.877 (n = 5, 6, 7, mean of the three blocks) |
| `v3_exact_check.py` | none (q = 101, 211; n <= 7) | PASS/FAIL lines on stdout, exit code | 1, 2 | Table `tab:v3-count` and the verified checks C1-C5 of Section 6 (Gabor rank, geodesic death, outward geodesic count, closed-form class count, Chebotarev witness) |
| `amirror_recon.py` | none; imports `v3_exact_check` | three findings on stdout | 7 | Recon of the a-mirror front: real-Fourier probes collapse to the Burnside count (4, 10, 24, 54, 116), single-edge probes are degenerate, two-edge probes separate; supports the motivation of Section 6.5, no number printed in the note |
| `amirror_mixed_coeff.py` | none; imports `v3_exact_check` | certification lines, `ALL PASS` | 11 | Remark `rem:amirror-certification`: eps^2 identity and kernel formula for the mixed two-anchor coefficient S |
| `amirror_jet_certify.py` | none; imports `amirror_mixed_coeff` | certification lines, `ALL PASS` | 17 | Remark `rem:amirror-certification`: moment reduction, vanishing at the orthogonal point, closed-form Hermitian jets (Lemma `lem:orthogonal-moment-hermitian-jet`) |
| `wn_recon.py` | none (standard library) | exact count sequences, rates, candidate mappings on stdout | none | Exploratory: numerics behind the qualitative statements of Section "evolving equation of state" (finite-n correction ~ n 2^-n, no forced count-to-density mapping); its w values are not in the note |
| `spectral_O12.py` | vendored module, see above | none (imported) | n/a | none directly; dependency of `trajectory_branching.py` |

## Known debt

- `wn_recon.py` and `amirror_recon.py` support no retained numerical result of the note (recon scripts); they are
  kept for history and for the reader who wants to see where the statements come from.
- `amirror_mixed_coeff.py` cites in its docstring a recovery note (`RECOVERY-NOTE-front-amirror-separation.md`) that is
  not in this repository.
- The docstrings of `v3_exact_check.py` and `amirror_recon.py` announce "a few minutes" of runtime; the measured
  runtime is a few seconds (see the README).
