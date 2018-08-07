# Jeffrey A. Wilson
# Created: Aug. 5, 2018
# Entry point for Running the Reddit Bot


import praw  # Reddit API Wrapper
import config
import os

phrase = config.searching_phrase
banned_subreddits = config.banned_subreddits
response = config.response

#######################################################
# Grab profile credentials from the private config file
# return the profile object to the calling routine of
# the script.
#######################################################


def bot_login():
    r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent="Ensures all comments are perfectly balanced.")

    return r

#######################################################
# This function will be executed on a loop in the
# calling routine. Scans the comments looking for the
# phrase and replies to it. Logs the comment ID to
# make sure we don't reply to the same comment multiple
# times. Takes in the bot's profile (p) and comments
# previously replied to as parameters.
#######################################################


def run_bot_initial(p, comments_replied_to):
    replied = False
    print("\nObtaining 100 INITIAL Comments...")

    for comment in p.subreddit('Test').comments(limit=100):
        if phrase in comment.body.lower() and comment.id not in comments_replied_list and comment.author != p.user.me():
            comment.reply(response)
            print("Replied to comment " + comment.id)
            replied = True

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as file:
                file.write(comment.id + "\n")

    if not replied:
        print("Did not reply to any comments")

    return


def run_bot_passive(p, comments_replied_to):
    replied = False
    print("\nINTERCEPTING NEW COMMENTS...")

    for comment in p.subreddit('Test').stream.comments():
        if phrase in comment.body.lower() and comment.id not in comments_replied_list and comment.author != p.user.me():
            comment.reply("As all things should be")
            print("Replied to comment " + comment.id)
            replied = True

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as file:
                file.write(comment.id + "\n")

    if not replied:
        print("Did not reply to any comments")

    return

#######################################################
# Grabs the log of previously replied comments. If the
# file exists stores the data from it into a
# list. If it doesn't, create an empty list. Return the
# list to the calling routine.
#######################################################


def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to


#############################################
# Entry point (Main) for running the script #
#############################################

# Should only be executed once
bot_profile = bot_login()
comments_replied_list = get_saved_comments()
run_bot_initial(bot_profile, comments_replied_list)

print("\nBOT HAS ENTERED PASSIVE MODE")
while True:
    run_bot_passive(bot_profile, comments_replied_list)

#############################################
# End of Script                             #
#############################################
