from opto.trace import node, bundle
from opto.trace.utils import contain, sum_feedback


# flat
x = node(1., trainable=True)
y = node(2.)
z = x**y + (x*x*x*x) + 0.5

assert len(z.parameter_dependencies) == 1
assert contain(z.parameter_dependencies, x)
assert not contain(z.parameter_dependencies, y)


### nested
x = node(1., trainable=True)
hidden_param = node(-15., trainable=True)

@bundle()
def inner_function(x):
    return x**2 + hidden_param

@bundle(traceable_code=True)
def outer_function(x):
    return inner_function(x) + 1 + hidden_param



output = outer_function(x)

assert len(output.parameter_dependencies) == 1
assert contain(output.parameter_dependencies, x)
assert not contain(output.parameter_dependencies, hidden_param)
assert len(output.expandable_dependencies) == 1
assert contain(output.expandable_dependencies, output)

print(x)

output.backward('feedback', visualize=True)  # top graph

g = sum_feedback([x])
fig = g.visualize()
fig

sg = g.expand(output)
assert len(sg.graph) == 6

for _, n in sg.graph:
    print(n)
    print('-----')

sg.visualize()


### nested (ony hidden params)
x = node(1.)
hidden_param = node(-15., trainable=True)

@bundle()
def inner_function(x):
    return x**2 + hidden_param

@bundle(traceable_code=True)
def outer_function(x):
    return inner_function(x) + 1 + hidden_param


output = outer_function(x)

assert len(output.parameter_dependencies) == 0
assert not contain(output.parameter_dependencies, hidden_param)
assert len(output.expandable_dependencies) == 1
assert contain(output.expandable_dependencies, output)

output.backward('feedback')  # top graph

tg = sum_feedback([hidden_param])
tg.visualize()  # this shows the top level graph
tg.expand(output).visualize()  # this shows the expanded graph
