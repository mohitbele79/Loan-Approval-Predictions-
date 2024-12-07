import pandas as pd 


class   READ():
    def readcsv(self,file):
        data=pd.read_excel(file)
        
        return(data)
    
