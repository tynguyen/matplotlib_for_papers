'''
    * plot_2D_lines.py
    * Author: Ty Nguyen [tynguyen@seas.upenn.edu]

    * Plot line figure. Each line represents the data given from a single file specified by an extension (default: txt),
    and number of columns (cols_per_file)
'''
import os, glob
from pylab import *
import pylab
import pdb 
import argparse 
from utils.plot_colors import gen_colors 
from utils.plot_line_styles import gen_line_styles
from utils.plot_params import single_plot_params 
import random
import yaml

# Use single plot parameters
rcParams.update(single_plot_params)


def load(root, extension='.txt', cols_per_file=5, skip_rows=False):
    '''
    Inputs:
        cols_per_file (int): number of cols per file
        skip_rows (boolean): whether skip the first 'skip_rows' rows of each file
        extension (str): extension of each file
    '''
    f_list = sorted(glob.glob(root + f'/*{extension}'))
    num_lines = sum(1 for line in open(f_list[0])) - skip_rows
    i = 0;
    data = np.zeros((len(f_list), num_lines, cols_per_file)) 
    for f in f_list:
        data[i, ...] = np.loadtxt(f, skiprows=skip_rows) #[:,1]
        i += 1
    return data # Num files x Num rows x Num cols 

def str2Bool(s):
    return False if 'f' in s.lower() else True
def parse_configs():
    parser = argparse.ArgumentParser("Plot lines")
    parser.add_argument("--config_file",help="Name of the configuration file that defines the figure",default="configs/icra2020_fewshot_performance_real_MAV.yml", type=str)

    opt = parser.parse_args()
    config_file = opt.config_file 
    with open(config_file, 'r') as f:
        configs = yaml.load(f)
    return configs 

def proceed_data(data, func_name):
    '''
    This function executes data processes such as finding mean, median ... to  obtain a data of shape: n_files x n_cols 
    Inputs:
        data (np.ndarray): n_files x n_rows x n_cols data 
    Outputs:
        output (np.ndarray): n_files x n_cols
    '''
    func_map = {'mean': np.mean,
                'std': np.std}
    
    data = func_map[func_name](data, axis=1)
    return data

def plot_line(ax, show_boundary_lines=True):
    '''
    If show_boundary_lines == False, only show x and y axes, not top, right lines
    '''
    # now all plot function should be applied to ax
    ax.spines['top'].set_visible(show_boundary_lines)
    ax.spines['right'].set_visible(show_boundary_lines)
    ax.spines['left'].set_visible(show_boundary_lines)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    # Draw ticks 
    ax.tick_params(axis='x', direction='out')
    ax.tick_params(axis='y', direction='out')
    #ax.tick_params(axis='y', length=0)

    # offset the spines
    if not show_boundary_lines:
        for spine in ax.spines.values():
            spine.set_position(('outward', 5))

    ax.grid(axis='y', color="0.9", linestyle='dashed', linewidth=1)
    ax.grid(axis='x', color="0.9", linestyle='dashed', linewidth=1)

    # put the grid behind
    ax.set_axisbelow(True)

    # Get x values
    if 'x_values' not in opt or len(opt['x_values'])==0:
        assert len(opt['xlim']) > 0, "Either x_values or xlim must be given in the config file"

        x_values = range(opt['xlim'])
    else:
        x_values = opt['x_values']
    
    for i in range(num_lines):
        ax.plot(x_values, data[i], linewidth=2, color=colors[i+2], linestyle=line_styles[i][0])
    
    if opt['xlim']:
        xlim(opt['xlim'][0], opt['xlim'][1])
    if opt['ylim']:
        ylim(opt['ylim'][0], opt['ylim'][1])
    
    if opt['xticks']:
        ax.xaxis.set_ticks(opt['xticks'])
    if opt['xlabels']:
        ax.xaxis.set_ticklabels(opt['xlabels'])
    if opt['yticks']:
        ax.yaxis.set_ticks(opt['yticks'])
    if opt['ylabels']:
        ax.yaxis.set_ticklabels(opt['ylabels'])
    if opt['xtitle']:
        ax.set_xlabel(opt['xtitle'])
    if opt['ytitle']:
        ax.set_ylabel(opt['ytitle'])


    
    legend = ax.legend(opt['legends'], loc=4);
    frame = legend.get_frame()
    frame.set_facecolor('0.9')
    frame.set_edgecolor('0.9')
    
    # Display xticks evenly regardless of their values:
    #ax.xaxis.set_minor_locator(plt.MultipleLocator(len(x_values))) # locates ticks at a multiple of the number you provide, as here 0.25 (keeps ticks evenly spaced)

def plot_points(ax, point_values, point_labels, point_markers, point_colors):
    '''
    Plot points
    ax (mpl.axes): subplot to display 
    point_values (list(list)): points i.e. [[5,0.743], [0,0.601]] 
    point_labels (list(str)): labels of points i.e. ['Baseline', 'Zero-shot'] 
    point_markers(list(str)): markers for each point i.e. ['s', 'o'] 
    point_colors(list(str)): colors for each point i.e. ['r', 'b'] 
    '''
    for i, (point, label, marker, color) in enumerate(zip(point_values, point_labels, point_markers, point_colors)):
        #ax.annotate(f'{label}', xy=point, xytext=(point[0]+10, point[1]-10), textcoords=label)
        ax.annotate(f'{label}', xy=point, xytext=(-15,5), textcoords='offset points')
        #ax.plot(point[0], point[1], marker, alpha=0.5)#='s', color='#cfbbb0', alpha=0.5)
        ax.plot(point[0], point[1], marker, alpha=0.5)#='s', color='#cfbbb0', alpha=0.5)
        

if __name__=="__main__":
    opt  = parse_configs() 
    data = load(root= opt['root_dir'],
                extension = opt['extension'],
                cols_per_file=opt['cols_per_file'],
                skip_rows=opt['skip_rows']
                )
    # Proceed the data 
    print(data.shape)
    print(data)
    data = proceed_data(data, opt['reduce_func'])
    print(data.shape)
    print(data)

    # Prepare to draw and save figs
    num_lines = data.shape[0]
    colors = gen_colors(num_lines+2)
    line_styles = gen_line_styles(num_lines)
    if not opt['saving_dir']:
        opt['saving_dir'] = opt['root_dir']
    if not os.path.exists(opt['saving_dir']):
        os.makedirs(opt['saving_dir'])
    fig_file  = os.path.join(opt['saving_dir'], opt['fig_name'])
   
    # Start drawing
    fig = figure()
    ax1 = fig.add_subplot(111)
    plot_line(ax1)

    if len(opt['point_values']) > 0:
        plot_points(ax1, opt['point_values'], opt['point_labels'], opt['point_markers'], opt['point_colors'])

    plt.show()
    fig.savefig(fig_file)
    print(f'Successfuly saved figure {fig_file}!')
