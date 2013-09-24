# OkMirror

As it was the day it was shut down...

For those unfamiliar, OkMirror was a webapp that allowed users of OkCupid to view their hidden attractiveness rating. It managed this through clever use of match search queries; the search-by-attractiveness feature is represented as a range between 0 and 10000, and by manipulating these values you're able to do a sort of binary search that gives you ~156 points of accuracy in just five or six requests.

OkCupid had lots of underlying issues with search and, as a result, OkMirror had lots of trouble with finding certain usernames. The old version of OkMirror (written in php) tried to rectify this by getting users who's names wouldn't work to input more information and using it to create a more specific query. This usually worked, occasionally didn't. I imagine extracting data from the user's page (say, using the scraping logic from OkCreeper) to make a more specific query could be automated, but I never got around to implementing anything like that.