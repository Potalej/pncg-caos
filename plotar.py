import numpy as np
import matplotlib.pyplot as plt

def rejeitar_outliers (data, m=2):
  d = np.abs(data - np.median(data))
  mdev = np.median(d)
  s = d/mdev if mdev else np.zeros(len(d))
  nova_data = data.copy()
  nova_data[s>=m] = np.mean(data[s<m])
  return nova_data

# def plotar_heatmap (out_put_dir:str, grid, xv, yv, R0, traj0, m=10, interp=None):
def plotar_heatmap (out_put_dir:str, grid, xv, yv, m=10, interp=None):
  fig, ax = plt.subplots(figsize=(8,8))
  
  # Rejeita os outliers
  lista = np.reshape(grid, -1)
  lista = rejeitar_outliers(lista, m)
  grid = np.reshape(lista, (len(xv),len(yv)))

  ax.imshow(grid, 
           cmap='hot',
           interpolation=interp,
           extent=[xv[0][0], xv[-1][-1], yv[0][0], yv[-1][-1]])
#   ax.scatter(R0[0][0], R0[0][1], color='white')

#   trajetoria_0 = list(zip(*list(zip(*Rs0))[0]))
#   ax.plot(*trajetoria_0[:2], color='white')
#   ax.set_xlim([xv[0][0], xv[-1][-1]])
#   ax.set_ylim([yv[0][0], yv[-1][-1]])
  
  fig.savefig(out_put_dir + '.jpg')