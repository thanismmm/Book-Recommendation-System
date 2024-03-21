import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the datasets
books_df = pd.read_csv('Books.csv')  # Replace with your actual path to the file
ratings_df = pd.read_csv('BX-Book-Ratings.csv')  # Replace with your actual path to the file

# Merge the dataframes based on ISBN
merged_df = pd.merge(books_df, ratings_df, on='ISBN')

# Group by 'Book-Title' or the appropriate column in Books.csv and calculate average ratings
average_ratings = merged_df.groupby('Book-Title')['Book-Rating'].mean().reset_index()

# Generate recommendation scores. This is typically done using a recommendation system, which
# is beyond the scope of this example. We'll use placeholder scores.
# You will need to replace this with your actual recommendation scores.
recommendation_scores = pd.Series([4.7, 4.3, 5, 3.1, 3.8], index=average_ratings['Book-Title'].head())

# Create a grouped bar chart
x = np.arange(len(average_ratings['Book-Title'].head()))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, average_ratings['Book-Rating'].head(), width, label='User Ratings')
rects2 = ax.bar(x + width/2, recommendation_scores, width, label='Recommendation Scores')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('User Ratings vs Recommendation Scores by Book')
ax.set_xticks(x)
ax.set_xticklabels(average_ratings['Book-Title'].head())
ax.legend()

# Function to attach a label above each bar, showing the score
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(round(height, 1)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Call the autolabel function
autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

# Show the plot
plt.show()
