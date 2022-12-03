from GeneratorPole import GeneratorPole
from SolverSudoku import Solver
import random
import time

from Timer import timer


class GeneratorSudoku(Solver):
    def __init__(self, lst: list, quality=21):
        super().__init__(lst)
        self.lst_copy = self.lst.copy()
        self.quality = quality

        self.lst.variant_gen = None
        self.buffer_gen = []

    def solver_for_gen(self):
        m3 = False
        res_1 = False

        while True:
            try:
                while not self.lst.check():
                    m = self.method()

                    if not m:
                        self.method_3()
                        m3 = True

                if self.lst not in self.lst_solvers:
                    self.lst_solvers.append(self.lst)

                if len(self.lst_solvers) == 1:
                    res_1 = True
                elif len(self.lst_solvers) > 1:
                    res_1 = False
                    self.lst_solvers = []
                    self.buffer = []
                    break

                self.lst = self.buffer.pop()

            except IndexError:
                break

        return m3, res_1

    @timer
    def create_sudoku(self):
        start = time.time()

        delay = 1
        count = 0
        while (self.lst.size**2 - self.quality) != count:
            coord = [(y, x) for y, row in enumerate(self.lst) for x, cell in enumerate(row) if cell != 0]
            while True:
                if coord:
                    y, x = random.choice(coord)
                else:
                    count = 0
                    self.lst = self.lst_copy.copy()
                    start = time.time()
                    break

                lst_copy = self.lst.copy()
                self.lst[y][x] = 0
                lst_zero = self.lst.copy()
                m3, res1 = self.solver_for_gen()

                if res1:
                    count += 1
                    self.lst = lst_zero.copy()
                    break
                else:
                    coord.remove((y, x))
                    self.lst = lst_copy.copy()

                end = time.time()

                if end - start > delay:
                    count = 0
                    self.lst = self.lst_copy.copy()
                    start = time.time()
                    break

        return self.lst.lst


if __name__ == '__main__':
    # Генерация поля
    pole = GeneratorPole().run().lst

    # Генерация головоломки
    gen = GeneratorSudoku(pole, quality=25)
    res = gen.create_sudoku()





