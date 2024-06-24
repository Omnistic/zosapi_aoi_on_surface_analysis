import matplotlib.pyplot as plt
import numpy as np
from System import Enum, Int32, Double

system_int32 = Int32(1)
system_double = Double(1.0)

surface = 2

wavenumber = 1

hx = 1
hy = 1

px_sampling = 16
py_sampling = 16

px_step = 2 / px_sampling
py_step = 2 / py_sampling

REAL_RAYS = ZOSAPI.Tools.RayTrace.RaysType.Real

batch_raytrace_tool = TheSystem.Tools.OpenBatchRayTrace()
norm_unpol_raytrace = batch_raytrace_tool.CreateNormUnpol(px_sampling*py_sampling, REAL_RAYS, surface)
norm_unpol_raytrace.ClearData()

for px_index in range(px_sampling):
    for py_index in range(py_sampling):
        px = -1 + px_index * px_step
        py = -1 + py_index * py_step
        norm_unpol_raytrace.AddRay(wavenumber, hx, hy, px, py, Enum.Parse(ZOSAPI.Tools.RayTrace.OPDMode, 'None'))

batch_raytrace_tool.RunAndWaitForCompletion()

if not norm_unpol_raytrace.HasResultData:
    raise Exception('ERROR: Raytrace unable to complete.')

norm_unpol_raytrace.StartReadingResults()

ray_data = norm_unpol_raytrace.ReadNextResult(system_int32,
                                              system_int32,
                                              system_int32,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,)

x_array = []
y_array = []

tanx_array = []
tany_array = []

while ray_data[0]:
    if not ( ray_data[2] and ray_data[3] ):
        x_array.append(ray_data[4])
        y_array.append(ray_data[5])
        tanx_array.append(ray_data[7]/ray_data[9])
        tany_array.append(ray_data[8]/ray_data[9])

    ray_data = norm_unpol_raytrace.ReadNextResult(system_int32,
                                              system_int32,
                                              system_int32,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,
                                              system_double,)

batch_raytrace_tool.Close()

color_array = np.sqrt(np.array(tanx_array)**2 + np.array(tany_array)**2)

plt.style.use('dark_background')

fig, ax = plt.subplots()
ax.quiver(x_array, y_array, tanx_array, tany_array, color_array, scale=2)
ax.set_aspect('equal')
ax.set_title(r'Arrow components are $\tan \theta_x$ and $\tan \theta_y$')
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
plt.show()