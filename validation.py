import model
import numpy as np

def system_validation(title):
    title=title
    nums = model.get_simscore(title)
    scores = []
    for n in nums:
        scores.append(n[1])
    mean = np.mean(scores)
    median = np.median(scores)
    print(f"Mean Similarity Score: {mean}")
    print(f"Median Similarity Score: {median}")

title = str(input('Please provide a movie name:')).lower()
system_validation(title)