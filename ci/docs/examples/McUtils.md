
We will provide a brief examples for the common use cases for each module.
More information can be found on the pages themselves.
The unit tests for each package are provided on the bottom of the package page.
These provide useful usage examples.

## Parsers

The `Parsers` package provides a toolkit for easily parsing string data out of files.
Here we'll get every key-value pair matching the pattern `key = value` from a Gaussian `.log` file

<div class="card in-out-block" markdown="1" id="Markdown_code">

```python
test_data = os.path.join(os.path.dirname(McUtils.__file__), 'ci', 'tests', 'TestData')
with open(os.path.join(test_data, 'water_OH_scan.log')) as log_dat:
    sample_data = log_dat.read()

key_value_matcher = RegexPattern([Named(Word, "key"), "=", Named(Word, "value")])
key_vals = StringParser(key_value_matcher).parse_all(sample_data)
key_vals['key'].array
```

<div class="card-body out-block" markdown="1">

```python
array(['0', 'Input', 'Output', ..., 'State', 'RMSD', 'PG'], dtype='<U7')
```

</div>
</div>

It's used extensively in the `GaussianInterface` package.

## Plots

A layer on `matplotlib` to provide more declarative syntax and easier composability.
Here we'll make a styled `GraphicsGrid`

<div class="card in-out-block" markdown="1">

```python
grid = np.linspace(0, 2 * np.pi, 100)
grid_2D = np.meshgrid(grid, grid)
x = grid_2D[1]
y = grid_2D[0]

main = GraphicsGrid(ncols=3, nrows=1, theme='Solarize_Light2', figure_label='my beuatufil triptych',
                            padding=((35, 60), (35, 40)), subimage_size=300)
main[0, 0] = ContourPlot(x, y, np.sin(y), plot_label='$sin(x)$',
                         axes_labels=[None, "cats (cc)"],
                         figure=main[0, 0]
                         )
main[0, 1] = ContourPlot(x, y, np.sin(x) * np.cos(y),
                         plot_label='$sin(x)cos(y)$',
                         axes_labels=[Styled("dogs (arb.)", {'color': 'red'}), None],
                         figure=main[0, 1])
main[0, 2] = ContourPlot(x, y, np.cos(y), plot_label='$cos(y)$', figure=main[0, 2])
main.colorbar = {"graphics": main[0, 1].graphics}
```

<div class="card-body out-block" markdown="1">

![plot](/McUtils/img/McUtils_GraphicsGrid_1.png)
</div>
</div>

## Data

Provides access to relevant atomic/units data pulled from NIST databases.

Pull the record for deuterium

<div class="card in-out-block" markdown="1">

```python
AtomData["D"]
```

<div class="card-body out-block" markdown="1">

```python
DataRecord('D', AtomDataHandler('AtomData', file='None'))
```

</div>
</div>

Grab the isotopically correct atomic mass

<div class="card in-out-block" markdown="1">

```python
AtomData["D", "Mass"]
```

<div class="card-body out-block" markdown="1">

```python
2.01410177812
```

</div>
</div>

Get all possible keys

<div class="card in-out-block" markdown="1">

```python
AtomData["D"].keys()
```

<div class="card-body out-block" markdown="1">

```python
dict_keys(['Name', 'Symbol', 'Mass', 'Number', 'MassNumber', 'IsotopeFraction', 'CanonicalName', 'CanonicalSymbol', 'ElementName', 'ElementSymbol', 'IconColor', 'IconRadius', 'PrimaryIsotope', 'StandardAtomicWeights'])
```

</div>
</div>

Get the conversion from Hartrees to wavenumbers

<div class="card in-out-block" markdown="1">

```python
UnitsData.convert("Hartrees", "Wavenumbers")
```

<div class="card-body out-block" markdown="1">

```python
219474.6313632
```

</div>
</div>

This conversion is not in the underlying database but is computed implicitly.
Another example

<div class="card in-out-block" markdown="1">

```python
UnitsData.data[("AtomicMassUnits", "Wavenumbers")]
```

<div class="card-body out-block" markdown="1">

```lang-none
KeyError: ('AtomicMassUnits', 'Wavenumbers')
```

</div>
</div>

<div class="card in-out-block" markdown="1">

```python
UnitsData.convert("AtomicMassUnits", "Wavenumbers")
```

<div class="card-body out-block" markdown="1">

```python
7513006610400.0
```

</div>
</div>

<div class="card in-out-block" markdown="1">

```python
UnitsData.data[("AtomicMassUnits", "Hartrees")]
```

<div class="card-body out-block" markdown="1">

```python
{'Value': 34231776.874,
 'Uncertainty': 0.01,
 'Conversion': ('AtomicMassUnits', 'Hartrees')}
```

</div>
</div>

## Coordinerds

Provides utilities for writing coordinate conversions and obtaining Jacobians between coordinate systems.
First we make a set of Cartesian coordinates

<div class="card in-out-block" markdown="1">

```python
struct = [
            [ 0.0,                    0.0,                   0.0                ],
            [ 0.5312106220949451,     0.0,                   0.0                ],
            [ 5.4908987527698905e-2,  0.5746865893353914,    0.0                ],
            [-6.188515885294378e-2,  -2.4189926062338385e-2, 0.4721688095375285 ],
            [ 1.53308938205413e-2,    0.3833690190410768,    0.23086294551212294],
            [ 0.1310095622893345,     0.30435650497612,      0.5316931774973834 ]
        ]
coords = CoordinateSet(struct)
```

<div class="card-body out-block" markdown="1">

```lang-none
CoordinateSet([[ 0.        ,  0.        ,  0.        ],
               [ 0.53121062,  0.        ,  0.        ],
               [ 0.05490899,  0.57468659,  0.        ],
               [-0.06188516, -0.02418993,  0.47216881],
               [ 0.01533089,  0.38336902,  0.23086295],
               [ 0.13100956,  0.3043565 ,  0.53169318]])
```

</div>
</div>

then convert that to Z-matrix coordinates

<div class="card in-out-block" markdown="1">

```python
icrds = coords.convert(ZMatrixCoordinates)
```

<div class="card-body out-block" markdown="1">

```lang-none
CoordinateSet([[ 0.53121062,  0.        ,  0.        ],
               [ 0.74641002,  0.878738  ,  0.        ],
               [ 0.77151626,  1.04598737, -0.7854913 ],
               [ 0.47989075,  0.13178784, -2.07064742],
               [ 0.3318484 ,  0.92484778,  2.60361273]])
```

</div>
</div>

we can also get the Jacobian for the transformation

<div class="card in-out-block" markdown="1">

```python
icrds = coords.convert(ZMatrixCoordinates)
```

<div class="card-body out-block" markdown="1">

```lang-none
array([[[[ -1.        ,   0.        ,   0.        ],
         [  0.        ,  -0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ]],

        [[  0.        ,   0.        ,   0.        ],
         [  0.        ,  -1.88249248,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ]],

        ...

        [[  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.61200111,   0.45926084,  -1.05894329],
         [  0.502835  ,  -0.77583777,  -0.70022831],
         [  0.        ,  -1.57576683,  -0.82116186]]],


       ...

        [[  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [ -0.23809822,   2.66405562,   1.5176851 ]],

        [[  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.        ,   0.        ,   0.        ],
         [  0.9065291 ,   0.16172563,   1.58012353]]]])
```

</div>
</div>

## Zachary


