"""CSM Jokebot exercise"""

import time, csv, sys, requests


def tell_jokes(prompt, punchline):
    """Delivers the prompt, then after 2s the punchline too. """
    print(prompt)
    time.sleep(2)
    print(punchline)

def read_input(inp):
    """Reads user input and returns True if input is 'next', False if input is
    'quit'.
    """
    inp_set = {"next", "quit"}
    while inp not in inp_set:
        print("Not a valid input. Please try again: ")
        inp = input()
    if inp == "next":
        return True
    else:
        return False

def read_csv(file):
    """Reads CSV file containing the jokes. Returns the jokes as a list of lists.
    Each inner list contains the prompt and punchline separated by a comma.
    """
    with open(file) as jokes:
        joke_reader = csv.reader(jokes)
        res = []
        for j in joke_reader:
            res.append(j)
        return res


def get_Rdt_jokes():
    """Obtain jokes from Reddit thread. Returns a list of filtered jokes.
    """
    header = {'User-agent': 'My bot 0.1'}
    r = requests.get('https://www.reddit.com/r/dadjokes.json', headers = header)
    posts = r.json()["data"]["children"]
    posts_filtered = filter_posts(posts)
    posts_formatted = format_posts(posts_filtered)
    return posts_formatted

def filter_posts(posts):
    """Helper function for get_Rdt_jokes. Filter out jokes that are over_18 or
    has prompts that are not phrased as questions.
    """
    not_18 = [p for p in posts if not p["data"]["over_18"]]
    valid_starts = {"What", "Why", "How", "what", "why", "how"}
    question_form = [p for p in not_18 if p["data"]["title"].split(" ", 1)[0] in valid_starts]
    return question_form

def format_posts(posts):
    """Helper function for get_Rdt_jokes. Correctly format the Reddit page as a
    list of jokes containing only the prompt (title) and the punchline (selftext)
    separated by a comma.
    """
    joke_list = []
    for p in posts:
        joke = [p["data"]["title"], p["data"]["selftext"]]
        joke_list.append(joke)
    return joke_list


def run(jokes):
    """Runs the Jokebot program given a source of jokes. Exits program when no
    more jokes are available.
    """
    count = 0
    while count < len(jokes):
        if count > 0 and not read_input(input("Continue? Enter 'next' or 'quit': ")):
            print("Ending Jokebot")
            sys.exit()
        elif len(jokes[count]) != 2 or jokes[count][1] == "":
            print("Incorrectly formatted joke. Moving onto the next Joke. ")
            count += 1
            continue
        else:
            tell_jokes(jokes[count][0], jokes[count][1])
            count += 1
    print("Jokebot ran out of jokes")
    sys.exit()

def main():
    """Main function that starts the Jokebot according to the command line
    arguments.
    """
    if len(sys.argv) == 1:
        run(get_Rdt_jokes())
    elif len(sys.argv) == 2:
        format = sys.argv[1].split(".", 1)
        if len(format) != 2 or (len(format) == 2 and format[1] != "csv"):
            print("Jokes not provided in CSV file. ")
            sys.exit()
        else:
            run(read_csv(sys.argv[1]))
    else:
        print("Too many command line arguments. ")
        sys.exit()


if __name__ == "__main__":
    main()
