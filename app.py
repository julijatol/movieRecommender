from flask import Flask, render_template, request
import model

app = Flask (__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods = ['POST'])
def recommend():
    movie_name = request.form.get('movieName')

    if not movie_name:
        error_message = 'Please enter a movie name'
        return render_template('index.html', error_message=error_message)

    movie_name = movie_name.lower()

    try:
        recs = model.get_recommendations(movie_name)
        similarity_score = model.get_simscore(movie_name)
        index = model.get_ids(movie_name)
    except IndexError:
        error_message = f'Movie "{movie_name}" not found. Please enter a valid movie title or provide the exact movie name for the best recommendations.'
        return render_template('index.html', error_message=error_message)

    scores = []
    for item in similarity_score:
        num = int((item[1]*100))
        scores.append(num)

    result = [[title, score, idx] for title, score, idx in zip(recs, scores, index)]

    piechart_data = get_piechart_data(scores)
    bar_data = model.similarity_distribution(movie_name)[0]
    bar_data_l = model.similarity_distribution(movie_name)[1]

    return render_template('recommend.html',recommendations=result, movie_name=movie_name,
                               piechart_data=piechart_data, bar_data=bar_data, bar_data_l=bar_data_l)

def get_piechart_data(scores):
    data=[0,0,0,0,0]
    for i in scores:
        if i >=40:
            data[0] += 1
        elif i >= 30 and i<40:
            data[1] += 1
        elif i >= 20 and i<30:
            data[2] += 1
        elif i >= 15 and i<20:
            data[3] += 1
        elif i<15:
            data[4] += 1
    return data


if __name__ == "__main__":
    app.run(debug=True)

