"""Start RockLan.

    py main.py          normal mode (progress saved to data/profile.json)
    py main.py --demo   show rocks at 0/33/66/100% without saving anything
"""
import argparse

from rocklan.app import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RockLan language progress tracker")
    parser.add_argument("--demo", action="store_true", help="show sample rocks, don't save")
    run(demo=parser.parse_args().demo)
