# Created by Raghu Acc Rullx Boy ❤️

from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

class FacebookCommenter:
    def comment_on_post(self, cookie, post_id, comment):
        session = requests.Session()
        session.headers.update({
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; SM-G960U)',
            'accept-language': 'en-US,en;q=0.9',
        })

        # Load the Facebook post
        response = session.get(f'https://mbasic.facebook.com/{post_id}', cookies={'cookie': cookie})
        action_url = re.search(r'method="post" action="([^"]+)"', response.text)
        fb_dtsg = re.search(r'name="fb_dtsg" value="([^"]+)"', response.text)
        jazoest = re.search(r'name="jazoest" value="([^"]+)"', response.text)

        if not (action_url and fb_dtsg and jazoest):
            return "❌ Invalid Cookie or Post ID!"

        # Prepare data to post comment
        data = {
            'fb_dtsg': fb_dtsg.group(1),
            'jazoest': jazoest.group(1),
            'comment_text': comment,
            'comment': 'Submit'
        }

        # Post the comment
        post_url = f"https://mbasic.facebook.com{action_url.group(1).replace('amp;', '')}"
        result = session.post(post_url, data=data, cookies={'cookie': cookie})

        if 'comment_success' in result.url:
            return "✅ Comment Posted Successfully!"
        else:
            return "❌ Failed to Post Comment."

# HTML Template
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Comment Bot by Raghu Acc Rullx Boy ❤️</title>
    <style>
        body { background-color: #000; color: yellow; text-align: center; font-family: Arial; padding: 20px; }
        input, button { margin: 10px; padding: 10px; width: 80%; max-width: 300px; border-radius: 5px; }
        button { background-color: yellow; color: black; border: none; cursor: pointer; }
        button:hover { background-color: orange; }
    </style>
</head>
<body>
    <h1>Comment Bot by Raghu Acc Rullx Boy ❤️</h1>
    <form method="POST">
        Post ID: <input type="text" name="post_id" required><br>
        Cookie: <input type="text" name="cookie" required><br>
        Comment: <input type="text" name="comment" required><br>
        <button type="submit">Submit</button>
    </form>
    <p>{{ message }}</p>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        post_id = request.form['post_id']
        cookie = request.form['cookie']
        comment = request.form['comment']

        commenter = FacebookCommenter()
        message = commenter.comment_on_post(cookie, post_id, comment)

    return render_template_string(html_template, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
