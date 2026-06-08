const API_URL = "http://127.0.0.1:8000";

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

    displayCandidate(data);

    loadCandidates();
}

function displayCandidate(data){

    let skillsHtml = "";

    data.skills.forEach(skill => {

        skillsHtml += `
            <span class="skill">
                ${skill}
            </span>
        `;
    });

    document.getElementById(
        "candidateInfo"
    ).innerHTML = `

        <p><strong>Name:</strong>
            ${data.name}
        </p>

        <p><strong>Email:</strong>
            ${data.email}
        </p>

        <p><strong>Phone:</strong>
            ${data.phone}
        </p>

        <div>
            ${skillsHtml}
        </div>
    `;
}

async function loadCandidates(){

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
                <td>${candidate.name}</td>
                <td>${candidate.email}</td>
                <td>${candidate.phone}</td>
            </tr>
        `;
    });
}

loadCandidates();