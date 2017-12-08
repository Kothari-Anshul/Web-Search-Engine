import urllib2
import re

# This method returns the source code for any input url
def get_page_content(url):
    try:
        response = urllib2.urlopen(url)
        page_source = response.read()
        return page_source
    except:
        return ""
#print get_page_content('jjjjj.com')
#print get_page_content("https://www.google.com")
# This method add the keyword and corresponding url to index
def add_to_index(index, keyword,url):
    
       
    if(keyword in index):
        index[keyword].append(url)
        return index
    index[keyword] = [url]
    return index
# This method add all the words with the page url to the index using add_index

def remove_all_tags(page_content):
    return re.sub('<[^<>]*>'," ",page_content)
#print remove_all_tags(get_page_content('https://stackoverflow.com/questions/16720541/python-string-replace-regular-expression'))

def add_page_to_index(index,page_content,url):
    page_content = remove_all_tags(page_content)
    list_of_keyword = page_content.split()
    for word in list_of_keyword:
        index = add_to_index(index,word,url)
   

#This method returns the union of two list, to avoid duplicates in the list
def union(p,q):
    return list(set(p) | set(q))
# This is web_crawler which returns index built by looping over and over urls found on any page
def web_crawler(seed_page):
    crawled = []
    to_be_crawled = [seed_page]
    index = {}
    graph = {}
    while(to_be_crawled != [] and len(crawled) < 1):
        page = to_be_crawled.pop()
        if(page not in crawled):
            page_content = get_page_content(page)
            links = get_all_links(page_content)
            add_page_to_index(index,page_content,page)
            to_be_crawled = union(to_be_crawled,links)
            crawled.append(page)
            graph[page] = links
    return index,graph
    
def get_all_links(page_content):
    return re.findall('<[\s]*a[\s]*href[\s]*=[\s]*"[\s]*([^\s]+)[\s]*"',page_content)


def compute_ranks_of_pages(graph,no_of_iterations):
    ranks = {}
    #damping factor to be consider for any sort of randomness in the web surfing
    d = 0.8
    n = len(graph)
    for page in graph:
        ranks[page] = 1.0/n
    for i in range(0,no_of_iterations):
        newranks = {}
        for page in graph:
            newranks[page] = (1-d)/n
            for node in graph:
                if(page in graph[node]):
                    newranks[page] += (d*ranks[node])/len(graph[node])
        ranks = newranks
    return ranks

# Method for lookup in the search engine with suitable keyword as input and must return relevant pages in sorted order according to their ranks
def lookup(index,ranks, keyword):
    if(keyword not in index):
        return []
    urls = index[keyword]
    return sorted_urls(urls,ranks)

def sorted_urls(urls,ranks):
    result = []
    temp_ranks = {}
    for items in ranks:
        temp_ranks[items] = ranks[items]
    
    for i in range(0,len(ranks)):
        best_url = ""
        best_rank = -1
        for item in temp_ranks:
            if(temp_ranks[item] > best_rank):
                # then update the following:
                best_rank = temp_ranks[item]
                best_url = item
        result.append(best_url)
        temp_ranks[best_url] = -1
    return result
        
#print web_crawler('https://stackoverflow.com/questions/16720541/python-string-replace-regular-expression')

#print get_page_content('<a href="https://stackoverflow.com/users/signup?ssrc=site_switcher&amp;returnurl=%2fusers%2fstory%2fcurrent&amp;amp;utm_source=stackoverflow.com&amp;amp;utm_medium=dev-story&amp;amp;utm_campaign=signup-redirect" class="login-link js-gps-track"     data-gps-track="site_switcher.click({ item_type:10 })">Sign up</a> or <a href="https://stackoverflow.com/users/login?ssrc=site_switcher&amp;returnurl=https%3a%2f%2fstackoverflow.com%2fquestions%2f8113782%2fsplit-string-on-whitespace-in-python" class="login-link js-gps-track"     data-gps-track="site_switcher.click({ item_type:11 })">log in</a> to customize your list.)

graph = {'http://udacity.com/cs101x/urank/kathleen.html': [],'http://udacity.com/cs101x/urank/zinc.html': ['http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/arsenic.html'], 'http://udacity.com/cs101x/urank/hummus.html': [],'http://udacity.com/cs101x/urank/arsenic.html': ['http://udacity.com/cs101x/urank/nickel.html'],'http://udacity.com/cs101x/urank/index.html': ['http://udacity.com/cs101x/urank/hummus.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/zinc.html'], 'http://udacity.com/cs101x/urank/nickel.html': ['http://udacity.com/cs101x/urank/kathleen.html']}
#print graph
ranks = compute_ranks_of_pages(graph,10)
#ranks = compute_ranks(graph)
#print ranks

index = {'<body>': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'Chef</a>': ['http://udacity.com/cs101x/urank/index.html'], '<html>': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'Here': ['http://udacity.com/cs101x/urank/index.html'], 'tablesppons': ['http://udacity.com/cs101x/urank/kathleen.html'], 'to': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'garbonzo': ['http://udacity.com/cs101x/urank/kathleen.html'], 'World': ['http://udacity.com/cs101x/urank/arsenic.html'], 'Recipe</a>': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/index.html'], 'it.': ['http://udacity.com/cs101x/urank/hummus.html'], 'them': ['http://udacity.com/cs101x/urank/kathleen.html'], '</html>': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'Hummus': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'recipe</a>.': ['http://udacity.com/cs101x/urank/zinc.html'], 'buttercream': ['http://udacity.com/cs101x/urank/kathleen.html'], 'recipe!': ['http://udacity.com/cs101x/urank/nickel.html'], 'Recipe': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'blender.': ['http://udacity.com/cs101x/urank/kathleen.html'], 'try': ['http://udacity.com/cs101x/urank/zinc.html'], '<p>': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'Go': ['http://udacity.com/cs101x/urank/hummus.html'], '</ul>': ['http://udacity.com/cs101x/urank/index.html'], 'opinions,': ['http://udacity.com/cs101x/urank/index.html'], 'href="http://udacity.com/cs101x/urank/zinc.html">Zinc': ['http://udacity.com/cs101x/urank/index.html'], 'For': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/zinc.html'], 'hummus.': ['http://udacity.com/cs101x/urank/hummus.html'], 'hummus,': ['http://udacity.com/cs101x/urank/zinc.html'], 'are': ['http://udacity.com/cs101x/urank/index.html'], 'href="http://udacity.com/cs101x/urank/arsenic.html">this': ['http://udacity.com/cs101x/urank/zinc.html'], 'best': ['http://udacity.com/cs101x/urank/nickel.html'], 'out': ['http://udacity.com/cs101x/urank/index.html'], 'Nickel': ['http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html'], 'expert': ['http://udacity.com/cs101x/urank/index.html'], 'everything': ['http://udacity.com/cs101x/urank/zinc.html'], '3': ['http://udacity.com/cs101x/urank/kathleen.html'], 'Hummus</a>': ['http://udacity.com/cs101x/urank/index.html'], '</body>': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'learned': ['http://udacity.com/cs101x/urank/zinc.html'], 'sauce.': ['http://udacity.com/cs101x/urank/kathleen.html'], 'This': ['http://udacity.com/cs101x/urank/nickel.html'], 'Chef</h1>': ['http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html'], 'Algorithms</h1>': ['http://udacity.com/cs101x/urank/index.html'], 'href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen\'s': ['http://udacity.com/cs101x/urank/index.html'], 'frosting': ['http://udacity.com/cs101x/urank/kathleen.html'], 'great': ['http://udacity.com/cs101x/urank/zinc.html'], 'Chef</a>.': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/arsenic.html'], 'favorite': ['http://udacity.com/cs101x/urank/index.html'], 'hummus': ['http://udacity.com/cs101x/urank/arsenic.html'], '</h1>': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'href="http://udacity.com/cs101x/urank/nickel.html">the': ['http://udacity.com/cs101x/urank/zinc.html'], '</ol>': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'Arsenic': ['http://udacity.com/cs101x/urank/arsenic.html'], 'Best': ['http://udacity.com/cs101x/urank/index.html'], 'lemon.': ['http://udacity.com/cs101x/urank/kathleen.html'], 'one': ['http://udacity.com/cs101x/urank/kathleen.html'], 'Add': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/kathleen.html'], '<h1>': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], '<li>': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'from': ['http://udacity.com/cs101x/urank/zinc.html'], 'her': ['http://udacity.com/cs101x/urank/arsenic.html'], "<h1>Dave's": ['http://udacity.com/cs101x/urank/index.html'], 'href="http://udacity.com/cs101x/urank/kathleen.html">': ['http://udacity.com/cs101x/urank/nickel.html'], 'recipies:': ['http://udacity.com/cs101x/urank/index.html'], '<h1>The': ['http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html'], 'href="http://udacity.com/cs101x/urank/arsenic.html">World\'s': ['http://udacity.com/cs101x/urank/index.html'], 'beans.': ['http://udacity.com/cs101x/urank/kathleen.html'], 'store': ['http://udacity.com/cs101x/urank/hummus.html'], 'more': ['http://udacity.com/cs101x/urank/index.html'], 'you.': ['http://udacity.com/cs101x/urank/arsenic.html'], 'href="http://udacity.com/cs101x/urank/hummus.html">Hummus': ['http://udacity.com/cs101x/urank/index.html'], 'buy': ['http://udacity.com/cs101x/urank/hummus.html'], 'Squeeze': ['http://udacity.com/cs101x/urank/kathleen.html'], 'Force': ['http://udacity.com/cs101x/urank/arsenic.html'], 'pepper,': ['http://udacity.com/cs101x/urank/kathleen.html'], 'can': ['http://udacity.com/cs101x/urank/kathleen.html'], 'Zinc': ['http://udacity.com/cs101x/urank/zinc.html'], 'of': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'Open': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'and': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'is': ['http://udacity.com/cs101x/urank/nickel.html'], 'Cooking': ['http://udacity.com/cs101x/urank/index.html'], 'Crush': ['http://udacity.com/cs101x/urank/kathleen.html'], 'container': ['http://udacity.com/cs101x/urank/hummus.html'], 'in': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/kathleen.html'], 'my': ['http://udacity.com/cs101x/urank/index.html'], 'check': ['http://udacity.com/cs101x/urank/index.html'], 'make': ['http://udacity.com/cs101x/urank/arsenic.html'], 'Famous': ['http://udacity.com/cs101x/urank/arsenic.html'], '<ul>': ['http://udacity.com/cs101x/urank/index.html'], 'salt,': ['http://udacity.com/cs101x/urank/kathleen.html'], "Chef's": ['http://udacity.com/cs101x/urank/arsenic.html'], 'I': ['http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/zinc.html'], "Kathleen's": ['http://udacity.com/cs101x/urank/kathleen.html'], '<ol>': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'taste.': ['http://udacity.com/cs101x/urank/kathleen.html'], 'href="http://udacity.com/cs101x/urank/nickel.html">Nickel': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/arsenic.html'], '<a': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/zinc.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/arsenic.html'], '</p>': ['http://udacity.com/cs101x/urank/zinc.html'], 'The': ['http://udacity.com/cs101x/urank/arsenic.html'], 'a': ['http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/kathleen.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'for': ['http://udacity.com/cs101x/urank/arsenic.html'], '</a>': ['http://udacity.com/cs101x/urank/nickel.html'], 'tahini': ['http://udacity.com/cs101x/urank/kathleen.html'], 'the': ['http://udacity.com/cs101x/urank/index.html', 'http://udacity.com/cs101x/urank/nickel.html', 'http://udacity.com/cs101x/urank/arsenic.html', 'http://udacity.com/cs101x/urank/hummus.html'], 'Kidnap': ['http://udacity.com/cs101x/urank/arsenic.html'], 'know': ['http://udacity.com/cs101x/urank/zinc.html']}
#print index
print lookup(index,ranks,'Recipe')




        
