class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"+{amount}. Баланс: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Не хватает средств!")
        else:
            self.balance -= amount  
            print(f"-{amount}. Баланс: {self.balance}")

name=input()
balance=int(input())
acc = Account(name, balance)
dep=int(input("Пополнить: "))
acc.deposit(dep)
wit=int(input("Вывести: ")) 
acc.withdraw(wit)