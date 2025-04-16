// Sticky, Smooth, Active Nav Start

const mainNavLinks = document.querySelectorAll(".header-navbar-menu li a");

function handleScrollSpy() {
    const fromTop = window.scrollY + window.innerHeight / 2;

    mainNavLinks.forEach(link => {
        const section = document.querySelector(link.hash);
        const sectionTop = section.offsetTop;
        const sectionBottom = sectionTop + section.offsetHeight;

        if (fromTop >= sectionTop && fromTop < sectionBottom) {
            link.classList.add("current");
        } else {
            link.classList.remove("current");
        }
    });
}

window.addEventListener("scroll", handleScrollSpy);

document.addEventListener("DOMContentLoaded", handleScrollSpy);

// Sticky, Smooth, Active Nav End


// Loader Start

document.addEventListener("DOMContentLoaded", () => {
    const loader = document.querySelector(".loader");
    const mainContent = document.querySelector(".main-content");

    // Loader göstərildikdən sonra 3 saniyə gözlə və keçidi et
    setTimeout(() => {
        hideLoader(loader);
        showContent(mainContent);
    }, 3000);
});

function hideLoader(loaderElement) {
    loaderElement.classList.add("hidden");
}

function showContent(contentElement) {
    contentElement.classList.add("visible");
}

// Loader End


// Switcher color Start
const switcherBtn = document.querySelector(".switcher-btn");
const colorSwitcherItem = document.querySelector(".color-switcher");

switcherBtn.addEventListener('click', () => {
    colorSwitcherItem.classList.add('active');
})

document.addEventListener('click', e => {
    if (!e.composedPath().includes(colorSwitcherItem) && !e.composedPath().includes(switcherBtn)) {
        colorSwitcherItem.classList.remove('active');
    }
})

let themeButtons = document.querySelectorAll('.theme-buttons');

themeButtons.forEach(color => {
    color.addEventListener('click', () => {
        let dataColor = color.getAttribute('data-color');
        document.querySelector(':root').style.setProperty('--color-mountain-meadow', dataColor)
    })
})

// Switcher color End


// Navbar scroll Start
document.onreadystatechange = function () {
    let lastScrollPosition = 0;
    let navbar = document.querySelector('.header_section');
    window.addEventListener('scroll', function (e) {
        lastScrollPosition = window.scrollY;
        if (lastScrollPosition > 250)
            navbar.classList.add('navbar-dark');
        else
            navbar.classList.remove('navbar-dark');
    });
}

// Scroll top
let mybutton = document.getElementById("btn-back-to-top");

window.onscroll = function () {
    scrollFunction();
};


function scrollFunction() {
    if (
        document.body.scrollTop > 600 ||
        document.documentElement.scrollTop > 600
    ) {
        mybutton.style.display = "block";
        mybutton.style.zIndex = "99"
    } else {
        mybutton.style.display = "none";
        mybutton.style.zIndex = "-1"

    }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

// Navbar scroll End


// Text Typing Effects Start

const typedTextSpan = document.querySelector(".typed-text");
const cursorSpan = document.querySelector(".cursor");

const textArray = ["Sabuhi Gasimov", "Web Developer."];
const typingDelay = 200;
const erasingDelay = 100;
const newTextDelay = 2000;
let textArrayIndex = 0;
let charIndex = 0;

function type() {
    if (charIndex < textArray[textArrayIndex].length) {
        if (!cursorSpan.classList.contains("typing")) cursorSpan.classList.add("typing");
        typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, typingDelay);
    } else {
        cursorSpan.classList.remove("typing");
        setTimeout(erase, newTextDelay);
    }
}

function erase() {
    if (charIndex > 0) {
        if (!cursorSpan.classList.contains("typing")) cursorSpan.classList.add("typing");
        typedTextSpan.textContent = textArray[textArrayIndex].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(erase, erasingDelay);
    } else {
        cursorSpan.classList.remove("typing");
        textArrayIndex++;
        if (textArrayIndex >= textArray.length) textArrayIndex = 0;
        setTimeout(type, typingDelay + 1100);
    }
}

document.addEventListener("DOMContentLoaded", function () { // On DOM Load initiate the effect
    if (textArray.length) setTimeout(type, newTextDelay + 250);
});

// Text Typing Effects End

// Responsive menu bar Start

// Mobile menu
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".header-navbar-menu");

hamburger.addEventListener("click", mobileMenu);

function mobileMenu() {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
}

// Close menu
const navLink = document.querySelectorAll(".header-navbar-menu li a");

navLink.forEach(n => n.addEventListener("click", closeMenu));

function closeMenu() {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
}

// Responsive menu bar End