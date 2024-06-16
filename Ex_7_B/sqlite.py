import requests
import sqlite3

with open("poll.db", "wb") as file:
    response = requests.get(
        "https://github.com/erelsgl-at-ariel/research-5784/raw/main/06-python-databases/homework/poll.db")
    file.write(response.content)

db = sqlite3.connect("poll.db")


def net_support_for_candidate1(candidate1: str, candidate2: str) -> int:
    """
    Calculate the net support for candidate1 over candidate2.

    :param candidate1: The name of the first candidate.
    :param candidate2: The name of the second candidate.
    :return: The net support for candidate1 over candidate2.
    :raises ValueError: If one or both candidate names are not found in the database or if candidate1 is equal to candidate2.

    >>> net_support_for_candidate1('גדעון סער', 'יולי אדלשטיין')
    81

    >>> net_support_for_candidate1('ניר ברקת', 'בני גנץ')
    25

    >>> net_support_for_candidate1('בנימין נתניהו', 'נפתלי בנט')
    -77

    >>> net_support_for_candidate1('יאיר לפיד', 'יאיר לפיד')
    Traceback (most recent call last):
    ValueError: Candidate1 and Candidate2 must be different.

    >>> net_support_for_candidate1('מישהו|י אחר|ת', 'יאיר לפיד')
    -17

    >>> net_support_for_candidate1('יאיר לפיד', 'aa')
    Traceback (most recent call last):
    ValueError: One or both candidate names are not found in the database.
    """

    if candidate1 == candidate2:
        raise ValueError("Candidate1 and Candidate2 must be different.")

    # Retrieving the columns associated with the candidates from the database
    q6_candidate1_col = db.execute("SELECT Variable FROM codes_for_questions WHERE Label = ?", (candidate1,)).fetchone()
    q6_candidate2_col = db.execute("SELECT Variable FROM codes_for_questions WHERE Label = ?", (candidate2,)).fetchone()

    # Raise an exception if one or both candidate names are not found in the database
    if q6_candidate1_col is None or q6_candidate2_col is None:
        raise ValueError("One or both candidate names are not found in the database.")

    # Extract the column names
    q6_candidate1_col = q6_candidate1_col[0]
    q6_candidate2_col = q6_candidate2_col[0]

    # Query to calculate the net support for candidate1 over candidate2
    query = """
        SELECT (
            (SELECT COUNT(*) FROM list_of_answers WHERE {0} < {1}) - 
            (SELECT COUNT(*) FROM list_of_answers WHERE {0} > {1})
        ) AS difference
        """.format(q6_candidate1_col, q6_candidate2_col)

    # Executing the query and returning the result
    return db.execute(query).fetchone()[0]


def condorcet_winner() -> str:
    """
    Find the Condorcet winner among the candidates.

    :return: The name of the Condorcet winner, or "אין" if none is found.

    >>> condorcet_winner()
    'נפתלי בנט'
    """
    # Query to retrieve the candidate names from the database
    query = """
            SELECT Label
            FROM codes_for_questions
            WHERE Variable LIKE 'Q6%'
        """
    # Fetching all candidate names from the database
    candidates = db.execute(query).fetchall()

    # Iterating through each candidate to check for Condorcet winner
    for candidate in candidates:
        # Checking if the candidate is a Condorcet winner
        is_condorcet_winner = all(
            net_support_for_candidate1(candidate[0], other[0]) > 0 for other in candidates if other != candidate)
        # If the candidate is a Condorcet winner, return the candidate name
        if is_condorcet_winner:
            return candidate[0]

    # Return "אין" if no Condorcet winner is found
    return "אין"


if __name__ == '__main__':
    party = input()
    if party == "condorcet_winner":
        print(condorcet_winner())
    else:
        candidate1, candidate2 = party.split(",")
        print(net_support_for_candidate1(candidate1, candidate2))
