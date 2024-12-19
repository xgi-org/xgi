# -*- coding: utf-8 -*-
"""
Creative Commons Legal Code

CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").

Certain owners wish to permanently relinquish those rights to a Work for
the purpose of contributing to a commons of creative, cultural and
scientific works ("Commons") that the public can reliably and without fear
of later claims of infringement build upon, modify, incorporate in other
works, reuse and redistribute as freely as possible in any form whatsoever
and for any purposes, including without limitation commercial purposes.
These owners may contribute to the Commons to promote the ideal of a free
culture and the further production of creative, cultural and scientific
works, or to gain reputation or greater distribution for their Work in
part through the use and efforts of others.

For these and/or other purposes and motivations, and without any
expectation of additional consideration or compensation, the person
associating CC0 with a Work (the "Affirmer"), to the extent that he or she
is an owner of Copyright and Related Rights in the Work, voluntarily
elects to apply CC0 to the Work and publicly distribute the Work under its
terms, with knowledge of his or her Copyright and Related Rights in the
Work and the meaning and intended legal effect of CC0 on those rights.

1. Copyright and Related Rights. A Work made available under CC0 may be
protected by copyright and related or neighboring rights ("Copyright and
Related Rights"). Copyright and Related Rights include, but are not
limited to, the following:

  i. the right to reproduce, adapt, distribute, perform, display,
     communicate, and translate a Work;
 ii. moral rights retained by the original author(s) and/or performer(s);
iii. publicity and privacy rights pertaining to a person's image or
     likeness depicted in a Work;
 iv. rights protecting against unfair competition in regards to a Work,
     subject to the limitations in paragraph 4(a), below;
  v. rights protecting the extraction, dissemination, use and reuse of data
     in a Work;
 vi. database rights (such as those arising under Directive 96/9/EC of the
     European Parliament and of the Council of 11 March 1996 on the legal
     protection of databases, and under any national implementation
     thereof, including any amended or successor version of such
     directive); and
vii. other similar, equivalent or corresponding rights throughout the
     world based on applicable law or treaty, and any national
     implementations thereof.

2. Waiver. To the greatest extent permitted by, but not in contravention
of, applicable law, Affirmer hereby overtly, fully, permanently,
irrevocably and unconditionally waives, abandons, and surrenders all of
Affirmer's Copyright and Related Rights and associated claims and causes
of action, whether now known or unknown (including existing as well as
future claims and causes of action), in the Work (i) in all territories
worldwide, (ii) for the maximum duration provided by applicable law or
treaty (including future time extensions), (iii) in any current or future
medium and for any number of copies, and (iv) for any purpose whatsoever,
including without limitation commercial, advertising or promotional
purposes (the "Waiver"). Affirmer makes the Waiver for the benefit of each
member of the public at large and to the detriment of Affirmer's heirs and
successors, fully intending that such Waiver shall not be subject to
revocation, rescission, cancellation, termination, or any other legal or
equitable action to disrupt the quiet enjoyment of the Work by the public
as contemplated by Affirmer's express Statement of Purpose.

3. Public License Fallback. Should any part of the Waiver for any reason
be judged legally invalid or ineffective under applicable law, then the
Waiver shall be preserved to the maximum extent permitted taking into
account Affirmer's express Statement of Purpose. In addition, to the
extent the Waiver is so judged Affirmer hereby grants to each affected
person a royalty-free, non transferable, non sublicensable, non exclusive,
irrevocable and unconditional license to exercise Affirmer's Copyright and
Related Rights in the Work (i) in all territories worldwide, (ii) for the
maximum duration provided by applicable law or treaty (including future
time extensions), (iii) in any current or future medium and for any number
of copies, and (iv) for any purpose whatsoever, including without
limitation commercial, advertising or promotional purposes (the
"License"). The License shall be deemed effective as of the date CC0 was
applied by Affirmer to the Work. Should any part of the License for any
reason be judged legally invalid or ineffective under applicable law, such
partial invalidity or ineffectiveness shall not invalidate the remainder
of the License, and in such case Affirmer hereby affirms that he or she
will not (i) exercise any of his or her remaining Copyright and Related
Rights in the Work or (ii) assert any associated claims and causes of
action with respect to the Work, in either case contrary to Affirmer's
express Statement of Purpose.

4. Limitations and Disclaimers.

 a. No trademark or patent rights held by Affirmer are waived, abandoned,
    surrendered, licensed or otherwise affected by this document.
 b. Affirmer offers the Work as-is and makes no representations or
    warranties of any kind concerning the Work, express, implied,
    statutory or otherwise, including without limitation warranties of
    title, merchantability, fitness for a particular purpose, non
    infringement, or the absence of latent or other defects, accuracy, or
    the present or absence of errors, whether or not discoverable, all to
    the greatest extent permissible under applicable law.
 c. Affirmer disclaims responsibility for clearing rights of other persons
    that may apply to the Work or any use thereof, including without
    limitation any person's Copyright and Related Rights in the Work.
    Further, Affirmer disclaims responsibility for obtaining any necessary
    consents, permissions or other rights required for any use of the
    Work.
 d. Affirmer understands and acknowledges that Creative Commons is not a
    party to this document and has no duty or obligation with respect to
    this CC0 or use of the Work.

Modified from https://github.com/cfpb/github-changelog

This is a script to determine which PRs have been merges since the last
release, or between two releases on the same branch.
"""
import argparse
import os
import re
from collections import namedtuple
from datetime import datetime, timedelta

import requests

DEFAULT_BRANCH = "main"
PUBLIC_GITHUB_URL = "https://github.com"
PUBLIC_GITHUB_API_URL = "https://api.github.com"
GitHubConfig = namedtuple("GitHubConfig", ["base_url", "api_url", "headers"])

Commit = namedtuple("Commit", ["sha", "message"])
PullRequest = namedtuple(
    "PullRequest", ["number", "title", "author", "closed_at", "associated_issues"]
)

# Merge commits use a double linebreak between the branch name and the title
MERGE_PR_RE = re.compile(r"^Merge pull request #([0-9]+)*")

# Squash-and-merge commits use the PR title with the number in parentheses
SQUASH_PR_RE = re.compile(r".*\(#([0-9]+)\)*")


class GitHubError(Exception):
    pass


def get_github_config(github_base_url, github_api_url, token):
    """Returns a GitHubConfig instance based on the given arguments"""
    if token is None:
        token = os.environ.get("GITHUB_API_TOKEN")

    headers = {}
    if token is not None:
        headers["Authorization"] = "token " + token

    return GitHubConfig(
        base_url=github_base_url, api_url=github_api_url, headers=headers
    )


def get_commit_for_tag(github_config, owner, repo, tag):
    """Get the commit sha for a given git tag"""
    tag_url = "/".join(
        [
            github_config.api_url,
            "repos",
            owner,
            repo,
            "git",
            "refs",
            "tags",
            tag,
        ]
    )
    tag_json = {}

    while "object" not in tag_json or tag_json["object"]["type"] != "commit":
        tag_response = requests.get(tag_url, headers=github_config.headers)
        tag_json = tag_response.json()

        if tag_response.status_code != 200:
            raise GitHubError(f"Unable to get tag {tag}. {tag_json["message"]}")

        # If we're given a tag object we have to look up the commit
        if tag_json["object"]["type"] == "tag":
            tag_url = tag_json["object"]["url"]

    return tag_json["object"]["sha"]


def get_last_commit(github_config, owner, repo, branch=DEFAULT_BRANCH):
    """Get the last commit sha for the given repo and branch"""
    commits_url = "/".join([github_config.api_url, "repos", owner, repo, "commits"])
    commits_response = requests.get(
        commits_url, params={"sha": branch}, headers=github_config.headers
    )
    commits_json = commits_response.json()
    if commits_response.status_code != 200:
        raise GitHubError(f"Unable to get commits. {commits_json["message"]}")

    return commits_json[0]["sha"]


def get_last_tag(github_config, owner, repo):
    """Get the last tag for the given repo"""
    tags_url = "/".join([github_config.api_url, "repos", owner, repo, "tags"])
    tags_response = requests.get(tags_url, headers=github_config.headers)
    tags_response.raise_for_status()
    tags_json = tags_response.json()
    return tags_json[0]["name"]


def get_commits_between(github_config, owner, repo, first_commit, last_commit):
    """Get a list of commits between two commits"""
    commits_url = "/".join(
        [
            github_config.api_url,
            "repos",
            owner,
            repo,
            "compare",
            first_commit + "..." + last_commit,
        ]
    )
    commits_response = requests.get(commits_url, headers=github_config.headers)
    commits_json = commits_response.json()
    if commits_response.status_code != 200:
        raise GitHubError(
            f"Unable to get commits between {first_commit} and {last_commit}. {commits_json["message"]}"
        )

    if "commits" not in commits_json:
        raise GitHubError(
            f"Commits not found between {first_commit} and {last_commit}."
        )

    commits = [
        Commit(c["sha"], c["commit"]["message"]) for c in commits_json["commits"]
    ]
    return commits


def is_pr(message):
    """Determine whether or not a commit message is a PR merge"""
    return MERGE_PR_RE.search(message) or SQUASH_PR_RE.search(message)


def extract_pr_number(message):
    """Given a PR merge commit message, extract the PR number and title"""
    merge_match = MERGE_PR_RE.match(message)
    squash_match = SQUASH_PR_RE.match(message)

    if merge_match is not None:
        numbers = merge_match.groups()
        return numbers[-1]
    elif squash_match is not None:
        numbers = squash_match.groups()

        return numbers[-1]  # PullRequest(number=number, title=title, author=author)

    raise Exception(f"Commit isn't a PR merge, {message}")


def prs_from_numbers(github_config, owner, repo, pr_numbers):
    pr_list = []
    for number in pr_numbers:
        pull_url = "/".join(
            [
                github_config.api_url,
                "repos",
                owner,
                repo,
                "pulls",
                number,
            ]
        )
        pull_response = requests.get(pull_url, headers=github_config.headers)
        pull_json = pull_response.json()
        title = pull_json["title"]
        author = pull_json["user"]["login"]
        closed_at = pull_json["closed_at"]
        pr_list.append(
            PullRequest(
                number=number,
                title=title,
                author=author,
                closed_at=closed_at,
                associated_issues=[],
            )
        )
    return pr_list


def get_associated_issues(github_config, owner, repo, prs):
    issues_url = "/".join(
        [
            github_config.api_url,
            "repos",
            owner,
            repo,
            "issues?state=closed",
        ]
    )
    issues_response = requests.get(issues_url, headers=github_config.headers)
    issues_json = issues_response.json()
    issues = {entry["number"]: entry["closed_at"] for entry in issues_json}
    for pr in prs:
        t_pr = datetime.fromisoformat(pr.closed_at)
        for i in issues:
            t_issue = datetime.fromisoformat(issues[i])
            if abs((t_issue - t_pr).total_seconds()) <= 2 and int(i) != int(pr.number):
                pr.associated_issues.append(i)


def fetch_changes(
    github_config,
    owner,
    repo,
    previous_tag=None,
    current_tag=None,
    branch=DEFAULT_BRANCH,
):
    if previous_tag is None:
        previous_tag = get_last_tag(github_config, owner, repo)
    previous_commit = get_commit_for_tag(github_config, owner, repo, previous_tag)

    current_commit = None
    if current_tag is not None:
        try:
            current_commit = get_commit_for_tag(github_config, owner, repo, current_tag)
        except GitHubError:
            # Try to proceed with the given "tag" as a commit sha
            current_commit = current_tag
    else:
        current_commit = get_last_commit(github_config, owner, repo, branch)

    commits_between = get_commits_between(
        github_config, owner, repo, previous_commit, current_commit
    )

    # Process the commit list looking for PR merges
    pr_numbers = [
        extract_pr_number(c.message) for c in commits_between if is_pr(c.message)
    ]

    if len(pr_numbers) == 0 and len(commits_between) > 0:
        raise Exception("Lots of commits and no PRs on branch {branch}")
    else:
        prs = prs_from_numbers(github_config, owner, repo, pr_numbers)

    prs.reverse()
    return prs


def format_changes(github_config, owner, repo, prs, markdown=True):
    """Format the list of prs in either text or markdown"""
    lines = []
    for pr in prs:
        pr_number = f"#{pr.number}"
        if markdown:
            pr_link = f"{github_config.base_url}/{owner}/{repo}/pull/{pr.number}"
            pr_number = f"[{pr_number}]({pr_link})"

        issues = pr.associated_issues

        if len(issues) == 0:
            issues_string = ""

        elif len(issues) == 1:
            issue_number = issues[0]
            issue_link = (
                f"{github_config.base_url}/{owner}/{repo}/issues/{issue_number}"
            )
            issues_string = f"(Closes Issue [#{issue_number}]({issue_link})) "

        elif len(issues) == 2:
            issue_number1, issue_number2 = issues
            issue_link1 = (
                f"{github_config.base_url}/{owner}/{repo}/issues/{issue_number1}"
            )
            issue_link2 = (
                f"{github_config.base_url}/{owner}/{repo}/issues/{issue_number2}"
            )
            issues_string = f"(Closes Issues [#{issue_number1}]({issue_link1}) and [#{issue_number2}]({issue_link2})) "
        else:
            issues_string = "(Closes Issues "
            for i, issue_number in enumerate(issues):
                issue_link = (
                    f"{github_config.base_url}/{owner}/{repo}/issues/{issue_number}"
                )

                if i < len(issues):
                    issues_string += f"[#{issue_number}]({issue_link}), "
                else:
                    issues_string += f"and [#{issue_number}]({issue_link})) "

        lines.append(f"* {pr.title}. {issues_string}{pr_number} (@{pr.author})")

    return lines


def generate_changelog(
    owner,
    repo,
    previous_tag=None,
    current_tag=None,
    markdown=True,
    single_line=False,
    branch=None,
    github_base_url=None,
    github_api_url=None,
    github_token=None,
):

    github_config = get_github_config(github_base_url, github_api_url, github_token)

    prs = fetch_changes(github_config, owner, repo, previous_tag, current_tag, branch)
    get_associated_issues(github_config, owner, repo, prs)
    lines = format_changes(github_config, owner, repo, prs, markdown=markdown)

    separator = "\\n" if single_line else "\n"
    return separator.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a CHANGELOG between two git tags based on GitHub"
        "Pull Request merge commit messages"
    )
    parser.add_argument("owner", metavar="OWNER", help="owner of the repo on GitHub")
    parser.add_argument("repo", metavar="REPO", help="name of the repo on GitHub")
    parser.add_argument(
        "previous_tag",
        metavar="PREVIOUS",
        nargs="?",
        help="previous release tag (defaults to last tag)",
    )
    parser.add_argument(
        "current_tag",
        metavar="CURRENT",
        nargs="?",
        help="current release tag (defaults to HEAD)",
    )
    parser.add_argument(
        "-m", "--markdown", action="store_true", help="output in markdown"
    )
    parser.add_argument(
        "-s",
        "--single-line",
        action="store_true",
        help="output as single line joined by \\n characters",
    )
    parser.add_argument(
        "--branch",
        type=str,
        action="store",
        default=DEFAULT_BRANCH,
        help="Override the " "target branch (defaults to main)",
    )
    parser.add_argument(
        "--github-base-url",
        type=str,
        action="store",
        default=PUBLIC_GITHUB_URL,
        help="Override if you "
        "are using GitHub Enterprise. e.g. https://github."
        "my-company.com",
    )
    parser.add_argument(
        "--github-api-url",
        type=str,
        action="store",
        default=PUBLIC_GITHUB_API_URL,
        help="Override if you "
        "are using GitHub Enterprise. e.g. https://github."
        "my-company.com/api/v3",
    )
    parser.add_argument(
        "--github-token",
        type=str,
        action="store",
        default=None,
        help="GitHub oauth token to auth " "your Github requests with",
    )

    args = parser.parse_args()

    changelog = generate_changelog(**vars(args))
    print(changelog)


if __name__ == "__main__":
    main()
