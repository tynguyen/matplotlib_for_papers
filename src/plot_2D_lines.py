'''
    * plot_lines.py
    * Author: Ty Nguyen [tynguyen@seas.upenn.edu]

    * Plot line figure. Each line represents the data given from a single file specified by an extension (default: txt),
    and number of columns (cols_per_file)
'''
import os, glob
from pylab import *
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
    f_list = glob.glob(root + f'/*{extension}')
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
    parser.add_argument("--config_file",help="Name of the configuration file that defines the figure",default="configs/icra2020_fewshot_performance.yml", type=str)

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
    colors = gen_colors(num_lines)
    line_styles = gen_line_styles(num_lines)
    if not opt['saving_dir']:
        opt['saving_dir'] = opt['root_dir']
    if not os.path.exists(opt['saving_dir']):
        os.makedirs(opt['saving_dir'])
    fig_file  = os.path.join(opt['saving_dir'], opt['fig_name'])
    
    # Start drawing
    axes(frameon=0)
    grid()
    
    # Get x values
    if 'x_values' not in opt or len(opt['x_values'])==0:
        assert len(opt['xlim']) > 0, "Either x_values or xlim must be given in the config file"

        x_values = range(opt['xlim'])
    else:
        x_values = opt['x_values']
    
    for i in range(num_lines):
        #plot(x_values, data[i], linewidth=2, color=colors[i], linestyle=line_styles[i])
        plot(x_values, data[i], linewidth=2, color='r', linestyle='solid')
    
    if opt['xlim']:
        xlim(opt['xlim'][0], opt['xlim'][1])
    if opt['ylim']:
        ylim(opt['ylim'][0], opt['ylim'][1])
    
    pdb.set_trace()
    if opt['xticks'] and opt['xlabels']:
        xticks(ticks=opt['xticks'],labels=opt['xlabels'])
    elif opt['xticks']:
        xticks(opt['xticks'])

    legend = legend(opt['legends'], loc=4);
    frame = legend.get_frame()
    frame.set_facecolor('0.9')
    frame.set_edgecolor('0.9')
    plt.show()
    savefig(fig_file)
    print(f'Successfuly saved figure {fig_file}!')
