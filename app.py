import os, codecs, yaml, markdown
from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('main.scss', 'docco.css', filters='pyscss', output='all.css')
assets.register('scss_all', scss)

data = yaml.load(open('data.yaml'))
data['markdown'] = {}

for group in data['writing']:
  for e in group['entries']:
    url = e['url'] = 'writing/%(y)s/%(u)s' % {'y': group['year'], 'u': e['url']}
    f = codecs.open(os.path.join('writing', e['file']),'r','utf-8','strict')
    data['markdown'][url] = {
      'title': e['title'],
      'date': e['date'],
      'text': markdown.markdown(f.read(), 
         extensions=['fenced_code', 'footnotes'])}

@app.route("/")
def index():
  return render_template('index.html', writing=data['writing'], projects=data['projects'])

@app.route("/writing")
def writing():
  return render_template('writing.html')

@app.route("/writing/<path:entry>")
def entry(entry):
  e = data['markdown'].get('writing/'+entry)
  return render_template('entry.html', title=e['title'], date=e['date'], text=e['text'])

@app.route("/projects")
def projects():
  return "Hello World!"

@app.route("/coursework")
def coursework():
  return render_template('coursework.html')

# TODO: Generalize this
@app.route("/courses/notes/dsp")
def dsp():
  return render_template('course-notes.html')

### Backwards compatibility ###
@app.route("/post/28504483668/devise-omniauth-facebook-js-sdk-tutorial")
def tumblr1():
  e = data['markdown'].get('writing/2012/fully-asynchronous-fb-login-with-devise-and-omniauth')
  return render_template('entry.html', title=e['title'], date=e['date'], text=e['text'])

@app.route("/post/24314393831/your-results-are-ready-23andme")
def tumblr1():
  e = data['markdown'].get('writing/2012/thoughts-on-23andme')
  return render_template('entry.html', title=e['title'], date=e['date'], text=e['text'])

@app.route("/post/43079165761/backpack-io-direct-multipart-uploads-to-s3-in-rails")
def tumblr1():
  e = data['markdown'].get('writing/2013/direct-multipart-uploads-to-s3-in-rails')
  return render_template('entry.html', title=e['title'], date=e['date'], text=e['text'])
###############################

if __name__ == "__main__":
  app.run()
