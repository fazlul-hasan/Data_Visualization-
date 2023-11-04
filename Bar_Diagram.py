from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__,template_folder='templates')
club_data = pd.read_csv('spain_club_data.csv')


@app.route('/', methods=['GET', 'POST'])
def index():
    selected_club = None
    plot_url = None

    if request.method == 'POST':
        selected_club = request.form.get('club_selector')
        if selected_club and selected_club != 'Select a Club':
            club_stats = club_data[club_data['club'] == selected_club]
            if not club_stats.empty:
                img = io.BytesIO()
                club_stats = club_stats[['goal_scored', 'goals_against', 'goal_differences']]
                ax = club_stats.plot(kind='bar', figsize=(10, 6))
                ax.set_xlabel('Statistics')
                ax.set_ylabel('Values')
                ax.set_title(f'{selected_club} Goal Stats')
                ax.legend(title='Statistics', loc='upper right')
                plt.savefig(img, format='png')
                plt.close()
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()

    # We use the same 'Bar_Diagram.html' for both displaying the form and the plot
    return render_template('Bar_Diagram.html',
                           clubs=['Select a Club'] + club_data['club'].unique().tolist(),
                           selected_club=selected_club,
                           plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=False)
