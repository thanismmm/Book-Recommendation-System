
import pickle
import streamlit as st
import numpy as np
import pandas as pd
import os

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://www.marketplace.org/wp-content/uploads/2021/01/Books_New-e1611252343470.jpg?fit=2879%2C1619");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
    object-fit: cover;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)


st.header("Book Recommendation System Using Big Data Analytics")
model = pickle.load(open('artifacts/model.pkl','rb'))
book_names = pickle.load(open('artifacts/book_names.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))


def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url



def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url       



selected_books = st.selectbox(
    "Select the Book Title",
    book_names
)

if st.button('Show Recommended Books'):
    recommended_books,poster_url = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])
    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])


# Initialize or load existing CSV file
csv_file = 'user_profiles.csv'
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=['book', 'rating'])
    df.to_csv(csv_file, index=False)
else:
    df = pd.read_csv(csv_file)

# Streamlit UI components
st.title("Book Rating System")
book_name = st.selectbox("Select a book", options=book_names)  # Use loaded book names
rating = st.slider("Rate the book (1 to 10)", 1, 10)
if st.button("Submit Rating"):
    # Append new rating to the CSV file
    new_entry = pd.DataFrame([[book_name, rating]], columns=['book', 'rating'])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.success("Rating submitted successfully!")

# Display current ratings (optional)
st.subheader("Current Ratings")
st.write(df)


# Load the user profiles data
user_profiles_path = 'user_profiles.csv'  # Make sure to adjust the path as necessary
user_profiles_df = pd.read_csv(user_profiles_path)

# Filter books with rating greater than 5
high_rated_books = user_profiles_df[user_profiles_df['rating'] > 4]

# Streamlit application
def main():
    st.title('Recommend Book Based on user rating behaviour')
    
    # Make sure to only proceed with sampling if there are books available
    if high_rated_books.empty:
        st.write("No books with a rating higher than 5 found.")
    else:
        # Button to recommend a book
        if st.button('Recommend a Book'):
            # Ensure that high_rated_books is not empty before sampling
            if not high_rated_books.empty:
                selected = high_rated_books.sample().iloc[0]['book']  # Randomly select one book
                recommended_books, poster_url = recommend_book(selected)
                # Assuming recommend_book and how you handle the recommended_books and poster_url are correctly implemented
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text(recommended_books[4])
                    st.image(poster_url[4])
                with col2:
                    st.text(recommended_books[3])
                    st.image(poster_url[3])
                with col3:
                    st.text(recommended_books[5])
                    st.image(poster_url[5])
            else:
                st.write("No books available for recommendation.")
        else:
            st.write("Click the button to get a book recommendation.")



if __name__ == "__main__":
    main()


