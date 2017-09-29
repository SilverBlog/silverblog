def get_theme_list():
    import urllib.request
    console.log("info", "Get Theme List")
    r = "[]"
    try:
        r = urllib.request.urlopen("https://api.github.com/orgs/silverblogtheme/repos"").read().decode('utf-8')
    except urllib2.HTTPError:
        console.log("Error", "Get Theme List error")
        exit(1)
    req = json.loads(r)
