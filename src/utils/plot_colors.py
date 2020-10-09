import brewer2mpl
from pylab import *
import pdb

def gen_colors(num_colors=7):
    # brewer2mpl.get_map args: set name  set type  number of colors
    # Each color type, sequential, qualitative, diverging has between 3 and 12 defined colors
    assert num_colors <= 12, "Number of colors cannot exceed 12!"
    num_colors = min(max(3, num_colors), 12)
    bmap = brewer2mpl.get_map('Set2', 'qualitative', num_colors) 
    colors = bmap.mpl_colors
    return colors
