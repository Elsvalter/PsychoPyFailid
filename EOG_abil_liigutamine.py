from pylsl import StreamInlet, resolve_stream
from psychopy import visual, core, event
import numpy as np
from collections import deque

# --- LSL streami leidmine
print("Otsin EEG LSL streami...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# --- Aken ja objekt
win = visual.Window([1000, 600], color='black')
circle = visual.Circle(win, radius=0.05, fillColor='red', lineColor='red', pos=(0, 0))

# --- Seaded
sampling_rate = 250  # Hz
buffer_len = 50      # mitu viimast väärtust keskmistame (~200ms @ 250Hz)
x_buffer = deque(maxlen=buffer_len)

# --- Skaleerimisfunktsioon
def scale_value(val, data_min=-4800, data_max=-2000, target_min=-0.8, target_max=0.8):
    val = np.clip(val, data_min, data_max)  # piirame müraga
    return ((val - data_min) / (data_max - data_min)) * (target_max - target_min) + target_min

# --- Põhiloop
while not event.getKeys():
    sample, timestamp = inlet.pull_sample()
    if not sample or len(sample) < 2:
        continue

    # hEOG signaal: parempoolne - vasakpoolne
    x_value = sample[0] - sample[1]
    print(x_value)
    x_buffer.append(x_value)

    # Liikuva keskmise arvutamine
    avg_x = np.mean(x_buffer)
    x_pos = scale_value(avg_x)
    print(x_pos)

    # Liiguta ringi
    circle.pos = (x_pos, 0)
    circle.draw()
    win.flip()

# --- Cleanup
win.close()
core.quit()
