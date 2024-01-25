import argparse 
import sys 
import os
import multiprocessing as mp
from multiprocessing import Pool
import time

""""""
# Parse input arguments 
parser = argparse.ArgumentParser(description="Required pyEPrun Arguments")

parser.add_argument('--output_dir', '-o', help='relative path to output directory to save all EP simulation objects', type=str, required=True)
parser.add_argument('--input_weather', '-w', help='relative path to input EPW weather file', type=str, required=True)
parser.add_argument('--input_idf', '-i', help='relative path to input IDF building description file', type=str, required=True)
parser.add_argument('--ep_path', '-e', help='absolute path to EP install, defaults to /usr/local/EnergyPlus-xx-x-x/', type=str, default='/usr/local/EnergyPlus-23-2-0/')

args = parser.parse_args()

# Setup environment
ep_install_path = args.ep_path
ep_output_dir = args.output_dir
ep_epw_dir = args.input_weather
ep_idf_dir = args.input_idf

if not ep_epw_dir.endswith('.epw'):
    print(ep_epw_dir)
    print(~ep_epw_dir.endswith('.epw'))
    print("ERROR: EPW file must end in .epw")
    sys.exit(1)

if not ep_idf_dir.endswith('.idf'):
    print("ERROR: IDF file must end in .idf")
    sys.exit(1)

sys.path.append(ep_install_path)
cwd = os.getcwd()

# Setup API hook
from pyenergyplus.api import EnergyPlusAPI

api = EnergyPlusAPI()
print("EnergyPlus Version: " + str(api.functional.ep_version()))

demo_in_list = [('first_output', 'epws/1992_historical_detroit_A.epw', 'idfs/in_DT92A_230.idf'), ('second_output', 'epws/1992_historical_detroit_H.epw', 'idfs/in_DT92A_230.idf'), ('third_output', 'epws/newprecip_2041_rcp85hotter_detroit_hc.epw', 'idfs/in_DT92A_230.idf')]
# demo_in_list = [('EPcomparison_pyparallel', 'EPcomparison_pyparallel/1992_historical_detroit_H.epw', 'EPcomparison_pyparallel/in_DT92H.idf'), ('second_output', 'epws/1992_historical_detroit_H.epw', 'idfs/in_DT92A_230.idf'), ('third_output', 'epws/newprecip_2041_rcp85hotter_detroit_hc.epw', 'idfs/in_DT92A_230.idf')]

def execute_sim(ep_output_in, ep_epw_in, ep_idf_in):
    print("starting simulation to be output at " + ep_output_in)
    # Execute simulation
    state = api.state_manager.new_state()
    progressValue = 0

    def progress_handler(progress: int) -> None:
        global progressValue
        progressValue = progress
        if 49 < progress < 51:
            print("------Halfway through simulation------")
            sys.stdout.flush()

    api.runtime.callback_progress(state, progress_handler)

    ep_output_dir = cwd + '/' + ep_output_in
    ep_epw_dir = cwd + '/' +  ep_epw_in
    ep_idf_dir = cwd + '/' +  ep_idf_in

    v = api.runtime.run_energyplus(state, ['-d', ep_output_dir, '-w', ep_epw_dir, ep_idf_dir])
    if v != 0:
        print("EnergyPlus Simulation Failed")
        sys.exit(1)
    # assert(progressValue == 100)

if __name__ == '__main__':
    # num_cores = int(os.getenv('SLURM_CPUS_PER_TASK'))
    num_cores = mp.cpu_count()
    start_time = time.time()
    with Pool(num_cores) as p:
        p.starmap(execute_sim, demo_in_list)

    print("Execution time: %s seconds" % (time.time() - start_time))