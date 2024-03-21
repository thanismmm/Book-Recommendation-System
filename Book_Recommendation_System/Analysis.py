import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
books_df = pd.read_csv('Books.csv')
ratings_df = pd.read_csv('BX-Book-Ratings.csv')

# Assuming Books.csv has a column 'ISBN' and 'Book-Title', and BX-Book-Ratings.csv has 'ISBN' and 'Book-Rating'

# Merge the two dataframes on the 'ISBN' column
merged_df = pd.merge(ratings_df, books_df, on='ISBN')

# Group by 'Book-Title' and count the ratings
rating_counts = merged_df.groupby('Book-Title')['Book-Rating'].count().reset_index()

# Sort the values and get the top 10 rated books
top_rated_books = rating_counts.sort_values('Book-Rating', ascending=False).head(10)

# Plotting
plt.figure(figsize=(12, 8))
plt.barh(top_rated_books['Book-Title'], top_rated_books['Book-Rating'], color='skyblue')
plt.xlabel('Total Ratings')
plt.title('Top 10 Most Rated Books')
plt.gca().invert_yaxis() # To have the highest rated book at the top of the chart
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()
