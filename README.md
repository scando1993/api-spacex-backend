# Blue Onion Labs Take Home Test

Hey! We are stoked that you are interested in joining the team at Blue Onion Labs.

We have crafted the following test to see how you approach pulling and manipulating of data. We want to get a general idea of how you approach some common types of problems that we encounter here at Blue Onion (we are really proficient at integrations!)

## Background
[spacexdata.com](https://docs.spacexdata.com/) provides an API to query attributes about SpaceX launches (https://github.com/r-spacex/SpaceX-API/blob/master/docs/v4/README.md). For this exercise we are going to be working with two resources in particular:
- The [Starlink Schema](https://github.com/r-spacex/SpaceX-API/blob/master/docs/v4/starlink/schema.md)
  Some relevant fields to note in the reponse:
    - spaceTrack.creation_date
    - longitude
    - latitude

## The Problem:
We want to be able to import the SpaceX Satellite data, and then we want to find out which satellites are physically closest to a given point.

## The Task:

Create a script/application to import the API results for 'starlink' data into memory. Have the script accept the following arguments:
- latitude
- longitude
- an integer N

Return value: the first 'N' number of satellites which are *closest in physical distance* to the input latitude/longitude. We essentially want to be able to ingest the satellite data, then find out which one is closest to a given point at any given time.

Do not worry about going deep into the math of distances between points on the ground and space in terms of lat/lon. You can assume the satellite positions (in lat/lon) and the position we compare it to are at the same altitude. No need to be too exact with this one :)
You will find the following package useful here: https://github.com/mapado/haversine

*Bonus points*:
- Tests. Feel free to test what you think needs testing, and make a note of what you think doesn't need any testing (and why!)

### How to Submit

1. Run through it one last time to make sure it works!
2. Push up to your forked repo one last time (or save your working directory to a 'zip')
3. Reach out to us with your solution

### Questions

If you have any questions at all during the challenge do not hesitate to reach out! Whether it be a question about the requirements, submitting, anything, just send us a note!
