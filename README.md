# What is this?

These tiny, unpolished scripts will find shape construction methods for [shapez.io](https://shapez.io/).

# Why is it needed?

Most of the shapes required in the game is trivial to make - just create each layer then assemble them via Stackers.

This tool exists for assembling *nontrivial* shapes where the above strategy won't work. This happens when two adjacent layers share no common quadrants. In version 1.2.1 of the game there are only two of them to bother: [the Logo shape](https://viewer.shapez.io/?RuCw--Cw:----Ru--) and [the Rocket shape](https://viewer.shapez.io/?CbCuCbCu:Sr------:--CrSrCr:CwCwCwCw).

Note that for Freeplay shapes from Level 27 there's no need for this tool as they are all trivial.

# How to run?

There's no external dependencies so you might run each script with your default python3 distributions.

> **Optional:** Run `search-all-constructible-shapes.py`. This will build a file `possible_shapes.marshal` which contains the construction table for all possible shapes. This step is optional as the file is already provided in the repository. Note that using **PyPy** is recommended for this step. The code runs extensive, unoptimized graph search in pure python so PyPy works way faster than CPython -- speedup by an order of magnitude in my test run.
>
> ```
> $ docker run -it --rm --name shapezio-script -v $PWD:/usr/src/myapp -w /usr/src/myapp pypy:3 pypy3 search-all-constructible-shapes.py
> ```



To find how to build a specific shape, run `map-construction.py` with shape code as an argument. This example shows how to build the rocket shape:

```
$ python map-construction.py CbCuCbCu:Sr------:--CrSrCr:CwCwCwCw
Note: Individual fragment setup is not supported; shape has been changed to CuCuCuCu:Cu------:--CuCuCu:CuCuCuCu .

[CuCuCuCu:Cu------:--CuCuCu:CuCuCuCu] Stack ----CuCu:CuCuCuCu over CuCuCuCu:Cu------:--Cu----
  [CuCuCuCu:Cu------:--Cu----] Stack Cu------:--Cu---- over CuCuCuCu
    [Cu------:--Cu----] Scissor Cu--Cu--:--CuCu-- and then take RIGHT-hand shape
      [Cu--Cu--:--CuCu--] Stack --CuCu-- over Cu--Cu--
  [----CuCu:CuCuCuCu] Stack CuCuCu-- over ----CuCu:------Cu
    [----CuCu:------Cu] Stack ----Cu-- over ------Cu:------Cu
      [------Cu:------Cu] Stack ------Cu over ------Cu
```



To find shapes that are not constructible (like [this one](https://viewer.shapez.io/?------Cu:CuCuCu--)), run `show-inconstructible-shapes.py`:

```
$ python show-inconstructible-shapes.py > inconstructible_shapes.txt
```

There are 1516 shape configurations that cannot be constructed within the game. This number excludes the count of individual fragment setups (quadrant shapes and colors), mirrored and rotated duplicates.

# Note

This script works as of version 1.2.1 of the game, and the result might be invalidated as the game changes.