import sys
import re
import numbers

def strsign(lhs):
    if lhs >= 0:
        return '+'
    else:
        return '-'

class Polynomial:
    def __init__(self, other=None, coeffs=()):
        if other != None:
            self.coeffs = other.coeffs.copy()
        else:
            self.coeffs = []
            if coeffs != ():
                for i in coeffs:
                    self.coeffs.append(i)
            

    def __str__(self):
        if len(self.coeffs) == 0:
            return '0'
        res = ''
        for i in range(len(self.coeffs)):
            if self.coeffs[i] != 0:
                res = f' {strsign(self.coeffs[i])} {abs(self.coeffs[i]):g}x^{i}' + res
        return res[:len(res)-3]

    def __add__(self, other):
        res = Polynomial()
        for i in range(max(len(self.coeffs), len(other.coeffs))):
            res.coeffs.append(0)
            res.coeffs[i] = (self.coeffs[i] if len(self.coeffs) > i else 0) + (other.coeffs[i] if len(other.coeffs) > i else 0)
        for i in range(len(self.coeffs) - 1, 0, -1):
            if self.coeffs[i] == 0:
                self.coeffs.pop()
            else:
                break
        return res

    def __mul__(self, other):
        res = Polynomial()
        for i in range(len(self.coeffs) + len(other.coeffs) - 1):
            res.coeffs.append(0)
        for i in range(len(self.coeffs)):
            for j in range(len(other.coeffs)):
                res.coeffs[i + j] += self.coeffs[i] * other.coeffs[j]
        for i in range(len(self.coeffs) - 1, 0, -1):
            if self.coeffs[i] == 0:
                self.coeffs.pop()
            else:
                break
        return res
    
def get_coords():
    str_format = re.compile(r"^([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?) ([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)$")
    coords = []
    temp_input = ''
    try:
        temp_input = input()
    except EOFError:
        return coords
    while True:
        if (match := re.match(str_format, temp_input)) is not None:
            input_arr = temp_input.split(' ')
            coords.append((float(input_arr[0]), float(input_arr[1])))
        else:
            print('bad input, skip')

        try:
            temp_input = input()
        except EOFError:
            break
    return coords

def get_polynomial(coords):
    res = Polynomial()
    for i in range(len(coords)):
        temp = Polynomial(coeffs=(1, ))
        for j in range(len(coords)):
            if i != j:
                if coords[i][0] == coords[j][0]:
                    raise ArithmeticError('that cannot be polynomial')
                temp *= Polynomial(coeffs=(-coords[j][0]/(coords[i][0] - coords[j][0]), 1/(coords[i][0] - coords[j][0])))
        res += Polynomial(coeffs=(coords[i][1], )) * temp
    return res

def main():
    res = ''
    coords = get_coords()
    try:
        res = get_polynomial(coords)
    except ArithmeticError:
        print('that cannot be polynomial')
        exit()
    print(res)

    return 0

if __name__ == '__main__':
    main()