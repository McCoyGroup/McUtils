# <a id="McUtils.GaussianInterface">McUtils.GaussianInterface</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/__init__.py#L1?message=Update%20Docs)]
</div>
    
A module for making use of the results of calculations run by the Gaussian electronic structure package.
We'd like to be able to also support the NWChem and Psi4 packages, but haven't had the time, yet, to write it out.

Two main avenues of support are provided:

1. importing Gaussian results
2. setting up Gaussian jobs

The first is likely to be more useful to you, but we're hoping to be able to hook (2.) into the `Psience.Molecools` package.
The goal there is to provide automated support for setting up scans of molecular vibrations & the like.

There are already direct hooks into (1.) in `Psience.Data` through the `DipoleSurface` and `PotentialSurface` objects.
These are still in the prototype stage, but hopefully will allow us to unify strands of our Gaussian support,
and also make it easy to unify support for Psi4 and NWChem data, once we have the basic interface down.







## Examples

## FChk Parsing

Gaussian `.fchk` files have a set structure which looks roughly like
```lang-none
key    data_type     data_size
 data
```
This allows us to provide a complete parser for any `key`.
The actual parser is a subclass of `[Parsers.FileStreamReader]`(../Parsers/) called `GaussianFchkReader`.

The syntax to parse is straightforward

```python
target_keys = {"Current cartesian coordinates", "Numerical dipole derivatives"}
with GaussianFchkReader("/path/to/output.log") as parser:
    res = parser.parse(target_keys)
```

and to access properties you will pull them from the dict, `res`

```python
my_coords = res["Current cartesian coordinates"]
```


## Log Parsing

Gaussian `.log` files are totally unstructured (and a bit of a disaster). 
This means we need to write custom parsing logic for every field we might want.
The basic supported formats are defined in `GaussianLogComponents.py`. 
The actual parser is a subclass of [`Parsers.FileStreamReader`](../Parsers/) called `GaussianLogReader`.

The syntax to parse is straightforward

```python
target_keys = {"StandardCartesianCoordinates", "DipoleMoments"}
with GaussianLogReader("/path/to/output.log") as parser:
    res = parser.parse(target_keys)
```

and to access properties you will pull them from the dict, `res`

```python
my_coords = res["StandardCartesianCoordinates"]
```

### Adding New Parsing Fields

New parse fields can be added by registering a property on `GaussianLogComponents`. 
Each field is defined as a dict like

```python
GaussianLogComponents["Name"] = {
    "description" : string, # used for docmenting what we have
    "tag_start"   : start_tag, # starting delimeter for a block
    "tag_end"     : end_tag, # ending delimiter for a block None means apply the parser upon tag_start
    "parser"      : parser, # function that'll parse the returned list of blocks (for "List") or block (for "Single")
    "mode"        : mode # "List" or "Single"
}
```

The `mode` argument specifies whether all blocks should be matched first and send to the `parser` (`"List"`) or if they should be fed in one-by-one `"Single"`.
This often provides a tradeoff between parsing efficiency and memory efficiency.

The `parser` can be any function, but commonly is built off of a [`Parsers.StringParser`](../Parsers/). 
See the documentation for `StringParser` for more.

You can add to `GaussianLogComponents` at runtime.
Not all changes need to be integrated directly into the file.
{: .alert .alert-info}

#### Creating Parsers

As a concrete example, for a simple property the coordinates, there is a series of blocks each of which looks like

```lang-none                 
 ---------------------------------------------------------------------
 Center     Atomic      Atomic             Coordinates (Angstroms)
 Number     Number       Type             X           Y           Z
 ---------------------------------------------------------------------
      1          8           0        0.000000    0.000000    0.000000
      2          1           0        0.000000    0.000000    0.565929
      3          1           0        0.549420    0.000000   -0.135695
 ---------------------------------------------------------------------
```

and the corresponding `StringParser` looks like

You don't need to use a `StringParser`.  
It can just be convenient for declaring complicated patterns in a way that can be
parsed efficiently.
{: .alert .alert-info}


```python
header_pattern = Named(
    Repeating(
        Capturing(PositiveInteger),
        min=3, max=3,
        prefix=Optional(Whitespace),
        suffix=Whitespace
    ),
    "GaussianStuff", handler=StringParser.array_handler(dtype=int)
)
coords_pattern = Named(
    Repeating(
        Capturing(Number),
        min=3,
        max=3,
        prefix=Optional(Whitespace),
        joiner=Whitespace
    ),
    "Coordinates", handler=StringParser.array_handler(dtype=float)
)
CartParser = StringParser(
    Repeating((header_pattern, coords_pattern), suffix=Optional(Newline))
)
```

There's quite a bit going on here, but each bit is straightforward. 

First off, we note that in the data we actually want, Gaussian puts three ints before each `x y z` triple.
We capture this by the `header_pattern`, which is given the name `"GaussianStuff"` and 
which declares a set of exactly three repeating positive integers that we want to capture in the output, 
joined and ended by whitespace.
We want to then take these and save them as an array of ints (the `handler` field)

Second, we have a named `"Coordinates"` block which is identical to the `header_pattern` except 
we capture plain `Numbers` (i.e. positive or negative floats) and save the results as an array of floats.

Then we string these two patterns together in a repeating block joined by newlines.

Next, we need to tell the system how to identify these blocks.
To do so we need a start and end tag.

For that, we declare the patterns

```python
cart_delim = """ --------------------------------------------------------------"""
cartesian_start_tag = FileStreamerTag(
    """Center     Atomic      Atomic             Coordinates (Angstroms)""",
    follow_ups=cart_delim
)
cartesian_end_tag = cart_delim
```

The `cartesian_start_tag` tells the code where to start looking. It first finds the line

```lang-none
Center     Atomic      Atomic             Coordinates (Angstroms)
```

and then follows that up by looking for `cart_delim`, as specified by `follow_ups`.

Finally, we declare the actual parser function we'll use which will take the list of identified blocks
and apply the `StringParser` we defined like so

```python
def cartesian_coordinates_parser(strs):
    strss = "\n\n".join(strs)

    parse = CartParser.parse_all(strss)

    coords = (
        parse["GaussianStuff", 0],
        parse["Coordinates"].array
    )

    return coords
```

where this returns each array of coordinates and the first match of the `GaussianStuff` (we assume they're all the same).

A regular function that uses `string.split` and friends would have worked here too.
It would have just been a little bit more involved. 
A regex would also work, and is what `StringPattern` uses under the hood.
{: .alert .alert-info}

Finally, we register the parser as

```python
GaussianLogComponents["CartesianCoordinates"] = {
    "tag_start": cartesian_start_tag,
    "tag_end"  : cartesian_end_tag,
    "parser"   : cartesian_coordinates_parser,
    "mode"     : "List"
}
```

There are few different coordinate orientations that Gaussian uses, and we get the different orientations by matching
different tags.
For instance, we get the Z-matrix oriented coordinates like so

```python
GaussianLogComponents["ZMatCartesianCoordinates"] = {
    "tag_start": FileStreamerTag('''Z-Matrix orientation:''', follow_ups = (cart_delim, cart_delim)),
    "tag_end"  : cartesian_end_tag,
    "parser"   : cartesian_coordinates_parser,
    "mode"     : "List"
}
```

where the reader now initially looks for the tag `Z-Matrix orientation:` and then skips over the delimiters twice.

#### Dealing with Optimizations

We can use the same type of trick to deal with parameters coming from optimizations.
For instance, to get the dipole moments from a relaxed scan, we do the following

```python
tag_start  = " Dipole        ="
tag_end    = " Optimization"


def convert_D_number(a, **kw):
    import numpy as np
    return np.array([float(s.replace("D", "E")) for s in a])
DNumberPattern = RegexPattern((Number, "D", Integer), dtype=float)
OptimizedDipolesParser = StringParser(
    RegexPattern(
        (
            "Dipole", "=",
            Repeating(
                Capturing(DNumberPattern, handler=convert_D_number),
                min=3,
                max=3,
                suffix=Optional(Whitespace)
            )
        ),
        joiner=Whitespace
    )
)

def parser(mom):
    """Parses dipole block, but only saves the dipole of the optimized structure"""
    import numpy as np

    mom = "Dipole  =" + mom
    # print(">>>>>", mom)
    grps = OptimizedDipolesParser.parse_iter(mom)
    match = None
    for match in grps:
        pass

    if match is None:
        return np.array([])
    return match.value.array
    # else:
    #     grp = match.value
    #     dip_list = [x.replace("D", "E") for x in grp]
    #     dip_array = np.asarray(dip_list)
    #     return dip_array.astype("float64")

mode       = "List"
parse_mode = "Single"

GaussianLogComponents["OptimizedDipoleMoments"] = {
    "tag_start" : tag_start,
    "tag_end"   : tag_end,
    "parser"    : parser,
    "mode"      : mode,
    "parse_mode": parse_mode
}
```

The `StringParser` is not much more sophisticated than the one for the Cartesian coordinates, with the caveat that
we need to convert `D` to `E` to allow python to recognize the floats. 
The conversion could have been made more efficient, but it is perhaps edifying to see what a simplistic `handler` looks like.

The `tag_start` simply looks for a mention of `Dipole` and the `tag_end` looks for the `Optimization` tag.
This will identify the block between when the dipole moment is first printed and the optimization completes.
As the dipole moment is expected to be printed multiple times in this block, we then need to skip to the
final time the dipole moment is printed and only use that value.

We handle this in the `parser` function by first adding the `tag_start` back onto the matched string
and then using `OptimizedDipolesParser.parse_iter` to create an iterator that allows us to loop over the
blocks that match the pattern declared above.  We do nothing for all of these matches, just exhausting the iterator.

Once the iterator has been run dry, the value of `match` is the final match found by the `OptimizedDipolesParser`.
If no matches were found, the value of `match` defaults to `None` and we do nothing.

Finally, we allow the `match` to actually parse out the dipole moment by accessing its `value` attribute, and
then we return the `array` from that which contains the matched dipole moment.

## GJF Setup

Support is also provided for the automatic generation of Gaussian job files (`.gjf`) through the `GaussianJob` class.






---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/GaussianInterface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/GaussianInterface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/GaussianInterface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/GaussianInterface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/__init__.py#L1?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>