"use strict";

const Menu = {
    info: 1,
    doctors: 2,
    schedule: 3,
    order: 4,
};

window.onload = () => {
    if (!sessionStorage.getItem('has_covid_loaded')) {
        sessionStorage.setItem('has_covid_loaded', "false")
    }
    const is_covid_loading = sessionStorage.getItem('is_covid_loading');
    const has_covid_loaded = sessionStorage.getItem('has_covid_loaded');
    const cases_field = document.getElementById('cases')
    const recovered_field = document.getElementById('recovered')
    const deaths_field = document.getElementById('deaths')
    const loader = document.getElementById('loader')
    const hideLoader = () => {
        loader.style.display = 'none'
    }
    const saveData = (cases, recovered, deaths) => {
        sessionStorage.setItem('cases', cases)
        sessionStorage.setItem('recovered', recovered)
        sessionStorage.setItem('deaths', deaths)
    }
    const showData = (cases, recovered, deaths) => {
        cases_field.innerText = "Всего случаев: " + cases
        recovered_field.innerText = "Выздоровело: " + recovered
        deaths_field.innerText = "Умерло: " + deaths
    }
    if (is_covid_loading === "true"){

    }else if (has_covid_loaded === "true") {
        hideLoader()
        showData(sessionStorage.getItem('cases'),
                 sessionStorage.getItem('recovered'),
                 sessionStorage.getItem('deaths'))
    }else{
        sessionStorage.setItem('is_covid_loading', "true")
        setTimeout(
            () =>
                fetch('https://covid2019-api.herokuapp.com/v2/country/belarus')
                    .then(async (r) => {
                        const {data} = await r.json()
                        hideLoader()
                        saveData(data.confirmed, data.recovered, data.deaths)
                        showData(data.confirmed, data.recovered, data.deaths)
                    })
                    .catch(() => {
                        hideLoader()
                        cases_field.innerText = "Время ожидания загрузки данных истекло"
                    }),
            2000
        )
        sessionStorage.setItem('has_covid_loaded', "true")
    }


    if (!sessionStorage.getItem('MENU_SELECTED')) {
        sessionStorage.setItem('MENU_SELECTED', Menu.info)
    }

    const info = document.getElementById('info');
    const doctors = document.getElementById('doctors');
    const schedule = document.getElementById('schedule');
    const order = document.getElementById('order');

    const lastClicked = sessionStorage.getItem('MENU_SELECTED');

    const elements = {
        [Menu.info]: info,
        [Menu.doctors]: doctors,
        [Menu.schedule]: schedule,
        [Menu.order]: order,
    };
    
    elements[lastClicked].classList.add('menu__selected');

    const getCallbackChangeSessionStorage = (changed) => () => {
        sessionStorage.setItem('MENU_SELECTED', changed);
        sessionStorage.removeItem('day_picked')
        sessionStorage.removeItem('talon_picked')
    }

    info.addEventListener('click', getCallbackChangeSessionStorage(Menu.info));
    doctors.addEventListener('click', getCallbackChangeSessionStorage(Menu.doctors));
    schedule.addEventListener('click', getCallbackChangeSessionStorage(Menu.schedule));
    order.addEventListener('click', getCallbackChangeSessionStorage(Menu.order));


    const btns = document.querySelectorAll('.day')
    btns.forEach(btn => {
       btn.addEventListener('click', event => {
            console.log( event.target.value);
            sessionStorage.setItem('day_picked', event.target.value)
            sessionStorage.removeItem('talon_picked')
       });
    });

    if (sessionStorage.getItem('day_picked')) {
        const day_number = sessionStorage.getItem('day_picked')
        btns.forEach(btn => {
            if (btn.value === day_number) {
                btn.style.color = "red"
            }
        });
    }


    const talons = document.querySelectorAll('.not-taken')
    talons.forEach(talon => {
       talon.addEventListener('click', event => {
            sessionStorage.setItem('talon_picked', event.target.value)
       });
    });

    if (sessionStorage.getItem('talon_picked')) {
        const talon_number = sessionStorage.getItem('talon_picked')
        talons.forEach(talon => {
            if (talon.value === talon_number) {
                talon.style.color = "red"
            }
        });
    }

};
