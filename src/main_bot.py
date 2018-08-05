# Jeffrey A. Wilson
# Created: Aug. 5, 2018
# Entry point for Running the Reddit Bot


import praw  # Reddit API Wrapper
import config
import time
import os

phrase = "perfectly balanced"

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
# times.
#######################################################


def run_bot(p, comments_replied_to):
    replied = False
    print("\nObtaining comments...")

    for comment in p.subreddit('Test').comments(limit=25):
        if phrase in comment.body.lower() and comment.id not in comments_replied_list and comment.author != p.user.me():
            comment.reply("As all things should be")
            print("Replied to comment " + comment.id)
            replied = True

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as file:
                file.write(comment.id + "\n")

    if not replied:
        print("Did not reply to any comments")

    # Sleep for 10 Seconds so we can chill a bit
    print("Sleeping for 10 seconds")
    time.sleep(10)

    return


#######################################################
# Grabs the log of previously replied comments. If the
# file exists stores the data from it into an empty
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

while True:
    run_bot(bot_profile, comments_replied_list)
