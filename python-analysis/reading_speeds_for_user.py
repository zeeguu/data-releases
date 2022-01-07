# reading speed is difficult to compute 
# because we don't know whether the user really
# fully read the article 

# strategies 
# - analyze 
#   - only articles that are liked
#   - articles that have micro-sessions that last for more than X min

STUDY_ONLY_LIKED = True
MIN_ART_DURATION = 180 # seconds

USER_ID = 1911
READING_LANGUAGE = 'nl'
PRINT_DETAIL = False

from zeeguu.core.model import User, UserArticle, Language
from zeeguu.core.model.user_activitiy_data import UserActivityData




def find_the_like_event(user, article):
    all_events = UserActivityData.find(user)
    all_events = [each for each in all_events if each.event == "UMR - LIKE ARTICLE" and each.article_id==article.id]
    for each in all_events:
        if PRINT_DETAIL:
            print(f" - {each.time}: LIKE: {each.value}")

def print_sesssions_for(user, article, micro_sessions):

    if PRINT_DETAIL:
        print(f"{article.title}")

    total_time = 0
    for session in micro_sessions[article]:
        if PRINT_DETAIL:
            print(f" - {session.start_time}, {session.duration / 1000},  {session.article.title}")
        total_time += session.duration / 1000

    if PRINT_DETAIL:
        find_the_like_event(user, article)
    
    reading_speed = int (article.word_count * 60 / total_time)

    if total_time > MIN_ART_DURATION: 
        print(f"{session.start_time.date()}, {reading_speed}, {article.word_count}, {total_time}, {article.url}")

    if PRINT_DETAIL:
        print(f" Total time: {total_time/60}min")
        print(f" Word count: {article.word_count}")
        print(f" Reading speed: {reading_speed} wpm")
        input("continue...")
        
    

    


def print_reading_sessions():
    user = User.find_by_id(USER_ID)

    german_id = Language.find(READING_LANGUAGE).id


    current_article = None

    micro_sessions = {}
    
    for session in user.all_reading_sessions(language_id=german_id):

        user_article = UserArticle.find(user, session.article) 
        
        if not user_article:
            continue

        if STUDY_ONLY_LIKED and not user_article.liked:
            # we're only looking at liked articles for now
            continue

        if not current_article:
            # first session: simply set current article
            current_article = session.article
            micro_sessions[current_article] = []
        else:
            if current_article != session.article:
                # encountered a new article; report on the prev and start a new one
                if len(micro_sessions[current_article]) > 0:
                    print_sesssions_for(user, current_article, micro_sessions)
                current_article = session.article
                micro_sessions[current_article] = []
            else:
                # add this session to the micro_session for current article
                micro_sessions[current_article].append(session)
               
        
        

        


if __name__== "__main__":
    print_reading_sessions()
