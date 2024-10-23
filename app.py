from flask import Flask, render_template, request
import pandas as pd
import random

# Load the dataset
df = pd.read_csv('books_dataset.csv')

# Convert 'Year of Publication' to numeric
df['Year of Publication'] = pd.to_numeric(df['Year of Publication'], errors='coerce')

app = Flask(__name__)

# Function to get books by year
def get_books_by_year(year):
    return df[df['Year of Publication'] == year][['Book Title', 'Author Name', 'Genre']].head(10)

# Function to get books by genre
def get_books_by_genre(genre):
    return df[df['Genre'].str.contains(genre, case=False, na=False)][['Book Title', 'Author Name', 'Year of Publication']].head(10)

# Function to get books by author
def get_books_by_author(author):
    return df[df['Author Name'].str.contains(author, case=False, na=False)][['Book Title', 'Year of Publication', 'Genre']].head(10)

# Function to get random books
def get_random_books():
    return df[['Book Title', 'Author Name', 'Year of Publication', 'Genre']].sample(n=10, random_state=random.randint(1, 100))

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    option = request.form['option']
    result = None

    if option == 'year':
        year_input = request.form['year']
        if year_input.isdigit():  # Check if the input is a valid number
            year = int(year_input)
            result = get_books_by_year(year)
        else:
            return render_template('index.html', books=[], message="Invalid year input. Please enter a valid year.")
    
    elif option == 'genre':
        genre = request.form['genre']
        result = get_books_by_genre(genre)
    
    elif option == 'author':
        author = request.form['author']
        result = get_books_by_author(author)
    
    elif option == 'random':
        result = get_random_books()
    
    if result is None or result.empty:
        return render_template('index.html', books=[], message="No books found!")
    else:
        return render_template('index.html', books=result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
