#!/usr/bin/env python

import webbrowser


class Video():
    def __init__(self, title, description, length):
        self.title = title
        self.description = description
        self.length = length


class Movie(Video):
    """
        Attributes
            title        (str): The title of the movie
            description  (str): A brief description of the movie's plot
            length       (int): The length of the movie in minutes
            artwork_path (str): A url to the artwork
            trailer_path (str): A url to the trailer

        Movie class derived from Video class.

        This class represents the basic attributes of a movie and provides the
        ability to display a movie's trailer in a webbrowser.
    """

    def __init__(self, title, description, length, artwork_path, trailer_path):
        # Initialise parent class
        Video.__init__(self, title, description, length)

        # Initialise class attributes
        self.artwork_path = artwork_path
        self.trailer_path = trailer_path

    def show_trailer(self):
        """
            Opens the movie trailer url in a webbrowser.
        """
        webbrowser.open(self.trailer_path)
