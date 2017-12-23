# Extract Business Location

## Function

This program reads the `business.json` file from the Yelp dataset and produces a list of business IDs by metropolitan area. These IDs can be used to identify the location of reviews and other data from the Yelp Dataset.

## How to run ex_loc

the command to run `ex_loc` is:

`./ex_loc.sh business_json_file areas_file output_directory`  

where `business_jsaon_file`, `areas_file`, and `output_directory` are the locations of those files.

To run `ex_loc`, a file defining the areas to be observed must be included. These areas should follow the format of the file `AREAS` and must contain a minimum and maximum value for latitude and longitude of the area. The code for `ex_loc` currently generates additional files based on the major metropolitan areas for the 10th round of the Yelp Dataset Challenge. If a new `AREAS` file is used, the `02_ACC` files will be invalid, but all others will be accurate.

## Output

| File name | Data | Format |
| --------- | ---- | ------ |
| 01\_QUAD\_**_xx_** | All data points within the corresponding quadrant of the globe (NE, SE, SW, NW)| Latitude, Longitude |
| 02\_ACC\_**_xx_** | All data points that have been accepted as part of an area. These files correspond to continents (North America, Europe, South America) | Business ID, Longitude, Latitude |
| 03\_DUPLICATES | All data points that appear in more than one metropolitan area. | Latitude, Longitude |
| 03\_OUTLIER | All data points that fall outside of any metropolitan area. | Latitude, Longitude |
| __*NAME\_OF\_AREA*__ | All data points that fall within the labeled metropolitan area as selected and see in README.md. All data points follow a header with the area name. | Area_name, \n, Latitude, Longitude | 
