import matplotlib.pyplot as plt
import numpy as np

surface = 3
wavenumber = 1

hx_sampling = 3
hy_sampling = 3

hx_step = 2 / (hx_sampling - 1)
hy_step = 2 / (hy_sampling - 1)

px_sampling = 16
py_sampling = 16

px_step = 2 / px_sampling
py_step = 2 / py_sampling

fig, axes = plt.subplots(hx_sampling, hy_sampling)

for hx_index in range(hx_sampling):
    for hy_index in range(hy_sampling):
        hx = -1 + hx_index * hx_step
        hy = -1 + hy_index * hy_step

        aoi = []

        for px_index in range(px_sampling):
            for py_index in range(py_sampling):
                px = -1 + px_index * px_step
                py = -1 + py_index * py_step

                aoi.append(TheSystem.MFE.GetOperandValue(ZOSAPI.Editors.MFE.MeritOperandType.RAID,
                                                        surface,
                                                        wavenumber,
                                                        hx,
                                                        hy,
                                                        px,
                                                        py,
                                                        0.0,
                                                        0.0))
        
        aoi = np.reshape(np.asarray(aoi), (px_sampling, py_sampling))

        axes[hx_index, hy_index].imshow(aoi, extent=(-1, 1, -1, 1))
        axes[hx_index, hy_index].set_title(f'hx: {hx}, hy: {hy}')

fig.tight_layout()
plt.show()
