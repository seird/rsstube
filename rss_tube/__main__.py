def main():
    import sys

    if "--version" in sys.argv:
        from rss_tube.__version__ import __version__
        print(__version__)
    else:
        from rss_tube.gui import start_gui
        start_gui()


if __name__ == "__main__":
    main()
