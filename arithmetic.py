import math

class ArithmeticErrors(Exception):
    pass

class RangeError(ArithmeticErrors):
    pass

class CantBeFloatError(ArithmeticErrors):
    pass

class Arithmetic_Diference:
    def __init__(self, a: float, d: float) -> None:
        self.a = a; self.d = d
    
    def get_amount_by_Nrangen(self, Nrange: tuple) -> float:
        """
        return the amount of range of N
        """

        try:
            float(Nrange[0])
            float(Nrange[1])
        except Exception:
            raise RangeError("invailed range")

        self.amount = 0
        for N in range(Nrange[0], Nrange[1] +1):
            self._plus = self.a + self.d*(N-1)
            self.amount += self._plus
        return self.amount
    
    def get_amount_by_ranges(self, ranges: tuple) -> float:
        """
        return the amount of provided ranges
        """

        try:
            float(ranges[0])
            float(ranges[1])
        except Exception:
            raise RangeError("invailed range")

        self.amount = 0
        self.firstN = 1
        while True:
            if self.a + self.d*(self.firstN -1) > ranges[0]:
                break
            self.firstN += 1

        self.secondN = self.firstN
        while True:
            if self.a + self.d*(self.secondN -1) > ranges[1]:
                self.secondN -= 1
                break
            self.secondN += 1

        for N in range(self.firstN, self.secondN +1):
            self._plus = self.a + self.d*(N-1)
            self.amount += self._plus
        return self.amount
    
    def N(self, n) -> float:
        """
        return the amount to n
        """
        
        try:
            float(n)
        except Exception:
            raise CantBeFloatError(f"provided 'n' can't be float")
        
        first = self.a
        second = self.a + (n-1)*self.d
        self.amount = 1/2*(n*(first + second))

        return self.amount


An = Arithmetic_Diference(14, 6)
result = An.get_amount_by_Nrangen((1, 15))
print(result)

Bn = Arithmetic_Diference(2, 6)
result = Bn.get_amount_by_ranges((10, 99))
print(result)
print(Bn.N(2))




