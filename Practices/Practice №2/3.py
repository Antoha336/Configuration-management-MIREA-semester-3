from graphviz import Digraph

# Для matplotlib
matplotlib_graph = Digraph(comment='Matplotlib Dependencies')
matplotlib_graph.attr(rankdir='LR')
matplotlib_graph.node('matplotlib', 'matplotlib', shape='box')

dependencies_matplotlib = [
    'numpy', 'cycler', 'kiwisolver', 'packaging', 'pyparsing', 'pillow', 'contourpy', 'fonttools'
]
for dep in dependencies_matplotlib:
    matplotlib_graph.node(dep, dep, shape='ellipse')
    matplotlib_graph.edge('matplotlib', dep)

# Для express
express_graph = Digraph(comment='Express Dependencies')
express_graph.attr(rankdir='LR')
express_graph.node('express', 'express', shape='box')

dependencies_express = [
    'accepts', 'body-parser', 'cookie', 'debug', 'finalhandler', 'array-flatten', 
    'content-disposition', 'http-errors', 'qs', 'etag', 'merge-descriptors', 'safe-buffer'
]
for dep in dependencies_express:
    express_graph.node(dep, dep, shape='ellipse')
    express_graph.edge('express', dep)

matplotlib_graph.render('matplotlib_dependencies', format='png')
express_graph.render('express_dependencies', format='png')
