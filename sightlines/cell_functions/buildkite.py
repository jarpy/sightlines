import requests
import webbrowser
from dateutil.parser import isoparse
from itertools import chain
from os import environ
from textwrap import dedent
from time import time
from sightlines.cell import Cell
from typing import Sequence

api_token = environ["BUILDKITE_API_TOKEN_SIGHTLINES"]
graphql_url = "https://graphql.buildkite.com/v1"
http_headers = {"Authorization": f"Bearer {api_token}"}


def get_builds_by_pipeline_slug(organization: str, tag: str):
    # fmt: off
    query = dedent("""
    query {
      organization(slug: "%s") {
        pipelines(first: 100, tags: ["%s"]) {
          edges {
            node {
              slug
              url
              builds(first: 20, state: [CREATING, SCHEDULED, RUNNING, CANCELING, NOT_RUN, BLOCKED]) {
                edges {
                  node {
                    url
                    state
                    createdAt
                    scheduledAt
                    jobs(first: 50) {
                      edges {
                        node {
                          ... on JobTypeCommand {
                            state
                            scheduledAt
                            runnableAt
                            url
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """ % (organization, tag))
    # fmt: on

    response = requests.post(
        graphql_url,
        headers=http_headers,
        json={"query": query},
    )

    edges = response.json()["data"]["organization"]["pipelines"]["edges"]
    builds_by_pipeline_slug = {}
    for edge in edges:
        slug = edge["node"]["slug"]
        builds = [b["node"] for b in edge["node"]["builds"]["edges"]]
        for build in builds:
            if "jobs" in build:
                build["jobs"] = [j["node"] for j in build["jobs"]["edges"]]
        builds_by_pipeline_slug[slug] = builds
    return builds_by_pipeline_slug


def pipeline_cells(cells: Sequence[Cell]):
    """Update cells with the status of Buildkite pipelines."""

    # Paint the whole area under our control grey. This shows the operator where
    # to expect information. It also serves to indicate problems. If no data is
    # coming in, you'll just see a big grey blob.
    for cell in cells:
        cell.set_rgb(10, 10, 10)

    # Fill up the cells with colourful goodness. One cell per pipeline.
    builds = get_builds_by_pipeline_slug(
        environ["BUILDKITE_ORGANIZATION"], environ["BUILDKITE_TAG"]
    )
    cell_number = 0
    for pipeline, builds in builds.items():
        if len(builds) == 0:
            continue

        running_builds = [build for build in builds if build["state"] == "RUNNING"]
        jobs = chain(*[job for job in [build["jobs"] for build in running_builds]])
        scheduled_jobs = [
            job for job in jobs if "state" in job and job["state"] == "SCHEDULED"
        ]
        runnable_jobs = [job for job in scheduled_jobs if job["runnableAt"] is not None]

        # The thing we are most concerned about is when jobs are ready to run,
        # but don't get assigned an agent to run on.
        longest_wait = 0.0
        for job in runnable_jobs:
            wait_time = time() - isoparse(job["runnableAt"]).timestamp()
            longest_wait = max(longest_wait, wait_time)

        # Make a decision about the color to show for this pipeline.
        #
        # Jobs that are stalled waiting for an agent are the most interesting.
        if longest_wait > 300:
            cells[cell_number].set_rgb(80, 127, 0)

        # "Blocked" builds are also interesting. They usually need operator
        # intervention (often by design, but people forget to click the "go"
        # button.
        elif any(build["state"] == "BLOCKED" for build in builds):
            cells[cell_number].set_rgb(40, 0, 40)

        # It's nice to see builds that are running happily, too.
        elif any(build["state"] == "RUNNING" for build in builds):
            cells[cell_number].set_rgb(0, 127, 127)

        # If none of the states we have defined so far apply, set the cell black
        # to indicate that we don't know what to do, and that someone should come
        # here and write an implementation. :)
        else:
            cells[cell_number].set_rgb(0, 0, 0)

        cells[cell_number].set_datum("url", builds[0]["url"])
        cells[cell_number].set_on_press(
            lambda cell: webbrowser.open(cell.get_datum("url"))
        )

        cell_number += 1
        if cell_number > len(cells):
            # We don't have enough cells to fit all the pipelines with live builds.
            break
