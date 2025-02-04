import typing

"""
All the GraphQL queries for Rosie
"""

from codiga.graphql.common import do_graphql_query


def get_rulesets_name_string(ruleset_names: typing.List[str]):
    """
    Converts a List[str] into a string for graphql requests
    :param ruleset_names: List[str]
    :return: str
    """
    return "[\"" + ("\", \"".join(ruleset_names)) + "\"]"


def graphql_get_rulesets(api_token: str, ruleset_names: typing.List[str]):
    """
    Get rulesets by their names

    :param api_token: the API token to access the GraphQL API
    :param ruleset_names: the names of all rulesets to fetch
    """
    if not ruleset_names or not api_token:
        raise ValueError

    ruleset_names_string = get_rulesets_name_string(ruleset_names)
    query = """
        {
            ruleSetsForClient(names: """ + ruleset_names_string + """){
            id
            name
            rules(howmany: 10000, skip: 0){
              id
              name
              content
              language
              ruleType
              pattern
              patternMultiline
              elementChecked
            }
          }
        }"""
    data = do_graphql_query(api_token, {"query": query})
    if 'ruleSetsForClient' in data:
        return data['ruleSetsForClient']
    return None


def graphql_get_file_analysis(api_token: str, file_analysis_id: int):
    """
    Get the file analysis object with violations

    :param api_token: the API token to access the GraphQL API
    :param file_analysis_id: the identifier of the file analysis to get
    :return: the file analysis object and it's violations
    """
    if not file_analysis_id:
        raise ValueError

    query = """
    {
      getFileAnalysis(id:""" + str(file_analysis_id) + """){
        status
        filename
        language
        runningTimeSeconds
        timestamp
        violations {
          id
          language
          description
          severity
          category
          line
          lineCount
          tool
          rule
          ruleUrl
        }
      }
    }
    """
    return do_graphql_query(api_token, {"query": query})
