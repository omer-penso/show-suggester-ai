import pandas as pd
from data_loader import load_csv_file, load_tv_show_names_from_csv


def test_load_csv_file():
    csv_content = """Title,Description,Genres
Game of Thrones,"A fantasy drama.","Action, Adventure, Drama"
Breaking Bad,"A high school teacher turned meth producer.","Crime, Drama, Thriller"
"""
    with open("mock_tv_shows.csv", "w") as f:
        f.write(csv_content)

    df = load_csv_file("mock_tv_shows.csv")
    assert isinstance(df, pd.DataFrame)
    assert list(df["Title"]) == ["Game of Thrones", "Breaking Bad"]
    assert "Description" in df.columns


def test_load_tv_show_names_from_csv():
    csv_content = """Title,Description,Genres
Game of Thrones,"A fantasy drama.","Action, Adventure, Drama"
Breaking Bad,"A high school teacher turned meth producer.","Crime, Drama, Thriller"
"""
    with open("mock_tv_shows.csv", "w") as f:
        f.write(csv_content)

    
    tv_show_names = load_tv_show_names_from_csv("mock_tv_shows.csv")
    assert isinstance(tv_show_names, list)
    assert tv_show_names == ["Game of Thrones", "Breaking Bad"]
