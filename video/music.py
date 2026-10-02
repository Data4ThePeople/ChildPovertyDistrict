"""Original background track for the tutorial video, synthesized in numpy (no samples, no licensing).
120 BPM, C major, I-V-vi-IV. Pad + arpeggio under the intro; beat from 4 s; drums drop at 42 s;
fade out by 45.2 s; a TV power-off zip and static blip at the switch-off. Writes video/build/music.wav."""
import wave
from pathlib import Path

import numpy as np

SR = 44100
DUR = 46.0
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
OUT = Path(__file__).resolve().parent / "build" / "music.wav"
rng = np.random.default_rng(7)

# I-V-vi-IV in C: chord tones (MIDI) and bass roots
CHORDS = [[60, 64, 67, 72], [59, 62, 67, 71], [57, 60, 64, 69], [57, 60, 65, 69]]
ROOTS = [36, 43, 45, 41]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a, d, sustain=0.0, release=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * (sustain + (1 - sustain) * np.exp(-t / max(d, 1e-4)))
    if release:
        r = int(release * SR)
        e[-r:] *= np.linspace(1, 0, r)
    return e


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):   # one-pole filter; fine for these lengths
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def place(buf, sig, t0):
    i = int(t0 * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i]


def main():
    n = int(DUR * SR)
    pad, arp, bass, drums, fx = (np.zeros(n) for _ in range(5))
    nbars = int(np.ceil(DUR / BAR))
    for b in range(nbars):
        t0 = b * BAR
        ch = CHORDS[b % 4]
        # pad: detuned saws, soft attack, filtered later
        m = int(BAR * SR)
        t = np.arange(m) / SR
        s = sum(((t * hz(note) * dt) % 1 - 0.5) for note in ch[:3] for dt in (0.997, 1.003))
        place(pad, s * env(m, 0.35, 10, 0.6, release=0.25) * 0.10, t0)
        # arpeggio: 16th notes up the chord, plucked sine with a soft second harmonic
        for k in range(16):
            note = ch[[0, 1, 2, 3, 2, 1, 2, 3][k % 8]] + 12
            mm = int(0.22 * SR)
            tt = np.arange(mm) / SR
            p = (np.sin(2 * np.pi * hz(note) * tt) + 0.25 * np.sin(4 * np.pi * hz(note) * tt)) * env(mm, 0.003, 0.09)
            vel = 0.13 if k % 4 == 0 else 0.08
            place(arp, p * vel, t0 + k * BEAT / 4)
        if t0 >= 4.0 - 1e-6:
            # bass: 8th notes on the root, plucked
            for k in range(8):
                mm = int(0.24 * SR)
                tt = np.arange(mm) / SR
                f = hz(ROOTS[b % 4] + (12 if k % 4 == 3 else 0))
                bsig = np.tanh(2.2 * np.sin(2 * np.pi * f * tt)) * env(mm, 0.004, 0.12)
                place(bass, bsig * 0.22, t0 + k * BEAT / 2)
            if t0 < 42.0:
                for k in range(4):
                    bt = t0 + k * BEAT
                    if k in (0, 2):   # kick
                        mm = int(0.25 * SR)
                        tt = np.arange(mm) / SR
                        f = 50 + 70 * np.exp(-tt / 0.03)
                        place(drums, np.sin(2 * np.pi * np.cumsum(f) / SR) * env(mm, 0.001, 0.12) * 0.55, bt)
                    else:             # clap: filtered noise burst
                        mm = int(0.18 * SR)
                        nz = rng.standard_normal(mm)
                        nz = nz - lowpass(nz, 900)
                        place(drums, nz * env(mm, 0.002, 0.05) * 0.22, bt)
                    for h in (0, 1):   # hats on 8ths
                        mm = int(0.05 * SR)
                        nz = rng.standard_normal(mm)
                        nz = nz - lowpass(nz, 6000)
                        place(drums, nz * env(mm, 0.001, 0.015) * (0.05 if h == 0 else 0.09), bt + h * BEAT / 2)
    pad = lowpass(pad, 1800)
    # TV power-off: falling zip at 44.2 s, short static blip at 44.9 s
    mm = int(0.55 * SR)
    tt = np.arange(mm) / SR
    f = 2200 * np.exp(-tt / 0.18) + 120
    place(fx, np.sin(2 * np.pi * np.cumsum(f) / SR) * env(mm, 0.005, 0.25) * 0.12, 44.2)
    mm = int(0.18 * SR)
    place(fx, rng.standard_normal(mm) * env(mm, 0.002, 0.06) * 0.10, 44.9)

    music = pad + arp + bass + drums
    t = np.arange(n) / SR
    fade = np.clip(t / 1.2, 0, 1) * np.clip((45.2 - t) / 3.0, 0, 1)
    mix = music * fade + fx
    # light stereo width: delay the pad and arp by 9 ms on the right channel
    d = int(0.009 * SR)
    width = np.zeros(n)
    width[d:] = ((pad + arp) * fade)[:-d]
    left = mix
    right = mix - (pad + arp) * fade + width
    st = np.stack([left, right], axis=1)
    st = st / np.max(np.abs(st)) * 10 ** (-1 / 20)   # peak -1 dBFS
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    print("wrote", OUT, f"{DUR:.1f} s")


if __name__ == "__main__":
    main()
