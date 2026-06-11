from stock_cutting import StockCutting



# Define cuts needed: {length: quantity}
#this is for 2 x 4
test_cuts_dict = {1 : 5,
                  2 : 1,
                  3 : 21,
                  4 : 4,
                  5 : 2,
                  6 : 2,
                  7 : 2, 
                  8 : 16, #remove those that we have 8' already, 33 - 17
                  9 : 4,
                  10 : 3,}

test_stock_length = 12


test_stock_cutting = StockCutting(test_cuts_dict, test_stock_length, nbr_hood_size = 2)

test_stock_cutting.solve_lp_problem(1000)
