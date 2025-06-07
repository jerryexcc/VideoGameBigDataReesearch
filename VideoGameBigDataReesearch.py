import pandas as pd
from bs4 import BeautifulSoup
import requests

output_csv = "re_vgsales.csv"

def get_score_from_ign(df: pd.DataFrame):
    """
    <span data-cy="review-score-hexagon-content-wrapper" class="hexagon-content-wrapper">
    <figcaption>10</figcaption>
    </span>
    """
    df["IGN"] = ""
    for idx, query in enumerate(df["query"]):
        print(f"{idx}. start: {query}")
        response = requests.get(f"https://www.ign.com/games/{query}", headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            score_tag = soup.find("span", class_="hexagon-content-wrapper")
            if score_tag and score_tag.find("figcaption"):
                score = score_tag.find("figcaption").text.strip()
                try:
                    df.at[idx, "IGN"] = float(score)
                except ValueError:
                    df.at[idx, "IGN"] = 0
            else:
                df.at[idx, "IGN"] = 0
        else:
            df.at[idx, "IGN"] = "ERR"
    return df

def saveToCsv(df: pd.DataFrame):
    df.to_csv(f"{df["Rank"].loc[0]}_{output_csv}", index=False)
    print(f"Data saved to {df["Rank"].loc[0]}_{output_csv}")

def main():
    df = pd.read_csv("dummy.csv")
    # df.describe()
    # df.info()
    df["query"] = df["Name"].str.lower()
    df["query"] = df["query"].str.replace(r"\s+", "-", regex=True)
    df["query"] = df["query"].str.replace("!", "")
    df["query"] = df["query"].str.replace(":", "-")
    df["query"] = df["query"].str.replace(": ", "-")
    df["query"] = df["query"].str.replace("'", "")
    df["query"] = df["query"].str.replace(".", "")
    df["query"] = df["query"].str.replace(r"-+", "-", regex=True)
    print(df["Rank"].loc[0])
    df = get_score_from_ign(df)
    saveToCsv(df)

if __name__ == "__main__":
    main()