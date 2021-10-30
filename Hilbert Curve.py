'''
https://github.com/PrincetonLIPS/numpy-hilbert-curve/blob/3568b109299185dc5bb4b885f9c7dd7264080997/examples/draw_2d.py
'''
import numpy             as np
import matplotlib.pyplot as plt

from hilbert import decode

num_dims = 2

def draw_curve(ax, num_bits):

  # The maximum Hilbert integer.
  max_h = 2**(num_bits*num_dims)

  # Generate a sequence of Hilbert integers.
  hilberts = np.arange(max_h)

  # Compute the 2-dimensional locations.
  locs = decode(hilberts, num_dims, num_bits)

  # Draw
  ax.plot(locs[:,0], locs[:,1], '.-')
  ax.set_aspect('equal')
  ax.set_title('%d bits per dimension' % (num_bits))
  ax.set_xlabel('dim 1')
  ax.set_ylabel('dim 2')


fig = plt.figure(figsize=(16,4))
for ii, num_bits in enumerate([2, 3, 4, 5]):
  ax = fig.add_subplot(1,4,ii+1)
  draw_curve(ax, num_bits)
plt.savefig('example_2d.png', bbox_inches='tight')
plt.show()