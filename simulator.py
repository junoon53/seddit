import praw
import nltk
import markovify
print praw.__version__


r = praw.Reddit('bot_1')


def prepare_text(text):
    text = text.strip()
    if not text.endswith((".", "?", "!")):
        text += "."

    return text

def get_comments(sub_id):
    sbmn = r.submission(id=sub_id)
    for top_level_comment in sbmn.comments:
        try:
            body =  top_level_comment.body 
            sentences = str(body).split("\n")
            for sentence in sentences:
                if len(sentence) > 0:
                    # print "# ", sentence
                    tokens =  nltk.word_tokenize(prepare_text(sentence))
                    print "comment:",tokens
            print "="*30
        except:
            None
 
def get_submissions(subreddit_name,limit):
    titles = []
    subreddit = r.subreddit(subreddit_name)
    for s in subreddit.hot(limit=limit):
        sbmn = r.submission(id=s)
        title =  prepare_text(sbmn.title)
        titles.append(title)
        print title
        # tokens =  nltk.word_tokenize(title)
        # print "title:",tokens
        # print "#"*30
    return "\n".join(titles)

def train_model(text):
    model = markovify.Text(text)
    return model


if __name__ == "__main__":
    f = open("sub_titles.txt","r")
    text = f.read().decode('utf8')
    if len(text) <= 0:
        f = open("sub_titles.txt","w")
        text = get_submissions("worldnews",200)
        f.write(text.encode('utf8'))
        f.close()

    model = train_model(text)

    print "#"*30

    for i in xrange(50):
        print model.make_sentence()
