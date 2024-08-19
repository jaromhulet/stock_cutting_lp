import pulp

# Define the problem
lp_problem = pulp.LpProblem("stock_cutting", pulp.LpMinimize)

# Define decision variables
x1 = pulp.LpVariable('x1', lowBound=0)
x2 = pulp.LpVariable('x2', lowBound=0)
x3 = pulp.LpVariable('x3', lowBound=0)
x4 = pulp.LpVariable('x4', lowBound=0)
x5 = pulp.LpVariable('x5', lowBound=0)

# Objective function - minimize stock purchases
lp_problem += (x1 + x2 + x3 + x4 + x5)

# Constraints
lp_problem += x4 >= 2, "6 foot cuts"
lp_problem += x3 + x5 >= 1, "5 foot cuts"
lp_problem += x2 + x5>= 1, "4 foot cuts"
lp_problem += 2*x1 + x2 + x3 + x4 >= 2, "3 foot cuts"

# Solve the problem
lp_problem.solve()

# Output the results
print("Status:", pulp.LpStatus[lp_problem.status])
print("Optimal number of stock purchases:", pulp.value(lp_problem.objective))
print("Optimal use of cut patterns:")
print("x1 =", pulp.value(x1))
print("x2 =", pulp.value(x2))
print("x3 =", pulp.value(x3))
print("x4 =", pulp.value(x4))
print("x5 =", pulp.value(x5))
