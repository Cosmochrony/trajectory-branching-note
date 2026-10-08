"""
pell_counts.py
==============
Reproduces Table `tab:pell` of the note and the post-hoc refinement eps = 1e-3 quoted in Section V2.

WHAT IT COMPUTES
----------------
1. DETERMINISTIC columns (no data, no seed):
   * N_b(n), n = 1..12, by three independent routes that must agree: the Pell recursion
     N_b(n) = 2 N_b(n-1) + N_b(n-2) (N_b(1) = 3, N_b(2) = 7), the transfer matrix
     N_b(n) = 1^T M^(n-1) u, and brute-force enumeration of the set of b-increment sequences of all
     non-backtracking words (generator order X, X^-1, Y, Y^-1, increments of b read from
     `spectral_O12.build_generators`, inverse of generator i is i XOR 1).
2. SAMPLED columns at q = 211, T = 10^5 (seed 42):
   * the T = 10^5 non-backtracking paths are those of `trajectory_branching.run_one_prime`
     (`default_rng(seed + q)`, first draw sequence = `sample_paths`); "distinct b-sequences (sampled)" at
     depth n is the number of distinct rows (b_1, ..., b_n) of the sampled path positions (b is the second
     Heisenberg coordinate, no wrap for n < q/2);
   * "distinct profiles (sampled)" at depth n is the number of distinct rows (s_1, ..., s_n) of the V2
     (generic probe, O12 basis) float32 symbols, compared exactly (machine precision, no binning), for each of
     the three conjugate block pairs;
   * h_2(n) at eps = 1e-3: `estimators_for_eps(symbols[V2, block], 1e-3)[0]`, mean over the three blocks.
   The symbols are read from `q211_traj.npz` (default `--data-dir`: `traj_outputs/` next to this script, where
   `trajectory_branching.py --primes 211 --T 100000` writes it; its q = 211 output is bit-identical to the
   stored campaign data), or regenerated in memory with `--regenerate` (about 1 minute).

ACCEPTANCE
----------
The script compares every number with the values printed in the note and exits with status 1 on any
mismatch.  Nothing is random here: the only randomness is the seeded path ensemble above.

USAGE
-----
python code/trajectory_branching.py --primes 211 --T 100000     # writes code/traj_outputs/q211_traj.npz
python code/pell_counts.py                                       # reads it
python code/pell_counts.py --regenerate                          # or recompute the symbols in memory
python code/pell_counts.py --data-dir DIR                        # npz in another directory
python code/pell_counts.py --exact-only                          # deterministic part only, no data

REQUIRES: numpy, and the vendored module spectral_O12.py (through trajectory_branching.py).
"""

import argparse
import os
import pathlib
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import trajectory_branching as tb  # noqa: E402

Q, T, N_STEPS, SEED, N_BLOCKS = 211, 100_000, 12, 42, 3
V2 = tb.VARIANTS.index("V2_generic_o12")

# Values printed in Table tab:pell and Section V2 of the note.
TEX_EXACT = [3, 7, 17, 41, 99, 239, 577, 1393, 3363, 8119, 19601, 47321]
TEX_SAMPLED = [3, 7, 17, 41, 99, 239, 577, 1393, 3363, 8096, 18675, 37394]
TEX_H2_EPS1E3 = {5: 0.885, 6: 0.881, 7: 0.877}


def exact_pell(n_max):
    """N_b(n) by the Pell recursion."""
    nb = [3, 7]
    while len(nb) < n_max:
        nb.append(2 * nb[-1] + nb[-2])
    return nb[:n_max]


def exact_transfer(n_max):
    """N_b(n) = 1^T M^(n-1) u (transfer matrix of the classes {0, +1, -1})."""
    M = np.array([[1, 1, 1], [1, 1, 0], [1, 0, 1]], dtype=np.int64)
    u = np.ones(3, dtype=np.int64)
    out, v = [], u.copy()
    for _ in range(n_max):
        out.append(int(v.sum()))
        v = M @ v
    return out


def exact_enumeration(q, n_max):
    """N_b(n) by enumeration of the b-increment sequences of non-backtracking words."""
    gens = tb.build_generators(q)
    inc = [int(g[1]) for g in gens]               # b-increment of each generator
    states = {(g, (inc[g],)) for g in range(4)}    # (last generator, b-increment sequence)
    out = [len({s for _, s in states})]
    for _ in range(1, n_max):
        states = {(g, s + (inc[g],)) for (last, s) in states for g in range(4) if g != (last ^ 1)}
        out.append(len({s for _, s in states}))
    return out


def sampled_b_rows(q, T, n_steps, seed):
    """Sampled b-coordinates of the paths of `run_one_prime`: array (T, n_steps)."""
    rng = np.random.default_rng(seed + q)           # first consumer of the generator in run_one_prime
    gens = tb.build_generators(q)
    positions = tb.sample_paths(q, gens, T, n_steps, rng)
    return positions[:, :, 1].T.copy()


def count_rows(a):
    return len(np.unique(np.ascontiguousarray(a), axis=0))


def main():
    p = argparse.ArgumentParser(description="Table tab:pell and the eps = 1e-3 refinement of the note")
    p.add_argument("--data-dir", type=pathlib.Path, default=tb.OUTPUT_DIR,
                   help="directory holding q211_traj.npz (default: code/traj_outputs)")
    p.add_argument("--regenerate", action="store_true",
                   help="recompute the q = 211 symbols in memory (about 1 minute) instead of reading the npz")
    p.add_argument("--exact-only", action="store_true", help="deterministic columns only")
    args = p.parse_args()
    ok = True

    print("pell_counts.py  (Table tab:pell, q = 211, T = 10^5, seed 42)")
    e_pell, e_tm, e_enum = exact_pell(N_STEPS), exact_transfer(N_STEPS), exact_enumeration(Q, N_STEPS)
    exact_ok = e_pell == e_tm == e_enum == TEX_EXACT
    ok &= exact_ok
    print(f"\nN_b(n), n = 1..{N_STEPS}: Pell {e_pell}\n  transfer matrix equal: {e_tm == e_pell};"
          f" enumeration equal: {e_enum == e_pell}; equal to the table: {exact_ok}")
    if args.exact_only:
        print("\nPASS (exact part)" if ok else "\nFAIL (exact part)")
        return 0 if ok else 1

    if args.regenerate:
        print(f"\nregenerating the q = {Q} symbols in memory (T = {T}, seed {SEED}) ...", flush=True)
        res = tb.run_one_prime(Q, T, N_BLOCKS, SEED, verbose=False)
    else:
        path = args.data_dir / f"q{Q}_traj.npz"
        if not path.exists():
            print(f"\nMissing {path}.  Generate it with\n"
                  f"  python code/trajectory_branching.py --primes {Q} --T {T} --out-dir {args.data_dir}\n"
                  f"or run this script with --regenerate.")
            return 2
        z = np.load(path)
        res = {k: z[k] for k in z.files}
        print(f"\nread {path}")
    meta_ok = (int(res["q"]), int(res["T"]), int(res["seed"]), int(res["n_steps"])) == (Q, T, SEED, N_STEPS)
    print(f"metadata q, T, seed, n_steps = {int(res['q'])}, {int(res['T'])}, {int(res['seed'])},"
          f" {int(res['n_steps'])}  (expected {Q}, {T}, {SEED}, {N_STEPS}): {meta_ok}")
    ok &= meta_ok
    symbols = res["symbols"]                        # (variants, blocks, T, n_steps) float32

    b_rows = sampled_b_rows(Q, T, N_STEPS, SEED)
    nb_samp = [count_rows(b_rows[:, :n]) for n in range(1, N_STEPS + 1)]
    prof = [[count_rows(symbols[V2, blk, :, :n]) for n in range(1, N_STEPS + 1)] for blk in range(N_BLOCKS)]

    print(f"\n{'n':>3} {'N_b exact':>10} {'b-seq sampled':>14} {'profiles blk0':>14} {'blk1':>8} {'blk2':>8}")
    for n in range(N_STEPS):
        print(f"{n+1:>3} {e_pell[n]:>10} {nb_samp[n]:>14} {prof[0][n]:>14} {prof[1][n]:>8} {prof[2][n]:>8}")
    samp_ok = nb_samp == TEX_SAMPLED and all(pr == TEX_SAMPLED for pr in prof)
    ok &= samp_ok
    print(f"sampled b-sequences and profiles (all three blocks) equal to the table: {samp_ok}")

    h2 = np.mean([tb.estimators_for_eps(symbols[V2, blk], 1e-3)[0] for blk in range(N_BLOCKS)], axis=0)
    print("\nh_2(n) at eps = 1e-3 (V2, mean over the three blocks): "
          + ", ".join(f"n={n}: {h2[n-1]:.4f}" for n in range(1, N_STEPS + 1)))
    h2_ok = all(round(float(h2[n - 1]), 3) == v for n, v in TEX_H2_EPS1E3.items())
    ok &= h2_ok
    print(f"rounded to 3 decimals, n = 5, 6, 7: {[round(float(h2[n-1]), 3) for n in (5, 6, 7)]}"
          f" (note: 0.885, 0.881, 0.877): {h2_ok}")
    print(f"log(1+sqrt 2) = {tb.H_B_SHADOW:.4f}")

    print("\nPASS" if ok else "\nFAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
