from func_lib import *


# ------ ↓↓↓↓ Input ↓↓↓↓ -------------------------------------------------------------------------------

# Gate Matrix: G
G = [[[1], [1, 2]], [[1, 2], [2]]]

# Measurement Outcome Vector: qf, for example: 0000, 0001, 0010, 0011, ...
qf = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], dtype=np.int64)
# Count Vector: N_qf
N_qf = np.array([79283, 46478, 46874, 1181, 22585, 14860, 17136, 13067, 17966, 20842, 12602, 9263, 5154, 42661, 48700, 101348], dtype=np.int64)
Measured_Diagonal_Data = np.array([0.22087, 0.234442, 0.264606, 0.280082])

# Reference Quantum State: ρ_true, for display of results only
# State: [1.3, 0.9 + 1.1j]⊗[1.4, 0.8 + 1.2j]
ρ_true = np.array([[0.2209975715 + 0j, 0.1262843265 - 0.1894264898j, 0.1529983187 - 0.1869979451j, -0.0728563422 - 0.2379973846j], [0.1262843265 + 0.1894264898j, 0.2345280350 - 0.0000000000j, 0.2477115636 + 0.0242854474j, 0.1623655627 - 0.1984467989j], [0.1529983187 + 0.1869979451j, 0.2477115636 - 0.0242854474j, 0.2641509434 - 0.0000000000j, 0.1509433962 - 0.2264150943j], [-0.0728563422 + 0.2379973846j, 0.1623655627 + 0.1984467989j, 0.1509433962 + 0.2264150943j, 0.2803234501 - 0.0000000000j]], dtype=np.complex128)

# ------ ↓↓↓↓ Density Matrix Reconstruction ↓↓↓↓ -------------------------------------------------------

Gb = ToBinary(G)
n, nf = GetBitInfo(G)

ρ = np.zeros((2**n, 2**n), dtype=np.complex128)

for i in range(1, 2 ** n):
    for j in range(i):
        L = i ^ j
        RowIdx = ToIndex(L, n)
        ColIdx = ToIndex(j, n)

        F1 = XOR_Submatrix(Gb, RowIdx, ColIdx)
        F2 = XOR_LowerTriangle(Gb, RowIdx)
        F = F1 ^ F2
        LF = (L << nf) ^ F

        N_1 = BitCount(qf & LF) % 2
        Ni = BitCount(qf & (L << (nf - n))) % 4
        N1, N2, N3, N4 = Classify(N_qf, N_1, Ni)

        Nα = N1 + N2
        Nβ = N3 + N4

        α = N1 / Nα - 0.5
        β = N3 / Nβ - 0.5

        ρ[i, j] = α + β * 1j
        ρ[j, i] = α - β * 1j

np.fill_diagonal(ρ, Measured_Diagonal_Data)

# Output: ρ

# ------ ↓↓↓↓ Results Display ↓↓↓↓ ---------------------------------------------------------------------

print()
print_Gate_Matrix(G)
print()
print_Binary_Gate_Matrix(Gb)
print()
print_αβ(ρ_true, ρ)


