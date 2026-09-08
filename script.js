// ========================================
// InterviewAI - Registration System
// ========================================

const registrationForm = document.getElementById("registrationForm");

registrationForm.addEventListener("submit", async function (event) {

    // Prevent page refresh
    event.preventDefault();

    // ========================================
    // GET FORM VALUES
    // ========================================

    const fullName = document.getElementById("fullName").value.trim();
    const email = document.getElementById("email").value.trim();
    const targetRole = document.getElementById("targetRole").value;
    const experience = document.getElementById("experience").value;
    const skills = document.getElementById("skills").value.trim();
    const terms = document.getElementById("terms").checked;


    // ========================================
    // VALIDATION
    // ========================================

    if (fullName === "") {
        alert("Please enter your full name.");
        return;
    }

    if (email === "") {
        alert("Please enter your email address.");
        return;
    }

    if (targetRole === "") {
        alert("Please select your target job role.");
        return;
    }

    if (experience === "") {
        alert("Please select your experience level.");
        return;
    }

    if (skills === "") {
        alert("Please enter at least one skill.");
        return;
    }

    if (!terms) {
        alert("Please accept the terms to continue.");
        return;
    }


    // ========================================
    // CREATE PROFILE OBJECT
    // ========================================

    const candidateProfile = {

        name: fullName,

        email: email,

        targetRole: targetRole,

        experience: experience,

        skills: skills.split(",").map(function (skill) {
            return skill.trim();
        }),

        createdAt: new Date().toISOString()
    };


    // ========================================
    // SAVE PROFILE LOCALLY
    // ========================================

    localStorage.setItem(
        "interviewAIProfile",
        JSON.stringify(candidateProfile)
    );


    // ========================================
    // SEND DATA TO FASTAPI BACKEND
    // ========================================

    try {

        const response = await fetch(
    "https://ai-interview-performance-system.onrender.com/candidates",
    {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name: fullName,
            email: email,
            target_role: targetRole,
            experience: experience,
            skills: skills
        })
    }
);


        const data = await response.json();


        // ========================================
        // CHECK BACKEND RESPONSE
        // ========================================

        if (!response.ok || !data.success) {

            alert(
                "Could not save your profile to the database.\n\n" +
                data.message
            );

            return;
        }


        // ========================================
        // DATABASE SUCCESS
        // ========================================

        console.log(
            "Candidate saved with ID:",
            data.candidate_id
        );


        // ========================================
        // SUCCESS MESSAGE
        // ========================================

        alert(
            "Profile created successfully!\n\n" +
            "Welcome to InterviewAI, " +
            fullName +
            "!"
        );


        // ========================================
        // GO TO PERFORMANCE DASHBOARD
        // ========================================

        console.log("REDIRECTING TO DASHBOARD");

        setTimeout(function () {
            window.location.href = "performance.html";
        }, 500);


    } catch (error) {

        console.error(
            "Backend connection error:",
            error
        );

        alert(
            "Unable to connect to the InterviewAI server.\n\n" +
            "Please make sure the FastAPI backend is running."
        );
    }

});
