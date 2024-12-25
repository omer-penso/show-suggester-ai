from thefuzz import process
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def validate_user_input(tv_show_titles):
    """
    Ask the user for TV shows they liked and validate their input..
    """
    while True:
        user_input = input(
            "Which TV shows did you really like watching? Separate them by a ; (semicolon). Make sure to enter more than 1 show: "
        )
        user_shows = [show.strip() for show in user_input.split(";")]

        if len(user_shows) < 2:
            print("Please enter more than one show!")
            continue

        matched_shows = match_user_shows(user_shows, tv_show_titles)

        confirmation = input(
            f"Making sure, do you mean {', '.join(matched_shows)}? (y/n): "
        ).strip().lower()

        if confirmation == "y":
            return matched_shows
        else:
            print("Sorry about that. Lets try again, please make sure to write the names of the tv shows correctly”")


def match_user_shows(user_shows, tv_show_titles):
    """
    Match the user's input to real TV shows using fuzzy matching.
    """
    matched_shows = []
    for user_show in user_shows:
        match, _ = process.extractOne(user_show, tv_show_titles)
        matched_shows.append(match)
    return matched_shows
