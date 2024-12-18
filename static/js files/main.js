// JavaScript for slider functionality on the homepage
let currentSlide = 0;
const slides = document.querySelectorAll(".slide");
const totalSlides = slides.length;
document.addEventListener("DOMContentLoaded", () => {
    const slides = document.querySelectorAll(".slide");
    const totalSlides = slides.length;
    let currentSlide = 0;

    // Function to display the current slide
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.transform = `translateX(${(i - index) * 100}%)`;
        });
    }

    // Function to automatically transition slides
    function autoSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }

    // Initialize the slider
    showSlide(currentSlide);

    // Set the slide interval (5 seconds)
    setInterval(autoSlide, 5000);
});



// Dynamic navigation handling
document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll(".nav-links a");
    navLinks.forEach(link => {
        link.addEventListener("click", e => {
            e.preventDefault();
            const target = e.target.getAttribute("href");
            window.location.href = target;
        });
    });
});

// Register form validation
const registerForm = document.querySelector("form[action='/register']");
if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (!username || !email || !password) {
            e.preventDefault();
            alert("All fields are required!");
        }
    });
}

// Login form validation
const loginForm = document.querySelector("form[action='/login']");
if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (!email || !password) {
            e.preventDefault();
            alert("Please enter your email and password!");
        }
    });
}

// Hover effects for social media icons
const socialIcons = document.querySelectorAll(".social-icons a img");
socialIcons.forEach(icon => {
    icon.addEventListener("mouseover", () => {
        icon.style.transform = "scale(1.2)";
    });
    icon.addEventListener("mouseout", () => {
        icon.style.transform = "scale(1)";
    });
});
function readMore(articleId) {
    alert(`Read more about ${articleId}!`);
}

// function bookEvent(eventId) {
//     alert(`Booking confirmed for ${eventId}!`);
// }
// let currentSlide = 0;
// const slides = document.querySelectorAll(".slide");
// const totalSlides = slides.length;

function bookEvent(eventId) {
    // Here we're using fetch API to send a request to the server
    fetch(`/book_event/${eventId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Booking confirmed for Event: ${data.eventName}`);
        } else {
            alert(`Booking failed: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error with your booking request.');
    });
}

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.transform = `translateX(${(i - index) * 100}%)`;
    });
}

function autoSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

setInterval(autoSlide, 5000);

// Dynamic navigation
document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll("nav ul li a");
    navLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const targetPage = e.target.getAttribute("href");
            window.location.href = targetPage;
        });
    });
});

// Buttons functionality
function readMore(articleId) {
    alert(`Read more about article: ${articleId}`);
}

function bookEvent(eventId) {
    alert(`You have successfully booked the event: ${eventId}`);
}
function bookEvent(eventId) {
    alert(`Booking confirmed for event ID: ${eventId}!`);
}

// Optional: Slider, form validation, and any additional JS functionality can be added here.