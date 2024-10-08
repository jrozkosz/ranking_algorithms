# author: Jakub Rozkosz

from CEC2022 import CECfunctions, FuncCallsLimitReachedException
import json
import numpy as np
import random
import sys
import importlib

class RunningAlgorithm:
    def __init__(self, alg_name) -> None:
        self.alg_name = alg_name
        self.call_count = 0
        with open("ranking_config.json", 'r') as f:
            params = json.load(f)
        self.g_optimum = params["g_optimum"]
        self.functions = params["functions"]
        self.max_call_count = params["max_call_count"]
        self.dimensions = params["dimensions"]
        self.rand_seed = params["rand_seed"]
        self.runs = params["runs"]
    
    def run_algorithm(self):
        data = {}

        CECfuncs = CECfunctions()
        for dim, max_fes in zip(enumerate(self.dimensions), self.max_call_count):
            dim_idx, dim = dim
            CECfuncs.set_max_fes(max_fes)
            for fun_idx, fun in enumerate(self.functions):
                real_value = CECfuncs.get_function_min(fun)
                CECfuncs.config_cec_functions(dim, fun)
                for r, rand_s in zip(range(self.runs), self.rand_seed):
                    try:
                        random.seed(rand_s)
                        np.random.seed(rand_s)
                        evolutionary_algorithm(CECfuncs.call_cec22_func, dim, rand_s)
                    except FuncCallsLimitReachedException as e:
                        calls_count = CECfuncs.get_calls_count()
                        best_value = CECfuncs.best_so_far[1]
                        print(best_value)
                        CECfuncs.reset_call_count()
                        CECfuncs.best_so_far = None
                        error = abs(best_value - real_value)
                        print("error: ", error)
                        print(e)
                        # saving the new algorithm's results to a file
                        if f"function_{fun}" not in data:
                            data[f"function_{fun}"] = {}
                        if f"dim_{dim}" not in data[f"function_{fun}"]:
                            data[f"function_{fun}"][f"dim_{dim}"] = {}
                        data[f"function_{fun}"][f"dim_{dim}"][f"trial_{r}"] = [error, calls_count]
                
                    self.save_progress_to_file(dim_idx, fun_idx, r, max_fes)

                with open(f'running_results_{alg_name}.json', 'w') as file:
                    json.dump(data, file, indent=4)
    
    def save_progress_to_file(self, dim, fun, run, max_fes):
        with open(f'progress_file_{alg_name}.txt', 'w') as f:
            all_runs = len(self.dimensions)*len(self.functions)*self.runs #*(self.max_call_count[0]+self.max_call_count[1])
            current_state = (dim*len(self.functions)*self.runs + fun*self.runs + (run+1)) #*max_fes
            progress = int((current_state/all_runs)*100)
            f.write(str(progress))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        alg_name = sys.argv[1]
        module_name = f"{alg_name}"
        # module_name = "algorithm"

        try:
            algorithm_module = importlib.import_module(module_name)
            evolutionary_algorithm = algorithm_module.evolutionary_algorithm
        except ImportError:
            print('Module does not exist.')
            exit(1)
        except AttributeError:
            print('Module does not contain the required function.')
            exit(1)
        
        RankingCalc = RunningAlgorithm(alg_name)
        RankingCalc.run_algorithm()
    else:
        print("No name provided.")
        exit(1)
