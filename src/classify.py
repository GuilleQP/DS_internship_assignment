import pandas as pd
import re

class Classifier:
    
    def __init__(self, file_path, sheet_id=1):
        '''Initialize the classifier

        '''
        self.df = pd.read_excel(file_path, sheet_id)
        print(self.df.head())

    def classify(self):
        '''Classify the data into Startups, Mature companies, Universities/Schools, Government/Non-profit or Unclassified.

        '''
        for index, row in self.df.iterrows():
            year = int(re.findall(r'\d+',str(row['LAUNCH DATE']))[0])
            
            if year > 1990:
                self.df.loc[index, 'TYPE'] = 'Startup'
        print(self.df.head())



if __name__ == "__main__":
    # Initialize classifier instance
    c = Classifier('../data/Data_Science_Internship_Assignment.xlsx')
    c.classify()