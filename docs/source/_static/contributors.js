// docs/_static/contributors.js

const CORE_TEAM = [
    "alpatania",
    "iaciac",
    "leotrs",
    "lordgrilo",
    "maximelucas",
    "nwlandry",
    "tlarock",
    "thomasrobiglio",
];

const CORE_TEAM_ALUMNI = [
    "acuschwarze",
    "mcontisc",
];


async function get_github_contributors() {
    const contributors = [];
    let page = 1;

    while (true) {
        const response = await fetch(
            `https://api.github.com/repos/xgi-org/xgi/contributors?per_page=100&page=${page}`
        );

        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status}`);
        }

        const results = await response.json();

        contributors.push(...results);

        if (results.length < 100) break;

        page++;
    }

    return contributors.filter(
        contributor =>
            contributor.login &&
            !contributor.login.endsWith("[bot]")
    );
}


function create_contributor(username, contributor = null) {
    const avatar = contributor
        ? contributor.avatar_url
        : `https://github.com/${username}.png`;

    const profile = contributor
        ? contributor.html_url
        : `https://github.com/${username}`;

    const tile = document.createElement("div");
    tile.className = "contributor-tile";

    const img = document.createElement("img");
    img.src = avatar;
    img.alt = `${username}'s GitHub avatar`;
    img.width = 50;
    img.height = 50;

    const link = document.createElement("a");
    link.href = profile;
    link.textContent = `@${username}`;
    link.target = "_blank";
    link.rel = "noopener noreferrer";

    tile.appendChild(img);
    tile.appendChild(link);

    return tile;
}


async function display_contributors() {
    const container = document.getElementById("github-contributors");

    if (!container) {
        console.error("Contributor container not found.");
        return;
    }

    // Add styling.
    const style = document.createElement("style");
    style.textContent = `
        .contributor-grid {
            display: grid;
            grid-template-columns: repeat(
                auto-fill,
                minmax(180px, 1fr)
            );
            gap: 12px;
            margin: 15px 0 30px 0;
        }

        .contributor-tile {
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 0;
        }

        .contributor-tile img {
            border-radius: 50%;
            flex-shrink: 0;
            object-fit: cover;
        }

        .contributor-tile a {
            overflow-wrap: anywhere;
        }
    `;
    document.head.appendChild(style);

    try {
        const contributors = await get_github_contributors();

        const contributor_map = new Map(
            contributors.map(c => [c.login, c])
        );

        // Add core team and alumni even if absent from the API.
        [...CORE_TEAM, ...CORE_TEAM_ALUMNI].forEach(username => {
            if (!contributor_map.has(username)) {
                contributor_map.set(username, null);
            }
        });

        const community = contributors
            .map(c => c.login)
            .filter(username =>
                !CORE_TEAM.includes(username) &&
                !CORE_TEAM_ALUMNI.includes(username)
            );

        const groups = [
            ["Core team", CORE_TEAM],
            ["Core team alumni", CORE_TEAM_ALUMNI],
            ["Contributors", community],
        ];

        for (const [title, usernames] of groups) {
            const heading = document.createElement("h3");
            heading.textContent = title;
            container.appendChild(heading);

            const grid = document.createElement("div");
            grid.className = "contributor-grid";

            usernames
                .sort((a, b) => a.localeCompare(b))
                .forEach(username => {
                    grid.appendChild(
                        create_contributor(
                            username,
                            contributor_map.get(username)
                        )
                    );
                });

            container.appendChild(grid);
        }
    } catch (error) {
        console.error("Could not load GitHub contributors:", error);
        container.textContent =
            "Unable to load contributors from GitHub. Please try again later.";
    }
}