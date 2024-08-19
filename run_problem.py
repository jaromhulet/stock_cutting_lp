from stock_cutting import StockCutting

test_cuts_dict = {5 : 2,
                  12 : 6,
                  4 : 9}

test_stock_length = 14
test_stock_cutting = StockCutting(test_cuts_dict, test_stock_length, nbr_hood_size = 2)

test_stock_cutting.solve_lp_problem(10)
