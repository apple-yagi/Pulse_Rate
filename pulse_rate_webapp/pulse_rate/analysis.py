import io
import pathlib
import numpy as np
from scipy import signal
from scipy import fftpack

import matplotlib.pyplot as plt

from .models import Pulse_Rate

def setPlt(pk):
    # 対象データを取得
    pulse_rate = Pulse_Rate.objects.get(pk=pk)
    path = pathlib.Path(pulse_rate.data.url)

    # データを読み込む
    f = open(path.resolve())
    lines = f.read().split()

    # -----変数の準備-----
    N = 4096
    lines_length = int(len(lines) / 2)
    if lines_length < N:
        N = 2048

    dt = float(lines[2]) - float(lines[0])
    pulse = []
    for num in range(N - 1):
        pulse.append(float(lines[num * 2 + 1]))
    # -------------------

    # -----サンプリング周波数計算-----
    t = np.arange(0, N * dt, dt)  # time
    freq = np.linspace(0, 1.0 / dt, N)  # frequency step
    # -----------------------------

    # -----波形の生成-----
    y = 0
    for pl in pulse:
        y += np.sin(2 * np.pi * pl * t)
    # -------------------

    # -----フーリエ変換-----
    # yf = fft(y)/(N/2) # 離散フーリエ変換&規格化
    yf = np.fft.fft(y)  # 高速フーリエ変換
    # --------------------

    # パワースペクトル算出
    yf_abs = np.abs(yf)

    # -----グラフの生成-----
    plt.figure()
    plt.subplot(211)
    plt.plot(t, y)
    # plt.xlim(0, 30)
    plt.xlabel("time")
    plt.ylabel("amplitude")
    plt.grid()

    plt.subplot(212)
    plt.plot(freq, yf_abs)
    plt.xlim(0, 10)
    plt.xlabel("frequency")
    plt.ylabel("amplitude")
    plt.grid()
    plt.tight_layout()
    # ----------------------


def set_filter_Plt(pk):
    # 対象データを取得
    pulse_rate = Pulse_Rate.objects.get(pk=pk)
    path = pathlib.Path(pulse_rate.data.url)

    # データを読み込む
    f = open(path.resolve())
    lines = f.read().split()

    # -----変数の準備-----
    N = 4096
    lines_length = int(len(lines) / 2)
    if lines_length < N:
        N = 2048

    dt = float(lines[2]) - float(lines[0])
    pulse = []
    for num in range(N - 1):
        pulse.append(float(lines[num * 2 + 1]))
    # -------------------

    # -----フィルタ設計-----
    fc_high_pass = pulse_rate.fc_high  # カットオフ周波数
    fc_low_pass = pulse_rate.fc_low  # ローパスフィルタカットオフ周波数
    fs = 1 / dt  # サンプリング周波数
    fc_upper = fs - fc_low_pass  # 上側のカットオフ　fc～fc_upperの部分をカット
    # ----------------------

    # -----サンプリング周波数計算-----
    t = np.arange(0, lines_length * dt, dt)  # time
    freq = np.linspace(0, 1.0 / dt, N)  # frequency step
    # -----------------------------

    # -----波形の生成-----
    y = 0
    for pl in pulse:
        y += np.sin(2 * np.pi * pl * t)
    # -------------------

    # -----フーリエ変換-----
    # yf = fft(y)/(N/2) # 離散フーリエ変換&規格化
    yf = np.fft.fft(y)  # 高速フーリエ変換
    # --------------------

    # パワースペクトル算出
    yf_abs = np.abs(yf)

    # -----フィルタ処理-----
    gf = yf.copy()

    # ハイパスフィルタ
    gf[(freq < fc_high_pass)] = 0
    gf[(freq > 1 / (dt * 2))] = 0

    # ローパスフィルタ
    gf[((freq > fc_low_pass) & (freq < fc_upper))] = 0 + 0j

    # パワースペクトル
    gf_abs = np.abs(gf)

    # 逆高速フーリエ変換
    g = np.fft.ifft(gf)

    maxId = signal.argrelmax(gf_abs, order=3)

    plt.figure(figsize=(10.0, 5.0))
    plt.subplot(221)
    plt.plot(t, y)
    # plt.xlim(0, 30)
    plt.xlabel("time")
    plt.ylabel("amplitude")
    plt.grid()

    plt.subplot(222)
    plt.plot(freq, yf_abs)
    plt.xlim(0, 10)
    plt.xlabel("frequency")
    plt.ylabel("amplitude")
    plt.grid()

    # plt.figure(2)
    plt.subplot(223)
    plt.plot(t, g)
    # plt.xlim(0, 30)
    plt.xlabel("time")
    plt.ylabel("amplitude")
    plt.grid()

    plt.subplot(224)
    plt.plot(freq, gf_abs)
    plt.xlim(0, 10)
    plt.xlabel("frequency")
    plt.ylabel("amplitude")
    plt.plot(freq[maxId], gf_abs[maxId], "ro")
    plt.grid()

    for i in range(len(maxId[0])):
        plt.text(freq[maxId[0][i]], gf_abs[maxId[0][i]], round(freq[maxId[0][i]], 2))
    plt.tight_layout()


def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s
