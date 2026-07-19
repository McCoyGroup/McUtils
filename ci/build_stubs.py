
import os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target = os.path.join(root, "ci", "stubs")
sys.path.insert(0, root)
os.chdir(root)

if __name__ == "__main__":
    from McUtils.Docs import *
    StubSummaryBuilder(verbose=True).generate_all("McUtils")