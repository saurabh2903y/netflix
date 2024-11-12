from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the CSV data
try:
    df = pd.read_csv('netflix_series.csv')
    print("CSV file loaded successfully.")
except FileNotFoundError:
    print("CSV file not found. Please check the path.")
    exit(1)

# Replace NaN values with an empty string or a valid JSON value
df.fillna('', inplace=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    category = request.args.get('category', '').lower()
    title = request.args.get('title', '').lower()
    page = int(request.args.get('page', 1))
    results_per_page = 10

    # Determine if searching by title or category
    if title:
        # Filter the dataframe based on the title
        print(f"Searching for title: {title}")  # Debug log
        filtered_df = df[df['title'].str.lower().str.contains(title, case=False, na=False)]
    elif category:
        # Filter the dataframe based on the category
        print(f"Searching for category: {category}")  # Debug log
        filtered_df = df[df['title'].str.lower().str.contains(category, case=False, na=False)]
    else:
        # No search criteria provided
        return jsonify({
            'total_results': 0,
            'total_pages': 0,
            'page_data': []
        })
    
    print(f"Found {len(filtered_df)} results for the search criteria.")  # Debug log

    # Pagination logic
    total_results = filtered_df.shape[0]
    total_pages = (total_results // results_per_page) + (1 if total_results % results_per_page > 0 else 0)
    
    start = (page - 1) * results_per_page
    end = start + results_per_page
    page_data = filtered_df.iloc[start:end].to_dict(orient='records')

    return jsonify({
        'total_results': total_results,
        'total_pages': total_pages,
        'page_data': page_data
    })

if __name__ == '__main__':
    app.run(debug=True)


