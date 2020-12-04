import marshal
import sys
import re

with open('possible_shapes.marshal', 'rb') as f:
    possible_shapes = marshal.load(f)

def get_layer(shape, layer):
    return (shape >> (4 * layer)) & 15

def strshape(shape):
    s = ':'.join('{:04b}'.format(layer)[::-1] for layer in (get_layer(shape, i) for i in range(4)) if layer != 0)
    s = s.replace('1', 'Cu')
    s = s.replace('0', '--')
    return s

def numshape(shapestr):
    SHAPEFRAG = r'(?:[CRWS][rgbypcuw])'
    FRAG = f'({SHAPEFRAG}|(?:--))'
    RE = f'({FRAG}{FRAG}{FRAG}{FRAG}:){{0,3}}{FRAG}{FRAG}{FRAG}{FRAG}'
    if re.fullmatch(RE, shapestr) is None:
        raise ValueError('Invalid shape code')
    new_shapestr = re.sub(SHAPEFRAG, 'Cu', shapestr)
    if new_shapestr != shapestr:
        print(f'Note: Individual fragment setup is not supported; shape has been changed to {new_shapestr} .')
        print()
    new_shapestr = new_shapestr.replace('--', '0')
    new_shapestr = new_shapestr.replace('Cu', '1')
    new_shapestr = new_shapestr.replace(':', '')
    new_shapestr = new_shapestr[::-1]
    return int(new_shapestr, base=2)

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} SHAPECODE')
    sys.exit(0)

shape = numshape(sys.argv[1])
def traverse(shape, level):
    method = possible_shapes[shape]
    if method is None:
        print('cannot be constructed')
    elif method[0] == 'base':
        return
    elif (shape & 15) == shape:
        return

    print('  ' * level + f'[{strshape(shape)}] ', end='')
    if method[0] == 'rotator-cw':
        _, shape0 = method
        
        method0 = possible_shapes[shape0]
        if method0[0] == 'rotator-cw':
            _, shape00 = method0

            method00 = possible_shapes[shape00]
            if method00[0] == 'rotator-cw':
                _, shape000 = method00
                print(f'Rotate (CCW) {strshape(shape000)}')
                traverse(shape000, level + 1)
            else:
                print(f'Rotate (180 degree) {strshape(shape00)}')
                traverse(shape00, level + 1)
        else:
            print(f'Rotate (CW) {strshape(shape0)}')
            traverse(shape0, level + 1)
    elif method[0] == 'scissor-rhs':
        _, shape0 = method
        
        print(f'Scissor {strshape(shape0)} and then take RIGHT-hand shape')
        traverse(shape0, level + 1)
    elif method[0] == 'stacker':
        _, shape0, shape1 = method
        print(f'Stack {strshape(shape1)} over {strshape(shape0)}')
        traverse(shape0, level + 1)
        traverse(shape1, level + 1)

traverse(shape, 0)
