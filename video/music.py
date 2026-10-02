"""Original background track for the tutorial video, synthesized in numpy (no samples, no licensing).

Reflective, ambient: slow A-minor-leaning pads (Am(add9) - Fmaj7 - C - Gsus) with a long synthetic
reverb, a faint band of filtered air, and a soft heartbeat pulse (lub-dub, about once a second)
during the tour. Quiet under the intro card, building gently, a swell into C(add9) as the logo
appears, then a clean cut with the TV switch-off and a soft power-down. About -24 dBFS RMS.
Writes video/build/music.wav (46 s, 44.1 kHz stereo)."""
import wave
from pathlib import Path

import numpy as np

SR = 44100
DUR = 46.0
OUT = Path(__file__).resolve().parent / "build" / "music.wav"
rng = np.random.default_rng(11)

CHORD_LEN = 4.5
CHORDS = [  # MIDI notes, voiced low and open
    [45, 52, 59, 60, 64],   # Am(add9): A E B C E
    [41, 48, 52, 57, 64],   # Fmaj7: F C E A E
    [48, 55, 60, 64, 67],   # C: C G C E G
    [43, 50, 55, 60, 62],   # Gsus: G D G C D
]
LOGO_CHORD = [36, 48, 55, 62, 64, 67]   # C(add9), for the swell into the logo
T_PULSE_ON, T_PULSE_OFF, T_LOGO, T_CUT = 4.0, 40.0, 40.0, 44.2


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def onepole(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def pad_voice(notes, start, length, level):
    """Soft pad: detuned triangle-ish voices, slow swell in and out."""
    n = int(length * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for m in notes:
        for det in (-0.006, 0.0, 0.007):
            f = hz(m) * (1 + det)
            ph = (t * f + rng.random()) % 1.0
            sig += (2 * np.abs(2 * ph - 1) - 1) * (0.7 if m < 50 else 0.45)
    att, rel = 1.6, 2.2
    env = np.minimum(1, t / att) * np.minimum(1, np.maximum(0, (length - t) / rel))
    return start, sig * env * level / len(notes)


def place(buf, start, sig):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i]


def reverb(x, seconds=4.2, seed=3):
    """Convolution with a decaying, darkened noise tail (FFT)."""
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-t * 6.9 / seconds)
    ir = onepole(ir, 2500)
    ir[: int(0.012 * SR)] = 0   # short pre-delay
    ir /= np.sqrt((ir ** 2).sum())
    m = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]
    return y


def main():
    n = int(DUR * SR)
    t = np.arange(n) / SR
    pads = np.zeros(n)
    # chords overlap by their release so the pad never drops out
    k = 0
    start = 0.0
    while start < T_LOGO - 0.5:
        s0, sig = pad_voice(CHORDS[k % 4], start, CHORD_LEN + 2.2, 1.0)
        place(pads, s0, sig)
        start += CHORD_LEN
        k += 1
    s0, sig = pad_voice(LOGO_CHORD, T_LOGO - 0.8, (T_CUT + 0.1) - (T_LOGO - 0.8), 1.15)
    place(pads, s0, sig)
    pads = onepole(pads, 1100)

    # air: band-limited noise, slowly breathing
    air = rng.standard_normal(n)
    air = onepole(air, 3200) - onepole(air, 250)
    air *= 0.5 + 0.5 * np.sin(2 * np.pi * t / 9.0) ** 2
    air *= 0.05

    # heartbeat: lub-dub roughly once a second, low and muted
    pulse = np.zeros(n)
    period = 1.05
    tb = T_PULSE_ON
    while tb < T_PULSE_OFF:
        for off, vel in ((0.0, 1.0), (0.24, 0.55)):
            m = int(0.30 * SR)
            tt = np.arange(m) / SR
            f = 42 + 26 * np.exp(-tt / 0.04)
            thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.11) * np.minimum(1, tt / 0.006)
            place(pulse, tb + off, thump * vel * 0.32)
        tb += period
    pulse_env = np.clip((t - T_PULSE_ON) / 2.5, 0, 1) * np.clip((T_PULSE_OFF + 0.4 - t) / 0.8, 0, 1)
    pulse = onepole(pulse * pulse_env, 400)

    # stereo: two reverbs with different tails for width
    dry = pads + air
    left = 0.45 * dry + 0.75 * reverb(dry, seed=3) + pulse
    right = 0.45 * dry + 0.75 * reverb(dry, seed=5) + pulse

    # arc: quiet intro, gentle build through the tour, swell into the logo, hard cut at the switch-off
    arc = np.interp(t, [0, 3.5, 4.5, 38.0, 40.0, 41.5, 43.6, T_CUT, T_CUT + 0.06, DUR],
                       [0.0, 0.42, 0.55, 0.78, 0.85, 1.0, 1.0, 0.85, 0.0, 0.0])
    left *= arc
    right *= arc

    # soft power-down at the switch-off: a low falling tone and a faint static breath
    m = int(0.6 * SR)
    tt = np.arange(m) / SR
    f = 900 * np.exp(-tt / 0.2) + 60
    zip_ = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.22) * 0.05
    st = rng.standard_normal(int(0.15 * SR)) * np.exp(-np.arange(int(0.15 * SR)) / SR / 0.05) * 0.03
    for ch in (left, right):
        place(ch, T_CUT, zip_)
        place(ch, T_CUT + 0.7, st)

    mix = np.stack([left, right], axis=1)
    rms = np.sqrt((mix[int(4 * SR):int(40 * SR)] ** 2).mean())
    mix *= 10 ** (-24 / 20) / rms            # tour section at -24 dBFS RMS
    peak = np.abs(mix).max()
    if peak > 10 ** (-3 / 20):
        mix *= 10 ** (-3 / 20) / peak
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())
    print("wrote", OUT)


if __name__ == "__main__":
    main()
