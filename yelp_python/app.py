# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
#POTAMIAS SOKRATIS 1115201400155
#PAVLOS TSAOYSAKIS 1115201400205
#PANAGIOTHS NIKOLOPOYLOS 1115201400128
import settings
import sys


def connection():
    ''' User this function to create your connections '''
    import sys
    sys.path.append(settings.MADIS_PATH)
    import madis

    con = madis.functions.Connection('/home/eliot/databases/ex3/yelp.db')
    
    return con

def classify_review(reviewid):
    #                                             63gqebKCZLt3ESZHBJAy2g
    # Create a new connection
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    cur.execute("SELECT var('myreviewid',?)",(reviewid,))
    cu = cur.execute("SELECT text FROM reviews WHERE review_id = var('myreviewid');")
    for i in cu:
        tempstring = str(i[0])
        cur.execute("SELECT var('mystring',?)",(tempstring,))
        cu2 = cur.execute("SELECT textwindow(var('mystring'),1,1);")
        for x in cu2:
            print x
           
    return [("business_name","result"),("yes",)]


def classify_review_plain_sql(reviewid):

    # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    #dhmioyrgia listas meta ta thetika kai arnitika gia thn pio eykolh diaxeirhsh
    positives = cur.execute("SELECT * FROM posterms;")
    pos_terms = []
    for a in positives:
        pos_terms.append(str(a[0]))

    neg_terms= []
    negatives = cur.execute("SELECT * FROM negterms;")
    for a in negatives:
        neg_terms.append(str(a[0]))

    cur.execute("SELECT var('myreviewid',?)",(reviewid,))
    cu = cur.execute("SELECT text FROM reviews WHERE review_id = var('myreviewid');")

    counter = 0
    #xwrizoyme to text sta kena afoy to kanoyme string
    for i in cu:
        review = str(i[0])
        review_words = review.split(" ")

    #oso yparxoyn akoma lejeis sto keimeno pairnoyme tiw prwtes 3 kai tiw elegxoyme 
    #an yparoyn sta thetika h ta arnhtika tiw afairoyme 
    #meta tiw 2 meta 1-1 
    #allivw pairnoyme tiw epomenew 3
    while len(review_words)>2:
        review_window=[]
        for x in xrange(0,3):
            review_window.append(review_words[x])
        for j in range(3,0,-1):
            small_window = ' '.join(review_window[:j])
            if small_window in pos_terms:
                counter += j
                review_words = review_words[j:]
                break
            elif small_window in neg_terms:
                counter -= j
                review_words = review_words[j:]
                break
            if j == 1:
                review_words = review_words[1:]
        #print counter

    small_window=''
    while len(review_words) > 0:
        review_window=[]
        for x in xrange(0,len(review_words)):
            review_window.append(review_words[x])
        for j in range(len(review_words),0,-1):
            small_window = ' '.join(review_window[:j])
            if small_window in pos_terms:
                counter += j
                review_words = review_words[j:]
                break
            elif small_window in neg_terms:
                counter -= j
                review_words = review_words[j:]
                break
            if j == 1:
                review_words = review_words[1:]

    cu = cur.execute("SELECT b.name FROM business b, reviews re WHERE re.review_id = var('myreviewid') and re.business_id=b.business_id;")
    for z in cu:
        bn_name = str(z[0])

    if counter >= 0:
        result="possitive"
    elif counter <0:
        result="negative"
    
    return [("business_name","result"),(bn_name,result),]

def updatezipcode(business_id,zipcode):
    
   # Create a new connection
    
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    #epilogh metablhtwn
    cur.execute("SELECT var('myzipcode',?)",(zipcode,))
    cur.execute("SELECT var('mybus',?)",(business_id,))
    cu = cur.execute("UPDATE business SET zip_code = var('myzipcode') WHERE business_id = var('mybus');")
    cu2 = cur.execute("SELECT business_id FROM business")
    answer = "no"
    for i in cu2:
        if not cmp(i,(business_id,)):
            answer ="yes"

    return [("result",),(answer,),]
    
    
def selectTopNbusinesses(category_id,n):

    # Create a new connection
    
    con=connection()
    res=[]
    resf=[]
    # Create a cursor on the connection
    cur=con.cursor()
    cur2 = con.cursor()
    cur3 = con.cursor()
    cur.execute("SELECT var('mycat',?)",(category_id,))
    cur.execute("SELECT var('myn',?)",(n,))
    cu = cur.execute("SELECT business_id FROM business_category where category_id=var('mycat');")    
    for i in cu:
        bn_id = str(i[0])
        positives=0
        cur2.execute("SELECT var('mybn_id',?)",(bn_id,))
        cu2 = cur2.execute("SELECT review_id FROM reviews WHERE business_id = var('mybn_id');")
        #gia ka8e review des an einai thethiko h oxi 
        for j in cu2:
            rv_id = str(j[0])
            cur3.execute("SELECT var('myrv_id',?)",(rv_id,))
            cu3 = cur3.execute("SELECT positive FROM reviews_pos_neg WHERE review_id = var('myrv_id');")
            for k in cu3:
                if k[0] == 1 :
                    positives+=1  
        res.append((bn_id,positives))
    #sort thn lista me fthinousa seira
    res.sort(key=lambda x: -x[1])
    #prostikh twn n prwtwn stoixewn sthn telikh lista      
    for x in range(0,int(n)):
        resf.append(res[x])
    return [("business_id", "numberOfreviews"),resf,]

def traceUserInfuence(userId,depth):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    


    return [("user_id",),]
