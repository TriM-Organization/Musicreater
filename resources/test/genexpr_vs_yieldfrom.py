
# 模拟两种写法
def method_A(self, start, end):
    yield from (f"{track}.get_range(start, end)" for track in self)

def method_B(self, start, end):
    return (f"{track}.get_range(start, end)" for track in self)



tracks = ["A", "B"]

gen_a = method_A(tracks, 0, 10)
print(list(gen_a))



gen_b = method_B(tracks, 0, 10)
print(list(gen_b))

# they are the same output
