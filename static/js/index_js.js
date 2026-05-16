//Search Suggestion logic
console.log("Autocomplete JS loaded"); 

document.querySelectorAll(".search-wrapper").forEach(wrapper => {       //apply to all search bars
    const input = wrapper.querySelector(".search-input");       //search input
    const suggestionsBox = wrapper.querySelector(".suggestions");   //suggestions box

    input.addEventListener("input", async () => {    //checks for typed inputs
        const query = input.value.trim();       //reads input

        if (!query) {       //ignores empty input
            suggestionsBox.innerHTML = "";
            return;
        }

        const response = await fetch(`/suggest?q=${query}`);     //calls flask which initiates search_suggest()
        const suggestions = await response.json();      //stores response from search_suggest()

        suggestionsBox.innerHTML = "";      //clears old suggestions

        suggestions.forEach(item => {        //loops through suggestions
            const div = document.createElement("div");      //creates entries for each one
            div.className = "suggestion";
            div.textContent = item;

            div.onclick = () => {       //when suggestion clicked
                input.value = item;     //used as input for search()
                suggestionsBox.innerHTML = "";      //clear old suggestions
            };

            suggestionsBox.appendChild(div);        //Add suggestion to page
        });
    });
});

// Contribute page form logic
function showForm(formId) {
    document.getElementById('buttons-view').style.display = 'none';
    document.getElementById(formId).style.display = 'block';
}

function hideForm(formId) {
    document.getElementById(formId).style.display = 'none';
    document.getElementById('buttons-view').style.display = 'flex';
}

function submitViaEmail() {
    const data = document.getElementById('new-animal-text').value;
    const subject = encodeURIComponent("Creature Lookup - New Animal Request");
    const body = encodeURIComponent("New animal submission:\n\n" + data);
    window.open(`https://mail.google.com/mail/?view=cm&to=341162980a@gmail.com&su=${subject}&body=${body}`, '_blank');
    hideForm('new-animal-form');
}

function showForm(formId) {
    document.getElementById('buttons-view').style.display = 'none';
    document.getElementById('hero-text-1').style.display = 'none';
    document.getElementById('hero-text-2').style.display = 'none';
    document.getElementById(formId).style.display = 'block';
}

function hideForm(formId) {
    document.getElementById(formId).style.display = 'none';
    document.getElementById('buttons-view').style.display = 'flex';
    document.getElementById('hero-text-1').style.display = 'block';
    document.getElementById('hero-text-2').style.display = 'block';

    // reset text areas to default
    if (formId === 'new-animal-form') {
        document.getElementById('new-animal-text').value = `Animal,Height (cm),Weight (kg),Color,Lifespan (years),Diet,Habitat,Predators,Average Speed (km/h),Countries Found,Conservation Status,Family,Gestation Period (days),Top Speed (km/h),Social Structure,Offspring per Birth,Food
Bengal Tiger,90-110,220-260,"Orange, Black",10-15,Carnivore,"Grasslands, Mangroves","Humans, Crocodiles",65,"India, Bangladesh, Nepal",Endangered,Felidae,104-106,65,Solitary,2-4,"Deer, wild boar, water buffalo"`;
    } else if (formId === 'data-change-form') {
        document.getElementById('data-change-text').value = ``;
    }
}

function submitChangeViaEmail() {
    const data = document.getElementById('data-change-text').value;
    const subject = encodeURIComponent("Creature Lookup - Data Change Request");
    const body = encodeURIComponent("Data change submission:\n\n" + data);
    window.open(`https://mail.google.com/mail/?view=cm&to=341162980a@gmail.com&su=${subject}&body=${body}`, '_blank');
    hideForm('data-change-form');
}


// hide carousel when results are shown
window.addEventListener('DOMContentLoaded', () => {
    const carousel = document.getElementById('carousel-wrapper');
    const hasResults = document.querySelector('.card') || document.querySelector('.results p');
    if (carousel && hasResults) {
        carousel.style.display = 'none';
    }
});


// hide food chain hero image when results are shown
window.addEventListener('DOMContentLoaded', () => {
    const heroImg = document.getElementById('foodchain-hero-img');
    const hasResults = document.querySelector('.food-chain') || document.querySelector('.results p');
    if (heroImg && hasResults) {
        heroImg.style.display = 'none';
    }
});