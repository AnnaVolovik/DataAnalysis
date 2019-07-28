# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


class DataAnalysis:

    """Demonstrating the ability to acquire, manipluate, clean and run basic data analysis with pandas.
    Assignment 3 within "Introduction to Data Science in Python" Coursera course by University of Michigan"
    """

    def answer_one(self):
        """
        Load the energy data from the file Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of energy.

        Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

        ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

        Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

        Rename the following list of countries (for use in later questions):

        "Republic of Korea": "South Korea",
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "China, Hong Kong Special Administrative Region": "Hong Kong"

        There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,
        e.g.
        'Bolivia (Plurinational State of)' should be 'Bolivia',
        'Switzerland17' should be 'Switzerland'.

        Next, load the GDP data from the file world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.

        Make sure to skip the header, and rename the following list of countries:

        "Korea, Rep.": "South Korea",
        "Iran, Islamic Rep.": "Iran",
        "Hong Kong SAR, China": "Hong Kong"

        Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.
        Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
        The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
        This function should return a DataFrame with 20 columns and 15 entries.
        """
        self.energy = (pd.read_excel(
            'source_files/Energy Indicators.xls',
            skiprows=list(range(0, 16, 1)) + [17] + list(range(245, 284, 1)),
            usecols=[2, 3, 4, 5],
            names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
                  .set_index('Country')
                  .replace('...', np.nan))
        self.energy.index = self.energy.index.str.replace(r"\(.*\)", "").str.rstrip()
        self.energy.index = self.energy.index.str.replace(r"[0-9]", "").str.rstrip()
        self.energy = self.energy.rename({'Republic of Korea': 'South Korea',
                                'United States of America': 'United States',
                                'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
                                'China, Hong Kong Special Administrative Region': 'Hong Kong'})
        self.energy['Energy Supply'] *= 1000000

        self.GDP = (pd.read_csv('source_files/world_bank.csv', skiprows=4)
               .set_index('Country Name')
               .rename({'Korea, Rep.': 'South Korea',
                        'Iran, Islamic Rep.': 'Iran',
                        'Hong Kong SAR, China': 'Hong Kong'})
               )
        self.ScimEn = pd.read_excel('source_files/scimagojr-3.xlsx').set_index('Country')

        cols = ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document',
                'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009',
                '2010', '2011', '2012', '2013', '2014', '2015']

        self.Top15 = (pd.merge(self.GDP, self.energy, how='inner', left_index=True, right_index=True)
                .merge(self.ScimEn.iloc[:15], how='inner', left_index=True, right_index=True)[cols])
        return self.Top15

    def answer_two(self):
        """
        The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the
        datasets, but before you reduced this to the top 15 items, how many entries did you lose?
        """
        return len((pd.merge(self.GDP, self.energy, how='inner', left_index=True, right_index=True)
                    .merge(self.ScimEn, how='inner', left_index=True, right_index=True)).index) \
               - len(self.answer_one().index)

    def answer_three(self):
        """
        What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
        This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.
        """
        return (np.mean(self.Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']],
                       axis=1)).sort_values(ascending=False)

    @staticmethod
    def average06_15(row):
        """ What is the mean Energy Supply per Capita?
        This function should return a single number. """
        data = row[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
        return pd.Series({'mean': np.mean(data), 'diff': data['2015'] - data['2006']})

    def answer_four(self):
        """By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
        This function should return a single number."""
        return self.Top15.apply(self.average06_15, axis=1).nlargest(6, 'mean').iloc[-1, 0]

    def answer_five(self):
        """What is the mean Energy Supply per Capita?
        This function should return a single number."""

        return self.Top15['Energy Supply per Capita'].mean()

    def answer_six(self):
        """What country has the maximum % Renewable and what is the percentage?
        This function should return a tuple with the name of the country and the percentage."""
        res = self.Top15.loc[lambda df: df['% Renewable'] == df['% Renewable'].max(), '% Renewable']
        return res.index[0], res.iloc[0]

    def answer_seven(self):
        """Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?
        This function should return a tuple with the name of the country and the ratio."""
        self.Top15['ratio'] = self.Top15['Self-citations'] / self.Top15['Citations']
        return self.Top15['ratio'].idxmax(), self.Top15.loc[self.Top15['ratio'].idxmax(), 'ratio']

    def answer_eight(self):
        """Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?
        This function should return a single string value."""
        self.Top15['Population'] = self.Top15['Energy Supply'] / self.Top15['Energy Supply per Capita']
        return self.Top15.nlargest(3, 'Population').index[-1]

    def answer_nine(self):
        """Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).
        This function should return a single number."""
        self.Top15['Citable docs per Capita'] = self.Top15['Citable documents'] / self.Top15['Population']
        return self.Top15['Citable docs per Capita'].corr(self.Top15['Energy Supply per Capita'], method='pearson')

    @staticmethod
    def cat_renewable(x, renewable_average):
        if x < renewable_average:
            return 0
        return 1

    def answer_ten(self):
        """Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
        This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank."""
        renewable_average = self.Top15['% Renewable'].mean()
        self.Top15['HighRenew'] = self.Top15['% Renewable'].apply(lambda x: self.cat_renewable(x, renewable_average))
        return self.Top15['HighRenew']

    @staticmethod
    def cat_continent(x):
        if x in ['China', 'Japan', 'India', 'South Korea', 'Iran']:
            return 'Asia'
        elif x in ['United Kingdom', 'Russian Federation', 'Germany', 'France', 'Italy', 'Spain']:
            return 'Europe'
        elif x in ['United States', 'Canada']:
            return 'North America'
        elif x == 'Brazil':
            return 'South America'
        return x  # Australia

    def answer_eleven(self):
        """Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the
        sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the
        estimated population of each country."""
        res = []
        for group, frame in self.Top15.groupby(self.cat_continent)['Population']:
            res.append(pd.Series({'size': frame.size, 'sum': frame.sum(), 'mean': frame.mean(), 'std': frame.std()},
                                 name=group))
        return pd.DataFrame(res)

    def answer_twelve(self):
        """Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
        This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries."""
        return self.Top15.groupby([self.Top15.index.map(self.cat_continent), pd.cut(self.Top15['% Renewable'], 5)]).size()

    def answer_thirteen(self):
        """Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
        e.g. 317615384.61538464 -> 317,615,384.61538464
        This function should return a Series PopEst whose index is the country name and whose values are the population estimate string."""
        self.Top15['PopEst'] = (self.Top15['Energy Supply'] / self.Top15['Energy Supply per Capita']).map('{:,}'.format)
        return self.Top15['PopEst']



ins = DataAnalysis()
print('Question 1', ins.answer_one())
print('Question 2', ins.answer_two())
print('Question 3', ins.answer_three())
print('Question 4', ins.answer_four())
print('Question 5', ins.answer_five())
print('Question 6', ins.answer_six())
print('Question 7', ins.answer_seven())
print('Question 8', ins.answer_eight())
print('Question 9', ins.answer_nine())
print('Question 10', ins.answer_ten())
print('Question 11', ins.answer_eleven())
print('Question 12', ins.answer_twelve())

