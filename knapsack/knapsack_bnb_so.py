from ortools.algorithms import pywrapknapsack_solver

num_products = 10
max_volume = 47250
values = []
weights_volumetric = []
weights_newton = []
productids = []

with open("short_millionth_customer_products_processed.csv") as f:
    for line in f:
        product_id, price, volume, weight = map(int, line.split(","))
        values.append(price)
        weights_volumetric.append(volume)
        weights_newton.append(weight)
        productids.append(product_id)

values = values[:num_products]
weights_volumetric = weights_volumetric[:num_products]
weights_newton = weights_newton[:num_products]
productids = productids[:num_products]

data_sorted = sorted(zip(range(len(weights_volumetric)), weights_volumetric, values),
                     key=lambda x: x[2]/x[1], reverse=True)

class State(object):
    def __init__(self, level, profit, weight, taken):
        # taken = list marking if an item is taken or not. ex. [1, 0, 0]
        # available = list marking all paths available, i.e. not explored yet
        self.level = level
        self.profit = profit
        self.weight = weight
        self.taken = taken
        self.ub = State.upperbound(self.taken[:self.level] + [1] * (len(data_sorted) - level))

    @staticmethod
    def upperbound(available):  # fractional knaksack's upperbound
        upperbound = 0
        # accumulated weight used to stop the upperbound summation
        remaining = max_volume
        for avail, (_, weight, value) in zip(available, data_sorted):
            weight_taken_not_taken =  weight * avail
            if weight_taken_not_taken <= remaining:
                remaining -= weight_taken_not_taken
                upperbound += value * avail
            else:
                upperbound += value * remaining / weight_taken_not_taken
                break
        return upperbound

    def develop(self):
        level = self.level + 1
        _, weight, profit = data_sorted[self.level]
        left_weight = self.weight + weight
        if left_weight <= max_volume:  # if not overweighted, give left child
            left_benefit = self.profit + profit
            left_taken = self.taken[:self.level] + [1] + self.taken[level:]
            left_child = State(level, left_benefit, left_weight, left_taken)
        else:
            left_child = None
        # anyway, give right child
        right_child = State(level, self.profit, self.weight, self.taken)
        return ([] if left_child is None else [left_child]) + [right_child]


Root = State(0, 0, 0, [0] * len(data_sorted))  # start with nothing
waiting_States = []  # list of States waiting to be explored
current_state = Root
while current_state.level < len(data_sorted):
    waiting_States.extend(current_state.develop())
    # sort the waiting list based on their upperbound
    waiting_States.sort(key=lambda x: x.ub)
    # explore the one with largest upperbound
    current_state = waiting_States.pop()
collected_items = [item for tok, (item, _, _)
                   in zip(current_state.taken, data_sorted) if tok == 1]

collected_items_productids = [productids[_] for _ in collected_items]
collected_items_productids.sort()

print("Total Value:%s, volumetric weight:%s, and NEWTON weight of products: %s"% (current_state.profit, current_state.weight, sum([weights_newton[_] for _ in collected_items])))
print("Product IDs of collected items: ", collected_items_productids)
print("Sum of product ids: %s" % sum(collected_items_productids), "\n\n")


def googleSolver():
    # Confirming solution using google OR tools.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
            KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        'test')


    weights_gor = [weights_volumetric]
    capacities = [max_volume, 32078]

    solver.Init(values, weights_gor, capacities)
    computed_value = solver.Solve()

    packed_items = [x for x in range(0, len(weights_gor[0]))
                    if solver.BestSolutionContains(x)]
    packed_weights = [weights_gor[0][i] for i in packed_items]
    total_weight = sum(packed_weights)

    print("Packed items product ids: %s" % [productids[_] for _ in packed_items])
    print("Total value: %s" % computed_value)
    print("Total weight (volumetric): %s" % total_weight)
    print("Total weight (newtons): %s" % sum([weights_newton[_] for _ in packed_items]))
    print("Total sum of product ids: %s" % sum([productids[_] for _ in packed_items]))


googleSolver()