Need a conda env (for example, 'composite') with: 
geojson
geopy
json
numpy
impactutils
mapio
cartopy
matplotlib


Link to Python dyfi libraries for aggregation:
(ignore if not using DYFI)
- clone dyfi4
- (in dyfi4 directory) pip install -r requirements.txt

conda activate composite

Need a link to all HDF files in './hdf/'

1. aggregateEvents
Scan all HDF files in the Atlas event directories and create a JSON file of the aggregated max mmis (highest mmi in each UTM block). Save each event to aggregated/EVID/aggregated_SPAN.json

2. createComposite
Scan all json files in aggregated/ and take the max value in each UTM block. Save to output/reviewed_allcells.json

3. mapComposite
Read reviewed_allcells.json and create JPG and PDF map.



