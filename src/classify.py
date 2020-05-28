import pandas as pd
import json
import re

debug = True

class Classifier:
    
    def __init__(self, file_path, sheet_id=1):
        '''Initialize the classifier

        '''
        try:
            self.df = pd.read_excel(file_path, sheet_id)
        except:
            raise Exception("Unable to load excel data file.")

        try:
            
            self.config = json.load(open('config.json','r'))
        except:
            raise Exception("Unable to load json config file.")
        
        if debug:
            print(self.df.head())

    def classify(self):
        '''Classify the data into Startups, Mature companies, Universities/Schools, Government/Non-profit or Unclassified.

        '''
        # Iterate over all instances in the dataframe
        for index, row in self.df.iterrows():
            # Extract the year from the colum LAUCH DATE
            year = int(re.findall(r'\d+',str(row['LAUNCH DATE']))[0])
            # Obtain all the words helpful to classify the entity
            description_words ='%s %s %s' % (str(row['WEBSITE']), str(row['TAGLINE']).lower(), str(row['TAGS']).lower())
            
            startup_occurences = len(self.__intersection(self.config['startup']['keywords'],description_words))
            university_occurences = len(self.__intersection(self.config['university']['keywords'],description_words))
            gov_occurences = len(self.__intersection(self.config['gov']['keywords'],description_words))


            if startup_occurences > (university_occurences and gov_occurences) and year > self.config['startup']['post_year']: 
                self.df.loc[index, 'TYPE'] = self.config['startup']['tag']
            elif university_occurences > gov_occurences:
                self.df.loc[index, 'TYPE'] = self.config['university']['tag']
            elif gov_occurences:
                self.df.loc[index, 'TYPE'] = self.config['gov']['tag']
            elif year < self.config['company']['pre_year']:
                self.df.loc[index, 'TYPE'] = self.config['company']['tag']
            else:
                self.df.loc[index, 'TYPE'] = 'Unclassified'
        
        self.df.to_excel('../out/classified_data.xlsx')

        if debug:
            print(self.df.head())
            

    def __intersection(self, lst1, lst2):
        return [value for value in lst1 if value in lst2]

if __name__ == "__main__":
    # Initialize classifier instance
    c = Classifier('../data/Data_Science_Internship_Assignment.xlsx')
    c.classify()