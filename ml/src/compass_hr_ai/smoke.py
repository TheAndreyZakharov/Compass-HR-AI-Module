def main() -> None:
    import numpy as np
    import pandas as pd

    df = pd.DataFrame({"a": [1, 2, 3]})
    x = np.array([1, 2, 3])

    print("OK: pandas rows =", len(df))
    print("OK: numpy sum =", int(x.sum()))

if __name__ == "__main__":
    main()
