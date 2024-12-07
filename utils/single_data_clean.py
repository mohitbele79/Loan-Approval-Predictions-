import numpy as np
import pandas as pd 
import pickle
import joblib

encoders = joblib.load("encoders.pkl")
scaler = joblib.load("scaler.pkl")



class CLEAN():

    def find_mode(self,file,i):
        print('Enter in  mode')
        fmode=file[i].mode()
        print('done in  mode')
        return(fmode)
    
    def data_type_con(self,file):
        print('Enter in  datatypeconvertion')
        file['Loan_Amount_Term']=file['Loan_Amount_Term'].astype('str')
        file['Credit_History']=file['Credit_History'].astype('str')
        print('done in  datatypeconvertion')
        return(file)
    
    def data_con(self,file):
        print('Enter in  3+ to3')
        file['Dependents'] = file['Dependents'].replace('3+', '3').astype('str')
        print('doen in  3+ to3')
        return(file)           

          
    
    def caping_num_cols(self,file,i):
        print('Enter in  capping_num_cols')
        #_,num_cols=self.cat_num_split(file)

        list=[]
        
        print(i)
        data=file[i]
        Q1=np.percentile(data,q=25)
        Q3=np.percentile(data,q=75)
            
        IQR=Q3-Q1

        lb=Q1-1.5*IQR
        ub=Q3+1.5*IQR
            
        con1=data<lb
        con2=data>ub
        con3=con1|con2
        #median=loan_df[i].median()
        list=np.where(con1,lb,data)
        print(f'lb_{i}_done')
        list=np.where(con2,ub,data)
        print(f'ub_{i}_done')
        file[i]=list
        print(f'data_processes_doen_for_{i}')
        print('doen in  capping_num_cols')
        return(file)
            
    def outlier_filling(self,file):
         _,num_cols=self.cat_num_split(file)
         for i in num_cols:
            file=self.caping_num_cols(file,i)
            print(file[i])
            return(file)

    def cat_num_split(self,file):
        print('Enter in  cat_num_split')
        #self.data_type_con(file)
        #self.data_con(file)
        cat_cols=file.select_dtypes(include='object').columns
        num_cols=file.select_dtypes(exclude='object').columns
        print('done in  cat_num_split')
        return(cat_cols,num_cols)
    
    def fill_null(self,file):
        print('Enter in  null_value filling')
        cat_cols , num_cols=self.cat_num_split(file)
        
        for i in file:
            if i in cat_cols:
                mode=self.find_mode(file,i)
                file[i]=file[i].fillna(mode)
                print(f'{i}__nullvaluefilling_of_cat_doen')
            elif i in num_cols:
                median=file[i].median()
                print(f'{i} = ',median)
                file[i]=file[i].fillna(median)
                print( len(file[i]))
               
                print(f'{i}__nullvaluefilling_of_num_doen')
        print('end  null_value filling')
        return(file) 
    
    
    
    def stand_data(self,file):
        print('Enter in stnderdization ')
        cat_cols,num_cols=self.cat_num_split(file)

        file[num_cols] = scaler.transform(file[num_cols]) 

        
        for i in file:
            if i in cat_cols:
                file[i]=encoders[i].transform(file[i])
            else:
                pass
        
               
        print('doen in stnderdization ')        

        return(file)       
    

    def clean_data(self,file):

        #file=file.drope['Loan_ID']
        con_data=self.data_type_con(file)
        data_3to3=self.data_con(con_data)
        #cat,num=self.cat_num_split(data_3to3)
        fill_data=self.fill_null(data_3to3)
        data_out=self.outlier_filling(fill_data)
        file=self.stand_data(data_out)
        for i in file:
            print(f'{i}__{file[i].isnull().sum()}')
         
        if 'Loan_ID'in file:    
            file=file.drop('Loan_ID',axis=1)   
        else:
            pass    
        
        
        #file.to_csv('test4.csv',index=False)    
        print('done data cleaning')

        return(file)