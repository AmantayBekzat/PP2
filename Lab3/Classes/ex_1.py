class String:
    def __init__(self):
        self.text=""
    
    def getString(self):
        self.text=input()

    def printString(self):
        print(self.text.upper())

st=String()
st.getString()
st.printString()