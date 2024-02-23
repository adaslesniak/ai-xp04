import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_dataset(test_name):
    plt.figure()
    plt.title("Click to add points for dataset. Right-click to stop.")
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    points = plt.ginput(n=-1, timeout=0, show_clicks=True, mouse_add=1, mouse_stop=3)
    plt.close()
    print('got points, thank you')

    # Convert points to a DataFrame and save to CSV
    df = pd.DataFrame(points, columns=['X', 'Y'])
    df.to_csv(f'{test_name}_dataset.csv', index=False)
    print('data saved, thank you')


create_dataset('kmeans')