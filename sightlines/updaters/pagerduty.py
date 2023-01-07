from os import environ
from sightlines.cell import Cell
from pdpyras import APISession as PagerDutySession  # type: ignore


pagerduty = PagerDutySession(environ["PAGERDUTY_TOKEN"])


def get_incidents():
    return pagerduty.list_all(
        "incidents",
        params={
            "team_ids[]": [environ["PAGERDUTY_TEAM_ID"]],
        },
    )


def update_pagerduty(cells: list[Cell]):
    if len(cells) != 1:
        raise ValueError("PagerDuty updater expects exactly one cell.")

    cell = cells[0]
    unresolved_incidents = [i for i in get_incidents() if i["status"] != "resolved"]
    if len(unresolved_incidents) > 0:
        cell.set_rgb(127, 0, 0)
    else:
        cell.set_rgb(0, 127, 0)
