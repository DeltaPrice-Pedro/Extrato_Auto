import pandas as pd

data = {
    'word' : ['a', 'b'],
    'letter' : ['C', 'C'],
    'value' : [1, 2]
}
df = pd.DataFrame(data)
letter_c = df.loc[df['letter'] == 'C']
for w, v in letter_c.loc[:, ['word','value']].values:
    print(w, v)