import pandas as pd
import numpy as np

df = pd.DataFrame({
'col1': ['A', 'A', 'B', np.nan, 'D', 'C'],
'col2': [2, 1, 9, 8, 7, 4],
'col3': [0, 1, 9, 4, 2, 3],
'col4': ['a', 'B', 'c', 'D', 'e', 'F']
})

print(df)

#df.sort_values(by=['col2'],inplace=True)
df = df.sort_values(by=['col2'])

print(df)

df.to_csv('test.csv')
