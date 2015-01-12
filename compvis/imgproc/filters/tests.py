import numpy as np
import time

from linear import summed_area_table, summed_area_table_fast

#img = np.array(((3, 2, 7, 2, 3),
#                (1, 5, 1, 3, 4),
#                (5, 1, 3, 5, 1),
#                (4, 3, 2, 1, 6),
#                (2, 4, 1, 4, 8)))

img = np.random.random((1000, 1000))

t0 = time.time()
tab1 = summed_area_table(img)
t1 = time.time()
print t1 - t0

t0 = time.time()
tab2 = summed_area_table_fast(img)
t1 = time.time()
print t1 - t0

print abs(tab1 - tab2) < 1e-6
