"""
**********
Matplotlib
**********
Draw hypergraphs with matplotlib.
"""
import xgi
from xgi.drawing.layout import (
    barycenter_spring_layout,
)

__all__ = [
    "draw_hypergraph",
    "draw_2d_hypergraph",
]

def draw_2d_hypergraph(H, pos, ax=None):      ################# I NEED TO FROM HERE
    """
    Draw hypergraph up to to dimension 2.
        
        Args
        ----
        H: xgi Hypergraph.
        
        pos: dict (default=None)
            If passed, this dictionary of positions d:(x,y) is used for placing the 0-simplices.
           
        ax: matplotlib.pyplot.axes (default=None)
    """
    import matplotlib.pyplot as plt
    
    #List of 0-simplices
    nodes = list(H.nodes)
    #List of 1-simplices
    edges = list(H.edges_of_order(1).values())
    #List of 2-simplices
    triangles = list(H.edges_of_order(2).values())
        
    if ax is None: ax = plt.gca()
    ax.set_xlim([-1.1, 1.1])      
    ax.set_ylim([-1.1, 1.1])
    ax.get_xaxis().set_ticks([])  
    ax.get_yaxis().set_ticks([])
    ax.axis('off')

    # Drawing the edges
    for i, j in edges:
        (x0, y0) = pos[i]
        (x1, y1) = pos[j]
        line = plt.Line2D([ x0, x1 ], [y0, y1 ],color = 'black', zorder = 1, lw=0.7)
        ax.add_line(line);
    
    # Filling in the triangles
    for i, j, k in triangles:
        (x0, y0) = pos[i]
        (x1, y1) = pos[j]
        (x2, y2) = pos[k]
        tri = plt.Polygon([ [ x0, y0 ], [ x1, y1 ], [ x2, y2 ] ],
                          edgecolor = 'black', facecolor = plt.cm.Blues(0.6),
                          zorder = 2, alpha=0.4, lw=0.5)
        ax.add_patch(tri);

    # Drawing the nodes 
    for i in nodes:
        (x, y) = pos[i]
        circ = plt.Circle([ x, y ], radius = 0.02, zorder = 3, lw=0.5,
                          edgecolor = 'Black', facecolor = u'#ff7f0e')
        ax.add_patch(circ);
        
def draw_hypergraph(H, pos, ax=None):
    """
    Draw hypergraph.
        
        Args
        ----
        H: xgi Hypergraph.
        
        pos: dict (default=None)
            If passed, this dictionary of positions d:(x,y) is used for placing the 0-simplices.
           
        ax: matplotlib.pyplot.axes (default=None)
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    import palettable as pltt
    import numpy as np

    def ccw_sort(p):
        p = np.array(p)
        mean = np.mean(p,axis=0)
        d = p-mean
        s = np.arctan2(d[:,0], d[:,1])
        return p[np.argsort(s),:]

            
    if ax is None: ax = plt.gca()
    ax.set_xlim([-1.1, 1.1])      
    ax.set_ylim([-1.1, 1.1])
    ax.get_xaxis().set_ticks([])  
    ax.get_yaxis().set_ticks([])
    ax.axis('off')
    
    #Defining colors, one for each dimension
    d_max = H.max_edge_order()
    colors = [ListedColormap(pltt.colorbrewer.qualitative.Paired_12.mpl_colors)(i) for i in range(0, d_max+1)]
    
    #Looping over the hyperedges of different order (reversed) -- nodes will be plotted separately
    for d in reversed(range(1, d_max+1)):
        if d==1:
            # Drawing the edges
            for he in list(H.edges_of_order(d).values()):
                x_coords = [pos[he[0]][0], pos[he[1]][0]]
                y_coords = [pos[he[0]][1], pos[he[1]][1]]
                line = plt.Line2D(x_coords, y_coords, color = 'black', lw=0.7)
                ax.add_line(line);
            
        else:
            #Hyperedges of order d (d=1: links, etc.)
            for he in list(H.edges_of_order(d).values()):
                # Filling the polygon
                coordinates = [[pos[n][0], pos[n][1]] for n in he]
                #Sorting the points counterclockwise (needed to have the correct filling)
                sorted_coordinates = ccw_sort(coordinates)
                obj = plt.Polygon(sorted_coordinates, edgecolor = 'black', facecolor=colors[d], alpha=0.4, lw=0.5)
                ax.add_patch(obj);
            
    # Drawing the nodes 
    for i in list(H.nodes):
        (x, y) = pos[i]
        circ = plt.Circle([ x, y ], radius = 0.02, lw=1, zorder=d_max+1, ec = 'black', fc = 'white')
        ax.add_patch(circ);
