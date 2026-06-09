const API_URL = window.location.origin;

async function uploadResume() {

    const fileInput =
        document.getElementById("resumeFile");

    const file =
        fileInput.files[0];

    if (!file) {
        alert("Select a PDF first");
        return;
    }

    const formData =
        new FormData();

    formData.append("file", file);

    try {

        const response =
            await fetch(
                `${API_URL}/upload-resume`,
                {
                    method: "POST",
                    body: formData
                }
            );

        const data =
            await response.json();

        if (!response.ok) {
            alert(data.error || "Upload failed");
            return;
        }

        displayCandidate(data);

        loadCandidates();

    } catch (error) {

        console.error(error);

        alert(
            "Error uploading resume."
        );
    }
}

function displayCandidate(data) {

    let skillsHtml = "";

    if (data.skills) {

        data.skills.forEach(skill => {

            skillsHtml += `
                <span class="skill">
                    ${skill}
                </span>
            `;
        });
    }

    document.getElementById(
        "candidateInfo"
    ).innerHTML = `

        <p>
            <strong>Name:</strong>
            ${data.name || ""}
        </p>

        <p>
            <strong>Email:</strong>
            ${data.email || ""}
        </p>

        <p>
            <strong>Phone:</strong>
            ${data.phone || ""}
        </p>

        <div>
            ${skillsHtml}
        </div>
    `;
}

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
                </tr>
            `;
        });

    } catch (error) {

        console.error(error);

        console.log(
            "Unable to load candidates"
        );
    }
}

loadCandidates();