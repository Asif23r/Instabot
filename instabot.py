from instagrapi import Client
import time

# Instagram automation account credentials
IG_USERNAME = "automation_account"
IG_PASSWORD = "automation_password"

# Owner username (jisse command milegi)
OWNER_USERNAME = "command_sender_account"

# Login to Instagram
cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)

print(f"[+] Logged in as {IG_USERNAME}")

# Continuously check for new DMs
while True:
    try:
        inbox = cl.direct_threads()
        for thread in inbox:
            if not thread.messages:
                continue

            msg = thread.messages[0].text.strip().lower()
            sender = thread.messages[0].user.username

            if sender != OWNER_USERNAME:
                continue  # Ignore other users

            if msg.startswith(".follow"):
                username = msg.split(" ", 1)[1]
                user_id = cl.user_id_from_username(username)
                cl.user_follow(user_id)
                cl.direct_send(f"Followed {username}", [thread.id])

            elif msg.startswith(".like"):
                username = msg.split(" ", 1)[1]
                user_id = cl.user_id_from_username(username)
                medias = cl.user_medias(user_id, 1)
                if medias:
                    cl.media_like(medias[0].id)
                    cl.direct_send(f"Liked latest post of {username}", [thread.id])

            elif msg.startswith(".comments"):
                username = msg.split(" ", 1)[1]
                user_id = cl.user_id_from_username(username)
                medias = cl.user_medias(user_id, 1)
                if medias:
                    cl.media_comment(medias[0].id, "Nice post!")
                    cl.direct_send(f"Commented on {username}'s post", [thread.id])

            elif msg.startswith(".commentlike"):
                username = msg.split(" ", 1)[1]
                user_id = cl.user_id_from_username(username)
                medias = cl.user_medias(user_id, 1)
                if medias:
                    comments = cl.media_comments(medias[0].id)
                    if comments:
                        cl.media_comment_like(comments[0].pk)
                        cl.direct_send(f"Liked top comment on {username}'s post", [thread.id])

            elif msg == ".info":
                cl.direct_send(f"Bot running\nLogged in as: {IG_USERNAME}\nOwner: {OWNER_USERNAME}", [thread.id])

    except Exception as e:
        print("Error:", e)
    time.sleep(10)  # check every 10 seconds