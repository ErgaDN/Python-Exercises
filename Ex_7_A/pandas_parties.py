import pandas as pd

codes_for_questions = pd.read_csv(
    "https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/codes_for_questions.csv")
codes_for_answers = pd.read_csv(
    "https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/codes_for_answers.csv")
list_of_answers = pd.read_csv(
    "https://raw.githubusercontent.com/erelsgl-at-ariel/research-5784/main/06-python-databases/homework/list_of_answers.csv")


def support_in_one_party_elections(party: str) -> int:
    """
    Calculate the number of supporters for a given party in one-party elections.

    :param party: The name of the party.

    :return: The number of supporters for the party.
    :raises ValueError: If the party code is not found.

    >>> support_in_one_party_elections('ודעם')
    21

    >>> support_in_one_party_elections('יז')
    3

    >>> support_in_one_party_elections('שס')
    13

    >>> support_in_one_party_elections('aaa')
    Traceback (most recent call last):
    ValueError: Party code aaa not found.
    """

    # Filter party code for the given party
    party_code_value = codes_for_answers[(codes_for_answers['Value'] == 'Q2') &
                                         (codes_for_answers['Label'].str.startswith(party))]

    # If party code not found, return appropriate message
    if party_code_value.empty:
        raise ValueError(f"Party code {party} not found.")

    # Extract party code
    code = party_code_value['Code'].values[0]

    # Count number of supporters for the party
    num_supporters = list_of_answers[list_of_answers['Q2'] == code].shape[0]
    return num_supporters


def support_in_multi_party_elections(party: str) -> int:
    """
    Calculate the number of supporters for a given party in multi-party elections.

    :param party: The name of the party.

    :return: The number of supporters for the party.
    :raises ValueError: If the party code is not found.

    >>> support_in_multi_party_elections('ודעם')
    27

    >>> support_in_multi_party_elections('יז')
    32

    >>> support_in_multi_party_elections('שס')
    39

    >>> support_in_multi_party_elections('aaa')
    Traceback (most recent call last):
    ValueError: Party code aaa not found.

    """
    # Filter party code for the given party
    party_code = codes_for_questions[(codes_for_questions['Variable'].str.startswith('Q3')) &
                                     (codes_for_questions['Label'].str.startswith(party))]

    # If party code not found, return appropriate message
    if party_code.empty:
        raise ValueError(f"Party code {party} not found.")

    # Extract questions code
    questions_code = party_code['Variable'].values[0]

    # Count number of supporters for the party
    num_supporters = list_of_answers[list_of_answers[questions_code] == 1].shape[0]

    return num_supporters


def parties_with_different_relative_order() -> tuple:
    """
    Find parties with different relative order of support in one-party and multi-party elections.

    :return: A tuple containing the parties with different relative order, if found. Otherwise, None.

    >>> parties_with_different_relative_order()
    ('אמת', 'כן')

    """
    # Extract party names from Q2 parties
    q2_parties = codes_for_answers[codes_for_answers['Value'] == 'Q2']
    party_names = q2_parties['Label'].apply(lambda x: x.split(' ')[0] if ' - ' in x else None).dropna().unique()

    # Calculate support for each party in one-party elections
    current_support_dict = {party: support_in_one_party_elections(party) for party in party_names}

    # Sort parties by support in one-party elections
    sorted_current_support_dict = dict(sorted(current_support_dict.items(), key=lambda item: item[1], reverse=True))

    # Calculate support for each party in multi-party elections
    multi_support_dict = {party: support_in_multi_party_elections(party) for party in party_names}

    # Sort parties by support in multi-party elections
    sorted_multi_support_dict = dict(sorted(multi_support_dict.items(), key=lambda item: item[1], reverse=True))

    # Compare the order of parties in both dictionaries
    for key1, key2 in zip(sorted_current_support_dict.keys(), sorted_multi_support_dict.keys()):
        if key1 != key2:
            return (key1, key2)

    return None


if __name__ == '__main__':
    party = input()
    if party == "parties_with_different_relative_order":
        print(parties_with_different_relative_order())
    else:
        print(support_in_one_party_elections(party), support_in_multi_party_elections(party))
