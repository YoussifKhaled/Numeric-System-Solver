import GaussJordan as gj
def main():

    size = int(input("Size:"))
    matrix = []
    print("Coeff Matrix|Solution:")
    for i in range(size):
        row = [x for x in input().split()]
        matrix.append(row)

    try:
        values, steps = gj.gauss_jordan_elimination(matrix,2)
    except ValueError as e:
        print(e)
        return
    
    print("Solution:")
    for i in range(size):
        print("x"+str(i+1)+" = "+str(values[i]))
    print("Steps:")
    for step in steps:
        print(step[1])
        for row in step[0]:
            print(row)
        print()

if __name__ == "__main__":
    main()