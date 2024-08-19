from copy import copy

import pandas as pd
import random

class CutsHillClimb():

    def __init__(self,
                 cuts_dict, 
                 stock_length,
                 nbr_hood_size):

        self.cuts_dict = cuts_dict
        self.stock_length = stock_length
        self.nbr_hood_size = nbr_hood_size

        return
    

    def starting_solution(self) -> list:

        '''
            Creates a random starting cut pattern.

            output:
                start_pattern (list) : list of cut lengths to go on
                                       a single piece of stock
        '''
        unique_cuts = list(self.cuts_dict.keys())

        waste = self.stock_length
        start_pattern = []
            
        while waste >= min(unique_cuts):
            # randomly sample with replacement
            next_cut = random.choice(unique_cuts)

            # only add cut if it makes a feasible pattern
            temp_pattern = copy(start_pattern)
            temp_pattern.append(next_cut)
            if self.check_pattern(temp_pattern):
                start_pattern.append(next_cut)
                waste -= next_cut

        return start_pattern
    
    def check_pattern(self, pattern):

        '''
            checks if a given pattern is feasible.

            Input:
                pattern (list) : contains cuts for pattern
            
            Output:
                valid (bool) : true if pattern is valid
                               otherwise false
        '''

        if sum(pattern) > self.stock_length:
            valid = False
        else:
            valid = True
        
        return valid


    def create_nbr_hood(self, pattern, size, prob_add_remove_cut = 0.1):

        '''
            Creates a neighborhood of patterns
            by swapping one cut for another.

            Inputs:
                pattern (list) : starting cut pattern
                size (int)     : size of neighborhood to be created

            Outputs: 
                nbr_hood (list) : list of patterns that are one
                                  cut different from the original
                                  pattern.
        '''

        nbr_hood = set()

        while len(nbr_hood) < size:

            # make a new copy to modify for every iteration
            pattern_cp = copy(pattern)

            # remove a cut
            cut_to_remove = random.choice(pattern)

            # add a cut
            cut_to_add = random.choice(list(self.cuts_dict.keys()))

            # only add if it is different than cut_to_remove
            if cut_to_remove != cut_to_add:
                pattern_cp.remove(cut_to_remove)
                pattern_cp.append(cut_to_add)            

            # randomly add or remove an extra cut
            rand_num = random.random()
            if rand_num <= prob_add_remove_cut:
                rand_add_remove = random.choice(['add extra', 'remove extra'])

                if rand_add_remove == 'remove extra':
                    extra_cut_to_remove = random.choice(pattern_cp)

                    pattern_cp.remove(extra_cut_to_remove)

                else:
                    extra_cut_to_add = random.choice(pattern)

                    pattern_cp.append(extra_cut_to_add)

            # add pattern if it is valid
            if self.check_pattern(pattern_cp):
                nbr_hood.add(tuple(pattern_cp))

        nbr_hood = list(nbr_hood)

        return nbr_hood
    
    def calc_waste(self, pattern):

        '''
            Given a pattern, calculates cutoff waste.

            Input:
                pattern (list) : list of cuts in a pattern

            Output:
                waste (float) : difference between stock length
                                and sum of cuts in pattern    
        '''
        waste = self.stock_length - sum(pattern)

        return waste
    

    def hill_climb(self, max_iter = 150) -> tuple:

        '''
            Runs a simple hill climbing algorithm to create
            an 'optimal' pattern. Algorithm intentionally
            is subject to returning local optimum because
            the output will be used in the stock cutting 
            problem - local optimum here could be useful
            in getting better stock cutting solutions.

            Inputs:
                max_iter (int, default = 150) : sets up a 
                                                maximum number
                                                of searches to 
                                                exit early after
            
            Output:
                best_nbr (tuple) : best cut pattern found in 
                                   the hill climb
        '''

        # create random starting solution
        start_sol = self.starting_solution()
        start_waste = self.calc_waste(start_sol)
        
        if start_waste == 0:
            best_nbr = tuple(start_sol)
            lowest_waste = start_waste
            done = True
        else:
            done = False
        
        iter_count = 0

        while not done:
            
            iter_count += 1

            if iter_count >= max_iter:
                return best_nbr

            best_nbr = start_sol
            lowest_waste = start_waste

            temp_nbr_hood = self.create_nbr_hood(best_nbr, self.nbr_hood_size)

            for curr_nbr in temp_nbr_hood:
                
                curr_nbr_waste = self.calc_waste(curr_nbr)

                if curr_nbr_waste < lowest_waste:
                    best_nbr = curr_nbr
                    lowest_waste = curr_nbr_waste

                if curr_nbr == best_nbr:
                    done = True
                else:
                    curr_nbr = best_nbr

        return best_nbr
