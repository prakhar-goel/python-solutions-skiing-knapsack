# returns maxLength and maxDrop at grid[(i,j)]
def findSteepestPath(grid, rows, cols, i, j, history):
    if not (0 <= i < rows and 0 <= j < cols):
        return

    if (i, j) in history:
        return history[(i, j)]

    cell = grid[i][j]
    east = west = north = south = (1, 0, "")

    if i + 1 < rows and grid[i + 1][j] < cell:
        length, drop, path = findSteepestPath(grid, rows, cols, i + 1, j, history)
        south = (1 + length, cell - grid[i + 1][j] + drop, "%s-%s" % (grid[i + 1][j], path))

    if j - 1 > 0 and grid[i][j - 1] < cell:
        length, drop, path = findSteepestPath(grid, rows, cols, i, j - 1, history)
        west = (1 + length, cell - grid[i][j - 1] + drop, "%s-%s" % (grid[i][j - 1], path))

    if i - 1 > 0 and grid[i - 1][j] < cell:
        length, drop, path = findSteepestPath(grid, rows, cols, i - 1, j, history)
        north = (1 + length, cell - grid[i - 1][j] + drop, "%s-%s" % (grid[i - 1][j], path))

    if j + 1 < cols and grid[i][j + 1] < cell:
        length, drop, path = findSteepestPath(grid, rows, cols, i, j + 1, history)
        east = (1 + length, cell - grid[i][j + 1] + drop, "%s-%s" % (grid[i][j + 1], path))

    maxLength = max(south[0], west[0], north[0], east[0])
    maxDrop = max([_[1] for _ in [south, west, north, east] if _[0] == maxLength])
    maxPath = ""
    for v in [south, west, north, east]:
        if v[0] == maxLength and v[1] == maxDrop:
            maxPath = v[2]
    history[(i, j)] = (maxLength, maxDrop, maxPath)
    return maxLength, maxDrop, maxPath


gridStr = """
4 8 7 3 
2 5 9 3 
6 3 2 5 
4 4 1 6"""


def main():
    rows, cols = map(int, input().split(" "))
    grid = [[int(__) for __ in input().split(" ") if __ != ""] for _ in range(rows)]

    history = {}
    maxLength = 0
    maxDrop = 0
    maxPath = ""
    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            l, d, p = findSteepestPath(grid, rows, cols, i, j, history)
            if l > maxLength:
                maxLength = l
                maxDrop = d
                maxPath = "%s-%s" % (grid[i][j], p)
            elif l == maxLength and d > maxDrop:
                maxDrop = d
                maxPath = "%s-%s" % (grid[i][j], p)

    print("maxLength:%s, maxDrop:%s, maxPath:%s" % (maxLength, maxDrop, maxPath))


main()
