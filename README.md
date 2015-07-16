# Get_Sequence_API

These are [Araport](http://www.araport.org) API wrappers around the [Thalemine Sequence Access Endpoint](https://iodocs.araport.org/thalemine/docs#/ws-sequence) that returns a json of a sequence from the A. thaliana genome.

# get_sequence_by_coordinate: fetch by coordinate location
```
>>> import services.get_sequence_by_coordinate.main
>>> main.search({'chromosome':'Chr1', 'start':10, 'end':100})
{
  "start": 10, 
  "end": 100,
  "chromosome": "Chr1",
  "sequence": "gacgggaattgaacccgcgatggtgaattcacaatccactgccttaatccacttggctacatccgcccctacgctactatctattctttt"
}
```
The list function returns a list of chromosome ids and length.
```
>>> import services.get_sequence_by_coordinate.main
>>> main.list({})
{
  "length": 30427671, 
  "chromosome": "Chr1"
}
---
{
  "length": 19698289, 
  "chromosome": "Chr2"
}
---
{
  "length": 23459830, 
  "chromosome": "Chr3"
}
---
{
  "length": 18585056, 
  "chromosome": "Chr4"
}
---
{
  "length": 26975502, 
  "chromosome": "Chr5"
}
---
{
  "length": 154478, 
  "chromosome": "ChrC"
}
---
{
  "length": 366924, 
  "chromosome": "ChrM"
}
```

# get_sequence_by_identifier: fetch by gene locus
```
>>> import services.get_sequence_by_identifier.main
>>> main.search({'identifier': 'AT1G01210'})
{
  "start": 10, 
  "end": 100,
  "chromosome" : "Chr1",
  "sequence": "gacgggaattgaacccgcgatggtgaattcacaatccactgccttaatccacttggctacatccgcccctacgctactatctattctttt"
}
```
