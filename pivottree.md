# Pivot Tree
Pivot Tree というデータ構造を Python で実装しました.

非負整数の多重集合を効率よく管理することができます.

実装については [平衡二分木を実装する - Qiita](https://qiita.com/Kiri8128/items/6256f8559f0026485d90) を参考にしました.

## コンストラクタ
```Python3
pt = PivotTree(max_value = (1 << 60) - 2)
```
0 以上 max_value 以下の値を扱えるようになります.

デフォルトでは $1.152921504606846974 \times 10^{18}$ 以下の非負整数を扱えます.

### 制約
- $0 \leq max\_ value$

### 計算量
- $O(1)$

$n = max\_ value + 1$ とします.

## len(pt) / pt.size()
格納されている要素数を返します.

### 計算量
- $O(1)$

TODO: 各メソッドの説明

## 使用例
https://github.com/tatyam-prime/SortedSet/tree/main/example
などを参考に, 平衡二分木を使える問題を並べてみました.

TODO: 各問題の簡単な解説

### ABC119-D

### ABC141-D

### ABC217-D

### ABC234-D

### ABC241-D

### ABC253-C

### ARC033-C

### PAST009-M
