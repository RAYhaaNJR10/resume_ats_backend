const API_URL = window.location.origin;

// ======================================
// PAGE NAVIGATION
// ======================================

function showPage(pageId, button) {

    document
        .querySelectorAll(".page-section")
        .forEach(section => {
            section.style.display = "none";
        });

    document
        .querySelectorAll(".nav-btn")
        .forEach(btn => {
            btn.classList.remove("active");
        });

    document.getElementById(pageId).style.display = "block";

    if (button) {
        button.classList.add("active");
    }

    if (pageId === "candidates-page") {
    loadCandidates();
}

if (pageId === "search-page") {

    const tbody =
        document.querySelector(
            "#searchTable tbody"
        );

    if (tbody) {
        tbody.innerHTML = "";
    }

    const searchBox =
        document.getElementById(
            "skillSearch"
        );

    if (searchBox) {
        searchBox.value = "";
    }
}
}

// ======================================
// STATUS BOX
// ======================================

function updateStatus(
    message,
    type = ""
) {

    const box =
        document.getElementById(
            "statusBox"
        );

    if (!box) return;

    box.textContent = message;

    box.className =
        "status-box";

    if (type) {

        box.classList.add(
            type
        );
    }
}

// ======================================
// CREATE SKILL CELL
// ======================================

function createSkillsHTML(skills) {

    if (!skills) return "";

    const skillsArray =
        skills
            .split(",")
            .map(skill => skill.trim())
            .filter(skill => skill);

    return skillsArray
        .map(skill =>
            `<span class="skill-tag">${skill}</span>`
        )
        .join("");
}

// ======================================
// LOAD ALL CANDIDATES
// ======================================

async function loadCandidates() {

    try {

        updateStatus(
            "Loading candidates..."
        );

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

        if (!tbody) return;

        tbody.innerHTML = "";

        data.forEach(candidate => {

            tbody.innerHTML += `
                <tr>

                    <td>${candidate.id || ""}</td>

                    <td>${candidate.filename || ""}</td>

                    <td>${candidate.name || ""}</td>

                    <td>${candidate.email || ""}</td>

                    <td>${candidate.phone || ""}</td>

                    <td>${candidate.education || ""}</td>

                    <td>${candidate.experience || ""}</td>

                    <td>
                        ${
                            candidate.linkedin
                            ?
                            `<a href="${candidate.linkedin}" target="_blank">
                                Open
                            </a>`
                            :
                            ""
                        }
                    </td>

                    <td>
                        ${
                            candidate.github
                            ?
                            `<a href="${candidate.github}" target="_blank">
                                Open
                            </a>`
                            :
                            ""
                        }
                    </td>

                    <td>${candidate.projects || ""}</td>

                    <td>${candidate.certifications || ""}</td>

                    <td class="skills-cell">
                        ${createSkillsHTML(candidate.skills)}
                    </td>

                    <td>
                        ${candidate.ats_score || 0}%
                    </td>

                </tr>
            `;
        });

        updateStatus(
            `${data.length} candidates loaded`,
            "status-success"
        );

    } catch (error) {

        console.error(error);

        updateStatus(
            "Failed to load candidates",
            "status-error"
        );
    }
}

// ======================================
// BULK RESUME UPLOAD
// ======================================

async function uploadBulkResume() {

    const files =
        document.getElementById(
            "resumeFiles"
        ).files;

    if (files.length === 0) {

        alert(
            "Please select PDF files."
        );

        return;
    }

    updateStatus(
        `Uploading ${files.length} resume(s)...`
    );

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

        let successCount = 0;
        let duplicateCount = 0;
        let failedCount = 0;

        data.forEach(item => {

            if (
                item.status ===
                "success"
            ) {
                successCount++;
            }

            else if (
                item.status ===
                "duplicate"
            ) {
                duplicateCount++;
            }

            else {
                failedCount++;
            }
        });

        updateStatus(
            `Completed: ${successCount} added, ${duplicateCount} duplicate, ${failedCount} failed`,
            "status-success"
        );

        loadCandidates();

    } catch (error) {

        console.error(error);

        updateStatus(
            "Upload failed",
            "status-error"
        );
    }
}

// ======================================
// SEARCH CANDIDATES
// ======================================

async function searchCandidates() {

    const skill =
        document.getElementById(
            "skillSearch"
        ).value.trim();

    if (!skill) {

        alert(
            "Enter a skill to search."
        );

        return;
    }

    try {

        updateStatus(
            `Searching "${skill}"...`
        );

        const response =
            await fetch(
                `${API_URL}/search?skill=${encodeURIComponent(skill)}`
            );

        const data =
            await response.json();

        const tbody =
            document.querySelector(
                "#searchTable tbody"
            );

        if (!tbody) return;

        tbody.innerHTML = "";

        data.forEach(candidate => {

            tbody.innerHTML += `
                <tr>

                    <td>${candidate.id || ""}</td>

                    <td>${candidate.filename || ""}</td>

                    <td>${candidate.name || ""}</td>

                    <td>${candidate.email || ""}</td>

                    <td>${candidate.phone || ""}</td>

                    <td>${candidate.education || ""}</td>

                    <td>${candidate.experience || ""}</td>

                    <td></td>

                    <td></td>

                    <td></td>

                    <td></td>

                    <td class="skills-cell">
                        ${createSkillsHTML(candidate.skills)}
                    </td>

                    <td>
                        ${candidate.ats_score || 0}%
                    </td>

                </tr>
            `;
        });

        updateStatus(
            `${data.length} result(s) found`,
            "status-success"
        );

    } catch (error) {

        console.error(error);

        updateStatus(
            "Search failed",
            "status-error"
        );
    }
}

// ======================================
// ATS RANKING
// ======================================

async function rankCandidates() {

    const jd =
        document.getElementById(
            "jobDescription"
        ).value.trim();

    if (!jd) {

        alert(
            "Paste a Job Description."
        );

        return;
    }

    try {

        updateStatus(
            "Extracting JD skills using AI..."
        );

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
                        job_description: jd
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

                        <td>
                            ${candidate.candidate_id}
                        </td>

                        <td>
                            ${candidate.name}
                        </td>

                        <td>
                            ${candidate.email}
                        </td>

                        <td>
                            ${candidate.score}%
                        </td>

                        <td class="skills-cell">
                            ${candidate.matched_skills.join(", ")}
                        </td>

                    </tr>
                `;
            });

        updateStatus(
            `Ranking completed for ${data.rankings.length} candidate(s)`,
            "status-success"
        );

    } catch (error) {

        console.error(error);

        updateStatus(
            "Ranking failed",
            "status-error"
        );
    }
}

// ======================================
// EXPORT CSV
// ======================================

function exportCSV() {

    updateStatus(
        "Preparing CSV export..."
    );

    window.open(
        `${API_URL}/export-csv`,
        "_blank"
    );

    setTimeout(() => {

        updateStatus(
            "CSV exported",
            "status-success"
        );

    }, 1000);
}

// ======================================
// INITIAL LOAD
// ======================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadCandidates();
    }
);