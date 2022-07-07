import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# can only run after data has been prepared for arcgis only, as rm_sales_data.csv
def main():
    # load in sales data
    rm_sales_data = pd.read_csv('rm_sales_data.csv')

    fig, ax = plt.subplots()

    # visualize the relationship price and bedrooms
    sns.boxplot(x="Number of bedrooms", y="Price", palette="pastel", data=rm_sales_data, ax=ax, showfliers = False)

    # change the limits of X-axis
    ax.set_xlim(-2, 12)
    plt.show()

if __name__ == "__main__":
    main()
