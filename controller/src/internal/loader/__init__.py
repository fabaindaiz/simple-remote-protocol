import os
from internal.base import Singleton

class Loader(Singleton):
    @Singleton.init
    def __init__(self):

        loader = os.getenv("LOADER", "ROOT+USER")
        from internal.loader import main
        main()

    