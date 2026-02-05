const path = progressData.path || [];
const completed = progressData.completed || [];
const hoursData = progressData.hours || {};
const recommendations = progressData.recommendations || [];
const linksData = progressData.links || {};

const container = document.getElementById("skillsContainer");

let completedCount = 0;
let remainingHours = 0;

path.forEach(skill => {
    const card = document.createElement("div");
    card.className = "skill-card";

    if (completed.includes(skill)) {
        completedCount++;
        card.innerHTML = `
            <h3>${skill}</h3>
            <p>Status: Completed</p>
        `;
    } else {
        remainingHours += hoursData[skill] || 0;

        card.innerHTML = `<h3>${skill}</h3>
                         <p>Status: Pending</p>
                         <p>Estimated: ${hoursData[skill] || 0} hrs</p>
                         <a href="${linksData[skill]}" target="_blank">
                         <button>Start Course</button>
                        </a>
                        <br><br>
    <a href="/complete/${skill}">
        <button>Mark Completed</button>
    </a>
`;

    }

    container.appendChild(card);
});

// Progress %
let percent = 0;
if (path.length > 0) {
    percent = Math.round((completedCount / path.length) * 100);
}

document.getElementById("overallProgress").style.width = percent + "%";
document.getElementById("overallProgress").innerText = percent + "%";

document.getElementById("totalSkills").innerText = path.length;
document.getElementById("completedSkillsCount").innerText = completedCount;
document.getElementById("timeLeft").innerText = remainingHours + " hrs";

// Chart
const ctx = document.getElementById("progressChart");

new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Completed', 'Remaining'],
        datasets: [{
            data: [
                completedCount,
                path.length - completedCount
            ]
        }]
    },
    options: {
        responsive: true
    }
});

// ---------- Recommended Courses ----------
const recList = document.getElementById("recommendList");

if (recList) {
    recommendations.forEach(r => {
        const li = document.createElement("li");
        li.innerText = r;
        recList.appendChild(li);
    });
}
