const API_URL = window.location.origin;

// ======================
// LOAD CANDIDATES
// ======================

async function loadCandidates() {

    try {

        const response =
            await fetch(
                `${API_URL}/candidates`
            );

        const data =
            await response.json();

        const tbody =
            document.querySelector(
                "#candidateTable tbody"
            );

        tbody.innerHTML = "";

        data.forEach(candidate => {

            tbody.innerHTML += `
                <tr>
                    <td>${candidate.id}</td>
                    <td>${candidate.name || ""}</td>
                    <td>${candidate.email || ""}</td>
                    <td>${candidate.phone || ""}</td>
                    <td>${candidate.skills || ""}</td>
                    <td>${candidate.ats_score || 0}%</td>
                </tr>
            `;
        });

    } catch (error) {

        console.error(error);

        alert(
            "Unable to load candidates"
        );
    }
}

// ======================
// BULK UPLOAD
// ======================

async function uploadBulkResume() {

    const files =
        document.getElementById(
            "resumeFiles"
        ).files;

    if (files.length === 0) {

        alert(
            "Select PDFs first"
        );

        return;
    }

    const formData =
        new FormData();

    for (let file of files) {

        formData.append(
            "files",
            file
        );
    }

    try {

        const response =
            await fetch(
                `${API_URL}/upload-bulk`,
                {
                    method: "POST",
                    body: formData
                }
            );

        const data =
            await response.json();

        console.log(data);

        alert(
            "Upload completed"
        );

        loadCandidates();

    } catch (error) {

        console.error(error);

        alert(
            "Upload failed"
        );
    }
}

// ======================
// SEARCH
// ======================

async function searchCandidates() {

    const skill =
        document.getElementById(
            "skillSearch"
        ).value;

    if (!skill) {

        loadCandidates();
        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/search?skill=${encodeURIComponent(skill)}`
            );

        const data =
            await response.json();

        const tbody =
            document.querySelector(
                "#candidateTable tbody"
            );

        tbody.innerHTML = "";

        data.forEach(candidate => {

            tbody.innerHTML += `
                <tr>
                    <td>${candidate.id}</td>
                    <td>${candidate.name || ""}</td>
                    <td>${candidate.email || ""}</td>
                    <td>${candidate.phone || ""}</td>
                    <td>${candidate.skills || ""}</td>
                    <td>${candidate.ats_score || 0}%</td>
                </tr>
            `;
        });

    } catch (error) {

        console.error(error);
    }
}

// ======================
// ATS RANKING
// ======================

async function rankCandidates() {

    const jobDescription =
        document.getElementById(
            "jobDescription"
        ).value;

    if (!jobDescription) {

        alert(
            "Paste Job Description"
        );

        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/rank-candidates`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({
                        job_description:
                        jobDescription
                    })
                }
            );

        const data =
            await response.json();

        const tbody =
            document.querySelector(
                "#rankingTable tbody"
            );

        tbody.innerHTML = "";

        data.rankings.forEach(
            candidate => {

            tbody.innerHTML += `
                <tr>
                    <td>${candidate.candidate_id}</td>
                    <td>${candidate.name}</td>
                    <td>${candidate.email}</td>
                    <td>${candidate.score}%</td>
                    <td>${candidate.matched_skills.join(", ")}</td>
                </tr>
            `;
        });

        loadCandidates();

    } catch (error) {

        console.error(error);

        alert(
            "Ranking failed"
        );
    }
}

// ======================
// EXPORT CSV
// ======================

function exportCSV() {

    window.open(
        `${API_URL}/export-csv`,
        "_blank"
    );
}

loadCandidates();