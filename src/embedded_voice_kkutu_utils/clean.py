from os import remove

TARGETS = [
    "./assets/words.json",
]


def clean():
    [remove(each) for each in TARGETS]


def main():
    if __name__ == "__main__":
        print("Becuas of path issue, this script should not be executed directly.")
        exit(1)
    clean()
    print("Cleaned.")
