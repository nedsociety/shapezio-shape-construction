import collections
import time
import marshal
import sys

possible_shapes = [None] * (2**16)
fringe = collections.deque()
fringe.append((1, ('base',)))

def get_layer(shape, layer):
    return (shape >> (4 * layer)) & 15

def rotator(shape):
    MASK0 = 0b0001000100010001
    MASK1 = 0b1110111011101110
    return ((shape & MASK0) << 3) | ((shape & MASK1) >> 1)

def scissor(shape):
    MASK = 0b0011001100110011
    shape &= MASK
    # compress empty layers
    if shape & 0b0000111100000000 == 0:
        shape = (shape & 0b0000000011111111) | ((shape & 0b1111000000000000) >> 4)
    if shape & 0b0000000011110000 == 0:
        shape = (shape & 0b0000000000001111) | ((shape & 0b1111111100000000) >> 4)
    if shape & 0b0000000000001111 == 0:
        shape >>= 4
    return shape

def stacker(shape0, shape1):
    while shape1 < 0b10000000000000000:
        if shape0 & shape1 == 0:
            return shape0 | shape1
        shape1 <<= 4
    return 0

def add_fringe(shape, method):
    if shape == 0:
        return
    if possible_shapes[shape] is not None:
        return
    fringe.append((shape, method))

def consider_new_shapes(shape):
    add_fringe(rotator(shape), ('rotator-cw', shape))
    add_fringe(scissor(shape), ('scissor-rhs', shape))

    # Stacker
    for other_shape, method in enumerate(possible_shapes):
        if method is None:
            continue
        add_fringe(stacker(shape, other_shape), ('stacker', shape, other_shape))
        add_fringe(stacker(other_shape, shape), ('stacker', other_shape, shape))

last_printed = time.time()
num_checked = 0
while fringe:
    curshape, method = fringe.popleft()
    if possible_shapes[curshape] is not None:
        continue

    possible_shapes[curshape] = method
    consider_new_shapes(curshape)

    num_checked += 1
    curtime = time.time()
    if curtime - last_printed > 1:
        print(f'Checked {num_checked} shapes, current #fringe: {len(fringe)}')
        last_printed = curtime

with open('possible_shapes.marshal', 'wb') as f:
    marshal.dump(possible_shapes, f)

print('Done.')
