# file A
class TestA:

    def main(self):
        for n in range(100):

            print(n)


# file B
class TestB:
    def get_n(self, fun):
        return fun

    def main(self):
        testa = TestA()
        testa.main()
        print()
