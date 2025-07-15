import numpy as np


def ToBinary(门阵):
    n = len(门阵)
    二进制门阵 = np.zeros((n, n), dtype=int)
    nf = max(max(max(子列表) for 子列表 in 组) for 组 in 门阵)
    基数 = 1 << (nf - 1)
    for i in range(n):
        for j in range(n):
            二进制数 = 0
            for 元素 in 门阵[i][j]:
                二进制数 |= 基数 >> (元素 - 1)
            二进制门阵[i, j] = 二进制数
    return 二进制门阵


def GetBitInfo(门阵):
    n = len(门阵)
    nf = max(max(max(子列表) for 子列表 in 组) for 组 in 门阵)
    return n, nf


def ToIndex(二进制数, n):
    索引 = []
    起始 = 1 << (n - 1)
    for 位置 in range(n):
        if 二进制数 & (起始 >> 位置):
            索引.append(位置)
    return 索引


def XOR_Submatrix(矩阵, 行索引, 列索引):
    if len(行索引) > len(列索引):
        子矩阵 = 矩阵[np.ix_(列索引, 行索引)]
    else:
        子矩阵 = 矩阵[np.ix_(行索引, 列索引)]
    列异或 = np.bitwise_xor.reduce(子矩阵, axis=0)
    结果 = np.bitwise_xor.reduce(列异或)
    return 结果


def XOR_LowerTriangle(矩阵, 索引):
    # 下三角
    子矩阵 = 矩阵[np.ix_(索引, 索引)]
    n = len(索引)
    结果 = 0
    # 先按行进行处理
    for i in range(1, n):
        结果 ^= np.bitwise_xor.reduce(子矩阵[i, :i])
    return 结果


BitCount = np.vectorize(lambda x: x.bit_count())


def Classify(数量, 正负, 实虚):
    正负 = np.where(正负 == 0, 1, -1)
    过渡 = (实虚 + 1) * 正负

    N1系数 = np.zeros_like(正负)
    N1系数[过渡 == 1] = 1
    N1系数[过渡 == -3] = 1
    N1 = np.dot(N1系数, 数量)

    N2系数 = np.zeros_like(正负)
    N2系数[过渡 == 3] = 1
    N2系数[过渡 == -1] = 1
    N2 = np.dot(N2系数, 数量)

    N3系数 = np.zeros_like(正负)
    N3系数[过渡 == 4] = 1
    N3系数[过渡 == -2] = 1
    N3 = np.dot(N3系数, 数量)

    N4系数 = np.zeros_like(正负)
    N4系数[过渡 == -4] = 1
    N4系数[过渡 == 2] = 1
    N4 = np.dot(N4系数, 数量)

    return N1, N2, N3, N4


def print_Gate_Matrix(门阵):
    print('Gate Matrix:')

    行数 = len(门阵)
    列数 = len(门阵[0])

    # 计算每列的最大宽度
    列宽度 = [
        max(len(f"[{','.join(map(str, 门阵[i][j]))}]") for i in range(行数))
        for j in range(列数)]

    for i in range(行数):
        for j in range(列数):
            元素 = 门阵[i][j]
            格式化元素 = f"[{','.join(map(str, 元素))}]"  # 格式化为[a,b]
            print(格式化元素.center(列宽度[j]), end=' ')
        print()  # 换行


def print_Binary_Gate_Matrix(二进制门阵):
    print('Binary Gate Matrix:')

    # 计算最大值的二进制长度
    最大值 = int(np.max(二进制门阵))
    最大位数 = 最大值.bit_length()

    # 创建格式化字符串以保证二进制数字长度一致
    格式化字符串 = '{:0' + str(最大位数) + 'b}'

    # 遍历数组，逐行打印每个元素的二进制形式
    for 行 in 二进制门阵:
        for 数值 in 行:
            print(格式化字符串.format(int(数值)), end=' ')
        print()


def 对齐(i, j):
    # 将 i 和 j 转换成字符串，并用逗号分隔
    ij字符串 = f"{i},{j}"
    固定宽度 = 11  # 设定一个固定的宽度，确保无论 i 和 j 如何变化，都不影响后面内容的开始位置
    # 使用 ljust 方法确保 'i,j' 字符串长度至少为固定宽度，不足部分右侧填充空格
    前缀 = ij字符串.ljust(固定宽度)
    return 前缀


def print_αβ(ρ_true, ρ_meas):
    print('The parameters α_ij and β_ij:')
    d = len(ρ_true)
    for i in range(1, d):
        for j in range(i):
            print()
            print(f"i,j = {对齐(i, j)}α_true = {ρ_true[i, j].real:>13.10f}    β_true = {ρ_true[i, j].imag:>13.10f}")
            print(f"i,j = {对齐(i, j)}α_meas = {ρ_meas[i, j].real:>13.10f}    β_meas = {ρ_meas[i, j].imag:>13.10f}")

