import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

def load_emotion_data(name):
    return pd.read_csv(name) #, encoding='iso-8859-1')

def split_train_test(data, test_ratio):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

def main():
    edata = load_emotion_data('NRCcsvEmotion.csv')
    print(edata.head())
    print(edata.info())
    #print(data["ocean_proximity"].value_counts())

    #train_set, test_set = split_train_test(hsData, 0.2)
    #print("Training Set: %s and Testing Set: %d" % (len(train_set), len(test_set)))
    #hsData["income_cat"] = np.ceil(hsData["median_income"] / 1.5)
    #hsData["income_cat"].where(hsData["income_cat"] < 5, 5.0, inplace = True)

    #split = StratifiedShuffleSplit(n_splits = 1, test_size = 0.2, random_state = 42)
    #for train_index, test_index in split.split(hsData, hsData["income_cat"]):
    #    strat_train_set = hsData.loc[train_index]
    #    strat_test_set = hsData.loc[test_index]
    #print(strat_test_set["income_cat"].value_counts() / len(strat_test_set))
    #for set_ in (strat_train_set, strat_test_set):
    #    set_.drop("income_cat", axis = 1, inplace = True)

    #hsData2 = strat_train_set.copy()
    #corr_matrix = hsData2.corr()
    #print(corr_matrix["median_house_value"].sort_values(ascending = False))

    #hsData2 = makeNewAttributes(hsData2)
    #corr_matrix = hsData2.corr()
    #print(corr_matrix["median_house_value"].sort_values(ascending = False))

    #hsData2 = strat_train_set.drop("median_house_value", axis = 1)
    #hs_labels = strat_train_set["median_house_value"].copy()
    #imputer = SimpleImputer(strategy = "median")
    #hs_num = hsData2.drop("ocean_proximity", axis = 1)
    #imputer.fit(hs_num)
    #print(imputer.statistics_)
    #print(hs_num.median().values)
    #x = imputer.transform(hs_num)
    #hs_tr = pd.DataFrame(x, columns = hs_num.columns)

    #hs_cat = hsData2["ocean_proximity"]
    #print(hs_cat.head(10))
    #hs_cat_encoded, hs_categories = hs_cat.factorize()
    #print(hs_cat_encoded)
    #print(hs_categories)
    #encoder = OneHotEncoder(categories="auto")
    #hs_cat_1hot = encoder.fit_transform(hs_cat_encoded.reshape(-1,1))
    #print(hs_cat_1hot)
    #print(hs_cat_1hot.toarray())
    #cat_encoder = CategoricalEncoder()
    #hs_cat_reshaped = hs_cat.values.reshape(-1,1)
    #hs_cat_1hot = cat_encoder.fit_transform(hs_cat_reshaped)
    #print(hs_cat_1hot)

if __name__ == "__main__":
    main()
