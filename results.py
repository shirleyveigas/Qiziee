
def save_result(name, branch, score, total):
    with open("results.txt", "a") as file:
        file.write(f"{name} ({branch}): {score}/{total}\n")

