from flask import Flask, Response, render_template, request, redirect
import numpy as np
import pandas as pd
import json
from wtforms import TextField, Form
from songs import songs


df = pd.read_csv("PCADWGcluster.csv")
df = df.drop(['Unnamed: 0'],axis =1)
newdf = df.copy()
app = Flask(__name__)

class SearchForm(Form):
    autocomp = TextField('Enter Song', id='song_autocomplete')

def distance(a,b):
    a = np.array(a)
    b = np.array(b)
    distance=1-(np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b))) #calculating cosine distance between the PCA features of the two songs
    return distance

def Similarity(a, b):
    #isolating the features of the songs (PCA values)
    aA = a[6:12]
    bB = b[6:12]
    extra=0
    genre=0
    if a[1] == b[1]: #to make sure the same song is not recommended
        return 1000
    if a[3]==b[3]: #to make sure song by the same artist is not recommended unless no similar song is found
        extra = extra+0.5
    for i in a[4]:
        if i not in b[4]:
            genre = genre+1
    if genre == len(a[4]): #to make sure song that does not share the same genre is not recommended
        return 1000
    extra = extra+ 0.3*(genre) #penalising for genres that are not common
    if abs(a[5]-b[5])>5:
        extra = extra + abs(a[5]-b[5])/10 #penalising if the year gap between the songs is too large
    Distance = distance(aA,bB)
    return extra+Distance

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(songs), mimetype='application/json')


@app.route('/')
@app.route('/home')
def home():
    form = SearchForm(request.form)
    print(form)
    return render_template('home.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recommend',methods=["GET","POST"])
def final_recommend():
    req = request.form
    print(req)
    song = req['autocomp']
    print(song)
    song = song.lower()
    q = df.index[df['name']==song]
    qind = q[0]
    clust = df.iloc[qind]
    #isolating the rows belonging to the same cluster and sub cluster
    x = [clust['cluster_no'],clust['sub_cluster']]
    newdf = df[df['cluster_no']==x[0]]
    newdf = newdf[newdf['sub_cluster']==x[1]]
    newdf = newdf.reset_index()
    #print(newdf.shape)
    #finding query index for the song in the new isolated dataset
    q = newdf.index[newdf['name']==song]
    query_index1 = q[0]
    print(query_index1)
    simdict = []
    #calculating similarity between the input song and the rest of the songs in the dataset
    for i in range(0, newdf.shape[0]):
        a = np.array(newdf.iloc[query_index1])
        b = np.array(newdf.iloc[i])
        simdict.append((newdf.iloc[i]['name'],abs(Similarity(a, b))))
    newdf = df
    new = pd.DataFrame.from_dict(simdict)
    new.columns = ["name","score"]
    new=new.sort_values('score') #sorting the scores in ascending order
    res = new.head(10)
    song_list =  res.values.tolist()
    return render_template('recommend.html', song_list=song_list)



if __name__ == '__main__':
	app.run(debug=True)