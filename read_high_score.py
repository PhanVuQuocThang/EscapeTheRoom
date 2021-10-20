def read_file():
    with open("highest_score_endless.txt", "r") as high_score_file:
        highest_score = high_score_file.readline()
    return highest_score


def write_file(score):
    with open("highest_score_endless.txt", "w") as high_score_file:
        high_score_file.write(str(score))
    return None
