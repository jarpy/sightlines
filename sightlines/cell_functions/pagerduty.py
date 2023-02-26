import webbrowser
from os import environ
from sightlines.cell import Cell
from pdpyras import APISession as PagerDutySession  # type: ignore
from typing import Sequence

pagerduty = PagerDutySession(environ["PAGERDUTY_TOKEN"])
team_id = environ["PAGERDUTY_TEAM_ID"]
organization = environ["PAGERDUTY_ORGANIZATION"]


def get_incidents():
    return pagerduty.list_all(
        "incidents",
        params={
            "team_ids[]": [team_id],
        },
    )


def pagerduty_cells(cells: Sequence[Cell]):
    """A cell function that displays PagerDuty incident status.

    Note that only one status is displayed, so it's really only worth assigning
    this function to a single cell. However, the function signature still takes
    a list of cells, so that it satisfies the cell function API.
    """
    unresolved_incidents = [i for i in get_incidents() if i["status"] != "resolved"]
    for cell in cells:
        if len(unresolved_incidents) > 0:
            cell.set_rgb(127, 0, 0)
        else:
            cell.set_rgb(0, 127, 0)
        cell.set_on_press(
            lambda cell: webbrowser.open(
                f"https://{organization}.pagerduty.com/incidents"
            )
        )
