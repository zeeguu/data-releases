# Reading speed is difficult to compute
# because we don't know whether the user really
# fully read the article or not

# Strategies employed in this script
# - analyze
#   - only articles that are liked (not a very good approach because there are users who might not use the like button)
#   - only articles that were interacted with for more than a number seconds

# Some notes from testing with users:
#  1911, nl = a large number of articles
#  all articles
#   2019           28.0
#   2020           47.0
#   2021           73.0
#  only LIKED articles
#   2020           70.0
#   2021           84.0
#
#  534, de = a user who stopped studying and started being slower again?
#  all articles
#      reading_speed
#              count       mean
# year
# 2018           208  67.432692
# 2019            39  75.589744
# 2020            12  53.000000
# 2021             1  37.000000

#  only LIKED articles
# 2018            81  43.543210
# 2019            14  48.928571
# 2020             1  29.000000
#  2650, fr = impossibly high speeds
#  all articles
#     76,5
#  only LIKED
#     74


#  2465, fr, all (not sufficent LIKED) = decrease in speed between 2020 and 2021...
#   2020             2  50.500000
#   2021             6  41.166667# 2694, de
# - only read in 2021
# only liked:
#     57.5


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
from zeeguu.core.model import User, Language
from macro_session import extract_macro_sessions_from_db


def filter_sessions(macro_sessions):

    result = []
    for macro_session in macro_sessions:

        if ANALYZE_ONLY_LIKED and not macro_session.user_article.liked:
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
    print(df)

    year_and_speed = df[["year", "reading_speed"]]
    q_low = year_and_speed["reading_speed"].quantile(0.1)
    q_hi = year_and_speed["reading_speed"].quantile(0.9)
    df_filtered = year_and_speed[
        (year_and_speed["reading_speed"] < q_hi)
        & (year_and_speed["reading_speed"] > q_low)
    ]

    print(df_filtered.groupby("year").agg(["count", "mean"]))


if __name__ == "__main__":

    user = User.find_by_id(USER_ID)
    language_id = Language.find(READING_LANGUAGE).id

    macro_sessions = extract_macro_sessions_from_db(user, language_id)
    macro_sessions = filter_sessions(macro_sessions)

    if PRINT_DETAIL:
        for macro_session in macro_sessions:
            macro_session.print_details()
            input("<Enter to continue>")

    summarize_yearly_reading_speed(macro_sessions)
