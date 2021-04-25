import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-b", "--bb", help="bbb", action="store_true"
)
parser.add_argument(
    "-a", "--aa", help="aaa", action="store_true"
)
parser.add_argument(
    "-c", "--cc", help="ccc"
)
parser.add_argument(
    "-d", "--dd", help="ddd", type=int
)
parser.add_argument(
    "-e", help="eee", type=int, choices=[1, 2, 3]
)
parser.add_argument(
    "-f", help="fff"
)
parser.add_argument(
    "-g", help="ggg", choices=["a", "b", "c"]
)
parser.add_argument(
    "var", help="var"
)
args = parser.parse_args()

if args.aa:
    print("aa turned on")
if args.bb:
    print("bb turned on")

print(args)
