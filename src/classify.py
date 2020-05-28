'''
Startups classifier

@author: Guillermo Quintana Pelayo
@date: 28-05-2020
'''
import pandas as pd
import json
import re

debug = True

class Classifier:
    
    def __init__(self, file_path, sheet_id=1):
        '''
        Initialize the classifier.

        Reads an excel file containing data and the
        json file with the desired configuration
        for the classification.

        Parameters:
        file_path (str): path to excel data file.
        sheet_id (int): Optional paramenter indicating the
            sheet containing the data, default=1.
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
        '''
        Classify the data into Startups, Mature companies, Universities/Schools, 
        Government/Non-profit or Unclassified.

        This method iterates over all the data instances and classifies them 
        into 5 categories according to the settings specified in the json
        config file. It looks how many keywords there are for each entity and
        the class with highest occurences gets selected as the type. This classification 
        is fairly simple but robust and easy customizable.
        The data is then exported into an output dir under the name 'classified data'.
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
        '''
        Returns the intersection of two lists.

        Parameters:
        lst1 (list): Not empty list 1
        lst2 (list): Not empty list 2

        Returns:
        list with the values appearing in both input lists.
        '''
        return [value for value in lst1 if value in lst2]

if __name__ == "__main__":
    # Initialize classifier instance
    c = Classifier('../data/Data_Science_Internship_Assignment.xlsx')
    # Classify the data
    c.classify()