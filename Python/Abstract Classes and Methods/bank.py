# Import ABC and abstractmethod from the module abc (which stands for abstract base classes)
from abc import ABC, abstractmethod

# Class Bank
class Bank(ABC):

    def basicinfo(self):
        print("This is generic bank")
        s="Generic bank: 0"
        return s

        @abstractmethod
        def withdraw(self):
            pass

# Class Swiss
class Swiss(Bank):

    ### YOUR CODE HERE
    def __init__(self):
        self.bal = 1000
    def basicinfo(self):
        print("This is the Swiss Bank")
        s="Swiss Bank: " + str(self.bal)
        return s
    def withdraw(self, amount):
        if(amount>self.bal):
            print("Insufficient funds")
        else:
            self.bal -=amount
            print("Withdraw amount: " + str(amount))
        print("New balance: " + str(self.bal))
        return self.bal


# Driver Code
def main():
    assert issubclass(Bank, ABC)
    s = Swiss()
    print(s.basicinfo())
    s.withdraw(30)
    s.withdraw(1000)

if __name__ == "__main__":
    main()