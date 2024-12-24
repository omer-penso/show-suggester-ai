from unittest.mock import patch
from user_input import validate_user_input, match_user_shows


def test_match_user_shows():
    tv_show_titles = ["Game Of Thrones", "Lupin", "The Witcher"]
    user_shows = ["gem of throns", "lupan", "witcher"]
    expected_matches = ["Game Of Thrones", "Lupin", "The Witcher"]
    assert match_user_shows(user_shows, tv_show_titles) == expected_matches


def test_validate_user_input():
    tv_show_titles = ["Game Of Thrones", "Lupin", "The Witcher"]
    user_input = "ame Of thrones; lupin; The Witsher"
    with patch("builtins.input", side_effect=[user_input, "y"]):
        assert validate_user_input(tv_show_titles) == ["Game Of Thrones", "Lupin", "The Witcher"]
