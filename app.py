from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_current_grade(grades, weights):
    """Calculate the current weighted grade."""
    earned = sum(grade * weight for grade, weight in zip(grades, weights))
    total_weight = sum(weights)
    return earned / total_weight if total_weight > 0 else 0


def required_score_for_target(grades, weights, remaining_weights, target_grade):
    """Calculate the required scores for remaining assignments to achieve the target grade."""
    current_weighted_score = sum(grade * weight for grade, weight in zip(grades, weights))
    total_weight = sum(weights) + sum(remaining_weights)
    required_score = (target_grade * total_weight - current_weighted_score) / sum(remaining_weights)
    return required_score

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    current_grade = None
    
    if request.method == 'POST':
        try:
            num_completed = int(request.form['num_completed'])
            num_remaining = int(request.form['num_remaining'])
            target_grade = float(request.form['target_grade'])
            
            grades = [float(request.form[f'grade_{i}']) for i in range(num_completed)]
            weights = [float(request.form[f'weight_{i}']) / 100 for i in range(num_completed)]
            remaining_weights = [float(request.form[f'rem_weight_{i}']) / 100 for i in range(num_remaining)]
            
            current_grade = calculate_current_grade(grades, weights)
            required_score = required_score_for_target(grades, weights, remaining_weights, target_grade)
            
            if 0 <= required_score <= 100:
                result = f"You need to average {required_score:.2f}% on the remaining assignments to achieve a final grade of {target_grade}%."
            else:
                result = "Your target grade is not achievable given the remaining assignments and their weights."
        except ValueError:
            result = "Invalid input. Please enter valid numbers."
    
    return render_template('index.html', result=result, current_grade=current_grade)

if __name__ == "__main__":
    app.run(debug=True)
