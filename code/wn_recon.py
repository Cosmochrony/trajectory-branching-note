"""w(n) recon: exact count sequences, rates, deficits, candidate EoS mappings (exact, no fit)."""
import math

ln = math.log
h_pell = ln(1 + math.sqrt(2))   # canonical rate
h_v3 = ln(2)                    # full-history rate

# Exact sequences
NB = [1, 3]
for n in range(2, 41):
    NB.append(2 * NB[-1] + NB[-2])
NV = {n: 2**(n + 2) - 4 * n - 1 for n in range(2, 41)}

print("n   N_b          N_V3         h_b(n)   h_V3(n)  dh_V3=h_V3(n)-ln2  gap(n)=h_b(n)-h_V3(n)")
for n in range(3, 21):
    hb = ln(NB[n] / NB[n - 1])
    hv = ln(NV[n] / NV[n - 1])
    print(f"{n:<3d} {NB[n]:<12d} {NV[n]:<12d} {hb:.6f} {hv:.6f} {hv - h_v3: .3e}          {hb - hv: .6f}")

print(f"\nasymptotic: h_b={h_pell:.6f}  h_V3={h_v3:.6f}  gap={h_pell - h_v3:.6f}")

# Candidate mappings (ALL imported, graded in the recon note); rho ~ a^{-3(1+w)} => w = -1 - (1/3) dln(rho)/dln(a)
print("\nM1 (rho ~ N_dist):    w_b = %.4f   w_V3 = %.4f  (constant, phantom side)"
      % (-1 - h_pell / 3, -1 - h_v3 / 3))
print("M2 (rho ~ ln N = S):  w(n) = -1 - 1/(3n); n=10: %.4f  n=60: %.4f  n=140: %.4f"
      % (-1 - 1 / 30, -1 - 1 / 180, -1 - 1 / 420))
print("M3 (rho ~ N_V3/N_b):  w = -1 + gap/3 = %.4f  (constant, quintessence side)"
      % (-1 + (h_pell - h_v3) / 3))

# V3 finite-n transient in w units under M1-type reading: dw(n) = -dh_V3(n)/3
print("\nV3 transient dw(n) = -(h_V3(n)-ln2)/3:")
for n in (3, 5, 7, 10, 15, 20):
    hv = ln(NV[n] / NV[n - 1])
    print(f"  n={n:<3d} dw = {-(hv - h_v3) / 3: .3e}")

# Under H-dict, the transient decays like a^{-ln2} (times log a): show the a-scaling
print("\ntransient envelope check: (h_V3(n)-ln2) * 2^n / n:")
for n in (6, 10, 14, 18):
    hv = ln(NV[n] / NV[n - 1])
    print(f"  n={n:<3d} {(hv - h_v3) * 2**n / n:.4f}")

# Channel-choice flag at low ell: V3 count at n=1 is 2 (X+- merge) => ceiling 1/2 at the quadrupole
print("\nlow-ell channel flag: V3 N(1)=2 => ceiling 1-1/2 = 0.5 vs canonical N(1)=3 => 2/3")
