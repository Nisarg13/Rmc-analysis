import pandas as pd
def main():
    dataset_name='complaints2019.xlsx'
    df=pd.read_excel(dataset_name)
    df.to_csv('complaints.csv',header=True,index=False)

if __name__=='__main__':
    main()

