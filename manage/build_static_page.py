from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('SmartBlog', 'templates'))
template = env.get_template('index.html')
