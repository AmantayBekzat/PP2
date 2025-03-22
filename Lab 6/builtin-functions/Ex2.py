def count_letters(letter):
    upper=0
    lower=0
    for i in letter:
        if i>="A" and i<="Z":
            upper+=1
        else:
            lower+=1
    print("Upper case:", upper)
    print("Lower case:", lower)
            
        
sent=str(input("enter sentence:"))
count_letters(sent)