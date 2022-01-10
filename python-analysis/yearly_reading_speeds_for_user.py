# Reading speed is difficult to compute
# because we don't know whether the user really
# fully read the article or not

# Strategies employed in this script
# - analyze
#   - only articles that are liked (not a very good approach because there are users who might not use the like button)
#   - only articles that were interacted with for more than a number seconds


# To think about... maybe the grouping should not be done by year,
# but rather, by a group of N read articles;
# It would be natural to expect that increase in reading speed
# is related to the number of articles read not years passing by
#
# Also this does not take into account the article difficulty;
# if the learner reads more difficult articles, it would not bt
# surprising that they read faster

ANALYZE_ONLY_LIKED = True
MIN_ART_DURATION_IN_SEC = 180

PRINT_DETAIL = False

USER_ID = 534
READING_LANGUAGE = "de"

import pandas as pd
from sqlalchemy.sql.expression import desc
from zeeguu.core.model import User, Language
from macro_session import extract_macro_sessions_from_db


def filter_sessions(macro_sessions, only_liked=ANALYZE_ONLY_LIKED):

    result = []
    for macro_session in macro_sessions:

        if only_liked and not macro_session.user_article.liked:
            continue

        if macro_session.total_time < MIN_ART_DURATION_IN_SEC:
            continue

        result.append(macro_session)
    return result


def summarize_yearly_reading_speed(macro_sessions):

    data_table = []

    for session in macro_sessions:
        data_table.append(
            [
                session.start_date(),
                session.start_date().year,
                session.reading_speed,
                session.total_time,
                session.article.word_count,
            ]
        )

    df = pd.DataFrame(
        data_table,
        columns=["date", "year", "reading_speed", "total_time", "word_count"],
    )
    # print(df)

    year_and_speed = df[["year", "reading_speed"]]
    q_low = year_and_speed["reading_speed"].quantile(0.1)
    q_hi = year_and_speed["reading_speed"].quantile(0.9)
    df_filtered = year_and_speed[
        (year_and_speed["reading_speed"] < q_hi)
        & (year_and_speed["reading_speed"] > q_low)
    ]

    print(df_filtered.groupby("year").agg(["count", "median"]))


def analyze_user(user_id, language, only_liked=ANALYZE_ONLY_LIKED):
    user = User.find_by_id(user_id)
    language_id = Language.find(language).id

    macro_sessions = extract_macro_sessions_from_db(user, language_id)
    macro_sessions = filter_sessions(macro_sessions, only_liked)

    if PRINT_DETAIL:
        for macro_session in macro_sessions:
            macro_session.print_details()
            input("<Enter to continue>")

    summarize_yearly_reading_speed(macro_sessions)


def print_usr(description, user_id, language):
    marker = "=" * len(description)
    print(marker)
    print(description)
    print(marker)

    print("** Only LIKED:")
    analyze_user(user_id, language, only_liked=True)
    print("** All articles: ")
    analyze_user(user_id, language, only_liked=False)
    print("")
    print("")


if __name__ == "__main__":

    print_usr(
        "A user who stopped studying German and started being slower again?", 534, "de"
    )

    # print_usr("A user who read a lot and improved over time", 1911, "nl")

    # print_usr("A user with decrease in speed between 2020 and 2021", 2465, "fr")

    # print_usr("French reader with few articles", 2067, "fr")
    # print_usr("French reader in same class as previous", 2315, "fr")
    # print_usr("French reader in same class as previous two", 2066, "fr")
    # print_usr("Fourth student in the same class", 2079, "fr")

    # print_usr("A self-declared A2 reader of Danish", 2832, "da")

    # print_usr("Another self-declared A2 reader of Danish", 3159, "da")

    # print_usr("Self-declared A2 reader of Danish (w/ gmx.de email)", 2834, "da")

    # print_usr("A slow Danish reader", 2953, "da")
