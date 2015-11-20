# About

一筆書きの線画をスキャンして、頂点配列に変換するプログラムです。

# Usage

以下のように、線画を読み込ませます。

```python
figure = Figure('example.png')
```

以下のように、頂点配列にアクセスできます。

```python
figure.vertex
```

また、各頂点の外角を以下で取得できます。

```python
figure.angle
```

線画のスキャンのアニメーションを見れます。

```bash
python main.py
```

また、ipython notebookでいろいろ見れます。

# Requirement

`numpy`と`cv2`モジュールが必要です。
