from pylsl import StreamInlet, resolve_stream
from psychopy import visual, core, event
import numpy as np

# --- LSL streami leidmine
print("Otsin EEG LSL streami...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# --- Aken
win = visual.Window([1000, 400], color='black')

# --- Jooned kanalitele 1 ja 2 (init tühi)
n_samples = 250  # mitu punkti joonel (umbes 1 sekund @250Hz)
data_ch1 = [0] * n_samples
data_ch2 = [0] * n_samples

line_ch1 = visual.Line(win, start=(0, 0), end=(0, 0), lineColor='red')
line_ch2 = visual.Line(win, start=(0, 0), end=(0, 0), lineColor='green')

# --- Põhiloop
while not event.getKeys():
    sample, timestamp = inlet.pull_sample()

    # Värskenda andmejärjestusi
    data_ch1.append(sample[0])
    data_ch1.pop(0)
    data_ch2.append(sample[1])
    data_ch2.pop(0)

    window_size = 20  # Liikuva akna suurus (nt 20 viimast andmepunkti)
    mean_ch1 = np.mean(data_ch1[-window_size:])
    mean_ch2 = np.mean(data_ch2[-window_size:])

    # Skaleeri Y-koordinaadid (µV → visuaal)
    y1 = (np.array(data_ch1) - mean_ch1) / 50000  # Kohalik keskmine eemaldatud
    y2 = (np.array(data_ch2) - mean_ch2) / 50000 + 0.2

    # X-koordinaat: aja järjekorras
    time = np.arange(n_samples) / 250  # eeldame, et 250 samples/sekundis
    x = time - time[-1]  # teha nii, et aeg liigub vasakult paremale
    # Värskenda jooni
    line_ch1.setVertices(list(zip(x, y1)))
    line_ch2.setVertices(list(zip(x, y2)))

    # Joonista
    line_ch1.draw()
    line_ch2.draw()
    win.flip()

# --- Cleanup
win.close()
core.quit()
