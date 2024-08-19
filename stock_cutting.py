import pandas as pandas
from collections import Counter
import math
from pulp import LpMinimize, LpProblem, LpVariable, lpSum
from hill_climb import CutsHillClimb

class StockCutting(CutsHillClimb):

    def __init__(self,
                 cuts_dict, 
                 stock_length,
                 nbr_hood_size):
        
        super().__init__(cuts_dict,
                         stock_length,
                         nbr_hood_size)

        self.cuts_dict = cuts_dict
        self.stock_length = stock_length
        self.nbr_hood_size = nbr_hood_size



        return
    
    def create_list_of_patterns(self, num_patterns, max_iter = 150):

        '''
            Runs hill climb multiple time to create a list
            of patterns to serve as options for solving the stock
            cutting problem.

            input:
                num_patterns (int) : number of patterns to create

            Output:
                pattern_list (list) : list of patterns to include in 
                                      stock cutting problem
        '''

        print('creating cut patterns')
        patterns = set()

        iter_count = 0

        while len(patterns) < num_patterns:
            
            temp_pattern = self.hill_climb(self.nbr_hood_size)

            # sort and convert to tuple
            temp_pattern = sorted(temp_pattern)
            patterns.add(tuple(temp_pattern))

            iter_count += 1

            if iter_count > max_iter:
                print('Max iterations reached')
                print(f'{len(patterns)} patterns created')
                break

        print('Done creating cut patterns')

        return patterns
    
    
    
    def solve_lp_problem(self, num_patterns, max_iters = 150):

        patterns = self.create_list_of_patterns(num_patterns, max_iters)

        problem = LpProblem(name = 'Stock Cutting', sense = LpMinimize)

        # get number of patterns
        num_patterns = len(patterns)

        # create decision variables
        decision_vars = [LpVariable(f"pattern_{i}", lowBound=0, cat="Continuous") for i in range(num_patterns)]

        # get the number of specific cuts for each pattern
        cut_mapping = {}
        for i, pattern in enumerate(patterns):
            temp_counts = dict(Counter(pattern))
            cut_mapping[i] = temp_counts

        # add 0 to cut lengths that patterns don't have
        formatted_cut_mapping = {}
        for key in self.cuts_dict.keys():
            for key2, single_cut_map in cut_mapping.items():
                if key not in single_cut_map.keys():
                    single_cut_map[key] = 0

                formatted_cut_mapping[key2] = single_cut_map

        print('patterns')
        print(patterns)
        
        print('formatted cut mapping')
        print(formatted_cut_mapping)

        # add constraints
        # go through each pattern
        for key, value in self.cuts_dict.items():
            # loop through needed cuts in cuts_dict - 'value' is needed number of cuts, key is the index
            problem += lpSum((decision_vars[i] * formatted_cut_mapping[i][key]) for i in range(num_patterns)) >= value


        # costraints
        problem.solve()

        print(f"Status: {'Optimal Solution Found' if problem.status == 1 else 'Optimal Solution Not Found'}")
        print()

        total_stock_pieces = 0
        first_iter = True

        patterns_list = list(patterns)
        patterns_list.insert(0, '_')


        for variable, pattern_cuts in zip(problem.variables(), patterns_list):

            if first_iter:
                first_iter = False
            else:
                total_stock_pieces += variable.varValue
                if variable.varValue > 0:
                    print(f"{variable.name} uses = {variable.varValue}")
                    print(f"{variable.name} cuts = {pattern_cuts}")
                    print()

        print(f'Purchase {math.ceil(total_stock_pieces)} stock pieces')

        # if problem.status == 1:  # 1 indicates that an optimal solution was found
        #     print(f"Objective value: {problem.objective.value()}")
        # else:
        #     print(f"Problem not solved optimally, status: {problem.status}")

        return

