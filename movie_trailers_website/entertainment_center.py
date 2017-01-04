#!/usr/bin/env python

from media import Movie
import fresh_tomatoes

# Creation of a list of movie objects utilising Movie class from media.
movies = [Movie("Pulp Fiction",
                    "Prizefighter Butch Coolidge has decided to stop payment "
                    "on a deal he is made with the devil. "
                    "Honey Bunny and Pumpkin are young lovers and small time "
                    "thieves who decide they need a change of "
                    "venue. Meanwhile, two career criminals, Vincent Vega and "
                    "Jules, go about their daily business of "
                    "shooting up other crooks that are late on payments to "
                    "their boss. While one is asked to baby sit "
                    "their boss dangerously pretty young wife, the other "
                    "suddenly realizes that he must give up his "
                    "life of crime.",
                    178,
                    "https://www.gstatic.com/tv/thumb/movieposters/15684/p15684_p_v8_ac.jpg",  # NOQA
                    "https://www.youtube.com/watch?v=s7EdQ4FqbhY"),
              Movie("Terminator 2: Judgment Day",
                    "In this sequel set eleven years after 'The Terminator,"
                    "' young John Connor (Edward Furlong), "
                    "the key to civilization's victory over a future robot "
                    "uprising, is the target of the "
                    "shape-shifting T-1000 (Robert Patrick), a Terminator "
                    "sent from the future to kill him. Another "
                    "Terminator, the revamped T-800 (Arnold Schwarzenegger), "
                    "has been sent back to protect the boy. "
                    "As John and his mother (Linda Hamilton) go on the run "
                    "with the T-800, the boy forms an "
                    "unexpected bond with the robot.",
                    154,
                    "https://t1.gstatic.com/images?q=tbn:ANd9GcS5J6Ay6y1UT7WAI4U7Zm2KDYITrvfOI3vmaCNdGhx_0jmWiI1d",  # NOQA
                    "https://www.youtube.com/watch?v=lwSysg9o7wE"),
              Movie("Good Will Hunting",
                    "Matt Damon, who created the title character and wrote "
                    "the script with costar Ben Affleck, "
                    "gives a star-making performance as a working class "
                    "genius with a chip on his shoulder.",
                    126,
                    "https://t0.gstatic.com/images?q=tbn:ANd9GcT4vHOLWBM56R6fNs7K9xcEf7V8M8mzrzi6LtWGXrqfg8-KynGn",  # NOQA
                    "https://www.youtube.com/watch?v=z02M3NRtkAA")]

# Call to the fresh tomatoes script to create the movie page HTML and inject
# python Movie objects.
fresh_tomatoes.open_movies_page(movies)
