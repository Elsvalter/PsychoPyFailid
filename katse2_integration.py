from pylsl import StreamInlet, resolve_stream
from psychopy import visual, core, event
import numpy as np

# --- LSL streami leidmine
print("Otsin EEG LSL streami...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# --- Aken
win = visual.Window([1000, 600], color='black')

# --- Seaded
sampling_rate = 250  # Hz
duration_sec = 10    # Kuvame 10 sekundit korraga
n_samples = sampling_rate * duration_sec

data_ch1 = [0] * n_samples
data_ch2 = [0] * n_samples

line_ch1 = visual.Line(win, lineColor='red')
line_ch2 = visual.Line(win, lineColor='green')

def scale_signal(data, target_min=-0.5, target_max=0.5):
    data = np.array(data)
    d_min, d_max = np.min(data), np.max(data)
    if d_max == d_min:
        return np.zeros_like(data)
    return (data - d_min) / (d_max - d_min) * (target_max - target_min) + target_min

frame_count = 0

# --- Põhiloop
while not event.getKeys():
    sample, timestamp = inlet.pull_sample()
    if not sample or len(sample) < 2:
        continue

    data_ch1.append(sample[0])
    data_ch1.pop(0)
    data_ch2.append(sample[1])
    data_ch2.pop(0)

    frame_count += 1
    if frame_count % 10 != 0:
        continue  # uuenda vaid iga 10. prooviga (~25Hz)

    # Skaleerime visualiseerimiseks
    y1 = scale_signal(data_ch1)
    y2 = scale_signal(data_ch2)

    # Aja telg (-10 kuni 0 s)
    x = np.linspace(-duration_sec, 0, n_samples)

    # Nihutame jooni, et need ei kattuks
    line_ch1.setVertices(list(zip(x, y1 + 0.4)))
    line_ch2.setVertices(list(zip(x, y2 - 0.4)))

    # Joonista
    line_ch1.draw()
    line_ch2.draw()
    win.flip()

# --- Cleanup
win.close()
core.quit()
