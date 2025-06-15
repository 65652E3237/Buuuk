import json
from random import choice
from ai import call_gpt

GENRE_GROUPS = [
    {
        "group_id": "1",
        "label": "📘 Group 1: Traditional & Narrative Genres",
        "genres": [
            "Fiction",
            "Drama",
            "Crime",
            "Adventure",
            "Cozy",
            "Coming of age",
            "Contemporary",
            "Modernist",
            "Experimental",
            "20th century"
        ]
    },
    {
        "group_id": "2",
        "label": "🧠 Group 2: Philosophical, Abstract & Symbolic",
        "genres": [
            "Allegorical",
            "Absurdist",
            "Existentialist",
            "Mythological",
            "Dark",
            "Apocalyptic",
            "Dystopian",
            "Fantasy",
            "Cyberpunk",
            "Books About Books"
        ]
    },
    {
        "group_id": "3",
        "label": "📚 Group 3: Nonfiction, Reflective & Real-World",
        "genres": [
            "Nonfiction",
            "Memoir",
            "Autobiography",
            "Biography",
            "Cultural",
            "Americana",
            "Counselling",
            "Encyclopedic",
            "Diaries & Journals"
        ]
    },
    {
        "group_id": "4",
        "label": "👧 Group 4: Youth, Taboo, Family & Niche",
        "genres": [
            "Children's books",
            "Family & Relationships",
            "Adult",
            "Banned books",
            "Comics & Graphic Novels",
            "Ancient",
            "Arthurian",
            "Dark Humor"
        ]
    }
    ]

def main():
    with open('ad_books.json', 'r') as file:
        book_list = json.load(file)
       
    # Introduction
    name = input(f"Hello, welcome to Buuuk! This is a book recommendation tool. \nI'm Buuukie, how do I call you? ")
    print(f"Great! {name}, let's get started!")
    
    # Check the input
    user_choice = input("Do you have any preferences? (Enter 1 or 2) \n1. Surprise me!\n2. Show me options\n")
    while not user_choice.isdigit():
        user_choice = input("Please enter 1 or 2: ")
    while int(user_choice) not in range(1, 3):
        user_choice = input("Please enter 1 or 2: ")
    
    print()
    user_choice = int(user_choice)

    # 1. Get a random book from all list
    if user_choice == 1:
        is_content = choose_book(book_list)

    # 2. Get a random book from a specific topic
    elif user_choice == 2:
        filtered_books, genre_pick = choose_genre_group(book_list)
        is_content = choose_book(filtered_books)

    if is_content:
        print(f"Enjoy your book {name}! See you soon! ")    # Finished
    else:
        if user_choice == 2:
            if not filtered_books:
                if genre_pick == 0:
                    print(f"We ran out of books to recommend for this genre-group :(\nWe are working on finding more book recommendations!\nWe hope to see you again, {name}!")
                else:
                    print(f"We ran out of books to recommend for this genre :(\nWe are working on finding more book recommendations!\nWe hope to see you again, {name}!")
        else:
            print(f"We ran out of books to recommend :(\nWe are working on finding more book recommendations!\nWe hope to see you again, {name}!")


def choose_genre_group(book_list):
    # Show the genre-group options
    print("📘 Group 1: Traditional & Narrative Genres\n🧠 Group 2: Philosophical, Abstract & Symbolic\n📚 Group 3: Nonfiction, Reflective & Real-World\n👧 Group 4: Youth, Taboo, Family & Niche\n")

    genre_group_pick = input(f"Pick a genre-group (1 - 4): ")

    # Error handling
    while not genre_group_pick.isdigit():
        genre_group_pick = input("Please enter 1 - 4: ")
    while int(genre_group_pick) not in range(1, 5):
        genre_group_pick = input("Please enter 1 - 4: ")

    # Define the genres to filter by
    desired_genres = GENRE_GROUPS[int(genre_group_pick) - 1]

    # Different genre in the genre-groups
    genre_count = 1
    for genre in desired_genres['genres']:
        print(f"{genre_count}. {genre}")
        genre_count += 1
    print("0. Pick for me!")

    genre_pick = input(f"Pick a genre (1 - {genre_count}), or enter 0 if you can't choose: ")

    # Error handling
    while not genre_pick.isdigit():
        genre_pick = input(f"Please enter 0 - {genre_count}: ")
    while int(genre_pick) not in range(0, genre_count):
        genre_pick = input(f"Please enter 0 - {genre_count}: ")

    # Get a genre
    if genre_pick == '0':
        # Filter the book_list for books that match the desired genres
        filtered_books = [book for book in book_list if book['genre'] in desired_genres['genres']]
    else:
        book_genre = desired_genres['genres'][int(genre_pick) - 1]
        # Filter the book_list for books that match the desired genres
        filtered_books = [book for book in book_list if book['genre'] in book_genre]

    return filtered_books, genre_pick

def choose_book(filtered_books):
    is_content = False
    # Give the recommendation and check user's feedback
    # Recommendation
    while filtered_books:
        book = choice(filtered_books)
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Genre: {book['genre']}")
        response = call_gpt(f"Short description in 2 sentences about the book {book['title']} by {book['author']}")
        print()
        print(response)
        print()

        # Check if the user is content
        content = input("Are you content with your book recommendation? (Y(es) / N(o)) ")
        input_state = False
        while not input_state:
            if content == 'Y' or content == 'Yes' or content == 'y':
                is_content = True
                input_state = True
            elif content == 'N' or content == 'No' or content == 'n':
                is_content = False
                filtered_books.remove(book)
                input_state = True
            else:
                content = input("Please enter Y or N: ")
            
        # If is Y, finish the choosing process and return that the user is content
        # If is N, recommend another book and delete the previous recommendation from the list
        if is_content:
            return is_content
    
    return is_content # Return false for is_content if we run out of recommendations

if __name__ == "__main__":
    main()
