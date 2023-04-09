# import pandas as pd
#
# csv1 = pd.read_csv('climate_tech_eventbrite.csv')
# csv2 = pd.read_csv('Events-Grid view.csv')
#
# csv1 = csv1.drop(csv1.columns[[0, 1, 2, 8]], axis=1)
#
# csv1.insert(1, csv2.columns[1], csv2.iloc[:,0], True)
# csv1.insert(4, csv2.columns[3], csv2.iloc[:,0], True)
# csv1.insert(7, csv2.columns[6], csv2.iloc[:,0], True)
#
# csv1 = pd.concat([csv1, csv2.iloc[:, 9:20]], axis=1)
#
# csv1.columns = csv2.columns.values
#
# for col in csv1.columns:
#     print(col)
#
# csv1.to_csv('test.csv', index=False)
#