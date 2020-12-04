import marshal

with open('possible_shapes.marshal', 'rb') as f:
    possible_shapes = marshal.load(f)

def get_layer(shape, layer):
    return (shape >> (4 * layer)) & 15

def rotator(shape):
    MASK0 = 0b0001000100010001
    MASK1 = 0b1110111011101110
    return ((shape & MASK0) << 3) | ((shape & MASK1) >> 1)

def mirror(shape):
    MASK0 = 0b0001000100010001
    MASK1 = 0b0010001000100010
    MASK2 = 0b0100010001000100
    MASK3 = 0b1000100010001000
    return (
        ((shape & MASK0) << 3)
        | ((shape & MASK1) << 1)
        | ((shape & MASK2) >> 1)
        | ((shape & MASK3) >> 3)
    )

def strshape(shape):
    s = ':'.join('{:04b}'.format(layer)[::-1] for layer in (get_layer(shape, i) for i in range(4)) if layer != 0)
    s = s.replace('1', 'Cu')
    s = s.replace('0', '--')
    return s

def equivalent_variants(shape):
    variants = set()
    variants.add(shape)

    r = shape
    for _ in range(3):
        r = rotator(r)
        variants.add(r)
    
    for rshape in list(variants):
        variants.add(mirror(rshape))
    
    return variants

nontrivial_inconstructible_shapes = set()
for shape, method in enumerate(possible_shapes):
    if method is not None:
        continue
    
    # Skip trivial case where empty layer exists in-between
    nonempty_layer_indices = [i for i, layer in enumerate(get_layer(shape, i) for i in range(4)) if layer != 0]
    if len(nonempty_layer_indices) == 0:
        continue
    if nonempty_layer_indices[-1] != len(nonempty_layer_indices) - 1:
        continue
    
    # Skip if its equivalent shapes (rotation, mirror) are already present
    variants = equivalent_variants(shape)
    if any((variant in nontrivial_inconstructible_shapes) for variant in variants):
        continue

    nontrivial_inconstructible_shapes.add(shape)

for shape in sorted(nontrivial_inconstructible_shapes):
    print(strshape(shape))
