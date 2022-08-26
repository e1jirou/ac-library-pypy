# Pivot Tree
Pivot Tree というデータ構造を Python で実装しました.

非負整数の多重集合を効率よく管理することができます.

実装については [平衡二分木を実装する - Qiita](https://qiita.com/Kiri8128/items/6256f8559f0026485d90) を参考にしました.

## コンストラクタ
```Python3
pt = PivotTree(n = (1 << 60) - 2)
```
0 以上 n 以下の値を扱えるようになります.

デフォルトでは $1.152921504606846974 \times 10^{18}$ 以下の非負整数を扱えます.

### 制約
- $0 \leq n$

### 計算量
- $O(1)$

## len(pt) / pt.size()
格納されている要素数を返します.

### 計算量
- $O(1)$

## insert(v, c = 1)
整数 v を c 個追加します.

### 制約
- $0 \leq v \leq n$
- $0 < c$

### 計算量
- $O(\log n)$

## gt_min(v) / geq_min(v) / lt_max(v) / leq_max(v)
それぞれ値が v より大きいものの中で最小, v 以上のものの中で最小, v より小さいものの中で最大, v 以下のものの中で最大となるノードを返します.

該当するノードが無かったとき, gt_min 及び geq_min は木の根を返し, lt_max 及び leq_max は None を返します.

### 制約
- gt_min: $v < n$
- geq_min: $v \leq n$

### 計算量
- $O(\log n)$

## begin() / rbegin()
それぞれ値が最大, 最小のノードを返します.

### 計算量
- $O(\log n)$

## min() / max()
それぞれ最小値, 最大値を返します.

### 計算量
- $O(\log n)$

## erase(v, c = float("inf"), nd = None)
整数 v を c 個削除します. v が c 個以下の場合, v は全て削除されます. デフォルトでは v を全て削除します.

ノード nd を指定すると, nd の子孫の中から値が v のノードを見つけて削除を行います.

### 制約
- $0 \leq v \leq n$

### 計算量
- $O(\log n)$

## empty()
コンテナが空のとき True, そうでないとき False を返します.

### 計算量
- $O(1)$

## pt[k] / pt.find_by_order(k)
それぞれ小さいほうから 0-indexed で k 番目の値, その値を含むノードを返します.

k 番目の値が存在しないときは, それぞれ木の根の値, 木の根を返します.

### 計算量
- $O(\log n)$

## count(v)
格納されている要素 v の個数を返します.

### 制約
- $0 \leq v \leq n$

### 計算量
- $O(\log n)$

## index(v)
v より小さいものの個数を返します.

### 計算量
- $O(\log n)$

## node.get() / node.count
node は node.get() が node.count 個格納されていることを表します.

### 計算量
- $O(1)$

## node.prev() / node.next()
それぞれ次に値が小さいノード, 次に値が大きいノードを返します.

### 計算量
- 償却 $O(1)$
- 最悪 $O(\log n)$

## 使用例
https://github.com/tatyam-prime/SortedSet/tree/main/example
などを参考に, 平衡二分木を使える問題を並べてみました.

### ABC119-D
leq_max, geq_min などを使用して解くことができます.

### ABC141-D
max, erase などを使用して解くことができます. 優先度付きキューを用いたほうが高速に解くことができます.

### ABC170-E
max, min, erase などを使用して解くことができます. 優先度付きキューを用いたほうが高速に解くことができます.

### ABC217-D
lt_max, gt_min などを使用して解くことができます.

### ABC234-D
find_by_order などを使用して解くことができます.

### ABC241-D
leq_max, geq_min, index, node.prev, node.next などを使用して解くことができます.

### ABC253-C
max, min, erase などを使用して解くことができます.

### ARC033-C
erase, find_by_order などを使用して解くことができます.

### PAST003-N
erase, geq_min などを使用して解くことができます.

### PAST009-M
erase, find_by_order などを使用して解くことができます.

### PAST010-M
erase, find_by_order, index などを使用して解くことができます.