from ortools.algorithms import pywrapknapsack_solver

num_products = 20000
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


def knapsackDynamicProgramming(itemsPrice, itemsWeight, itemsWeight2, ksize):
    n = len(itemsPrice)
    matrix = [[[0, 0] for __ in range((ksize + 1))] for _ in range(n + 1)]

    def best_price_matrix():
        for i in range(1, n + 1):
            for j in range(ksize + 1):

                # itemsWeight's index start from 0 not 1, hence doing -1
                if (j < itemsWeight[i - 1]):
                    matrix[i][j][0] = matrix[i - 1][j][0]
                    matrix[i][j][1] = matrix[i - 1][j][1]
                else:
                    not_taking_this_item = matrix[i - 1][j][0]
                    taking_this_item = matrix[i - 1][j - itemsWeight[i - 1]][0] + itemsPrice[i - 1]
                    if (not_taking_this_item > taking_this_item):
                        matrix[i][j][0] = not_taking_this_item
                        matrix[i][j][1] = matrix[i - 1][j][1]
                    elif (not_taking_this_item < taking_this_item):
                        matrix[i][j][0] = taking_this_item
                        matrix[i][j][1] = matrix[i - 1][j - itemsWeight[i - 1]][1] + itemsWeight2[i - 1]
                    else:
                        # both prices are same. Choose the one with lower weight2
                        if (matrix[i - 1][j][1] < matrix[i - 1][j - itemsWeight[i - 1]][1] + itemsWeight2[i - 1]):
                            matrix[i][j][0] = matrix[i - 1][j][0]
                            matrix[i][j][1] = matrix[i - 1][j][1]
                        else:
                            matrix[i][j][0] = matrix[i - 1][j - itemsWeight[i-1]][0] + itemsPrice[i - 1]
                            matrix[i][j][1] = matrix[i - 1][j - itemsWeight[i-1]][1] + itemsWeight2[i - 1]

    best_price_matrix()  # calculate best_price matrix
    print("Value and NEWTON weight of products: ", matrix[n][ksize])


    # Starting from the reverse. Compare the price values. if they differ, that means we have taken this item
    collected_items = []
    remainingSize = ksize
    for i in range(n, 1, -1):
        if(matrix[i][remainingSize][0] != matrix[i-1][remainingSize][0]):
            collected_items.append(i-1)
            remainingSize -= itemsWeight[i-1]
        elif(matrix[i][remainingSize][1] != matrix[i-1][remainingSize][1]):
            collected_items.append(i - 1)
            remainingSize -= itemsWeight[i - 1]

    collected_items.reverse()
    collected_items_productids = [productids[_] for _ in collected_items]
    print("Product IDs of collected items: ", collected_items_productids)
    print("Sum of product ids: %s" % sum(collected_items_productids), "\n\n")

def googleSolver():
    # Confirming solution using google OR tools.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
            KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,
        'test')


    weights_gor = [weights_volumetric, weights_newton]
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


knapsackDynamicProgramming(values, weights_volumetric, weights_newton, max_volume)
googleSolver()
