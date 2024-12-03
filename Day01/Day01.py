# create virtual environment .venv
# python -m venv .venv

# upgrade pip if necessary
# python -m pip install --upgrade pip

# activate virtual environment .venv
# .\.venv\Scripts\activate

# install required libraries
# pip install -r .\requirements.txt
# requirements.txt contains:
# numpy
# tensorflow
# keras==2.12
# matplotlib
# get errors without deprecating keras

# uninstall libraries if needed to start again..
# pip freeze > current.txt
# pip uninstall -r .\current.txt -y

#_ga=GA1.2.1374795190.1701415040; 
# _gid=GA1.2.314749366.1733226540; 
# session=53616c7465645f5f22bc9f1fd4184fd1828df55fed38976e974abd7fa28d75d148f435b0b729052932f8355846cfff71f78ab51579fb3eab4db1fa81437d9615; _gat=1; _ga_MHSNPJKWC7=GS1.2.1733226540.19.1.1733228141.0.0.0

# uses read csv and loads data into a data frame with read_csv
# manipulates pandas dataframes

import pandas as pd

if __name__ == '__main__':
    file = 'C:\\Users\\marki\\OneDrive\\Documents\\AI Apprentiship\\20241203 Advent of Code 2024\\aoc2024\\Day01\\trail.csv'
    file = 'C:\\Users\\marki\\OneDrive\\Documents\\AI Apprentiship\\20241203 Advent of Code 2024\\aoc2024\\Day01\\day01stage01.csv'
    print(file)
    df = pd.read_csv(file, sep='\s+', names=['a','b'], index_col=False)
    print(df.head(8))
    df_a = df[['a']].copy()
    df_a = df_a.sort_values(by=['a'], ignore_index=True)
    df_b = df[['b']].copy()
    df_b = df_b.sort_values(by=['b'], ignore_index=True)
    print(df_a.head(8))
    print(df_b.head(8))

    total_dis = 0
    length = len(df_a)

    for i in range(length):
        x = df_a['a'].iloc[i]
        y = df_b['b'].iloc[i]
        dis = abs(x-y)
        total_dis += dis
        print(x,y,dis,total_dis)

    for x in df_a:
        z = df_b[df_b['b']==x]
        print (f"x: {x}")

    print(f"Part 1 answer:", total_dis)

    total_product = 0

    for i in range(length):
        x = df_a['a'].iloc[i]
        y = df_b.loc[df_b['b'] == x]
        count_value_x_in_df_b = len(y)
        if count_value_x_in_df_b:
            product = x * count_value_x_in_df_b
            total_product += product
            print(i,x,count_value_x_in_df_b,product,total_product)
        else:
            print(i,x,'None in b')

    print(f"Part 2 answer:", total_product)
