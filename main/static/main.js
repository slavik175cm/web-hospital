    "use strict";

    const Menu = {
        info: 1,
        doctors: 2,
        schedule: 3,
        order: 4,
        profile: 5,
        history: 6
    };
    const hideLoader = () => {
        loader.style.display = 'none'
    };
    const saveData = (cases, recovered, deaths) => {
        sessionStorage.setItem('cases', cases);
        sessionStorage.setItem('recovered', recovered);
        sessionStorage.setItem('deaths', deaths)
    };
    const showData = (cases, recovered, deaths) => {
        const recovered_field = document.getElementById('recovered');
        const deaths_field = document.getElementById('deaths');
        const cases_field = document.getElementById('cases');
        cases_field.innerText = "Всего случаев: " + cases;
        recovered_field.innerText = "Выздоровело: " + recovered;
        deaths_field.innerText = "Умерло: " + deaths
    };
    async function load_statistics() {
        setTimeout(
            () =>
                fetch('https://covid2019-api.herokuapp.com/v2/country/belarus')
                    .then(async (r) => {
                        const {data} = await r.json();
                        hideLoader();
                        saveData(data.confirmed, data.recovered, data.deaths);
                        showData(data.confirmed, data.recovered, data.deaths);
                        sessionStorage.setItem('has_covid_loaded', "true");
                    })
                    .catch(() => {
                        hideLoader();
                        sessionStorage.setItem('has_covid_loaded', "true");
                        sessionStorage.setItem('is_covid_loading', "false");
                        const cases_field = document.getElementById('cases');
                        cases_field.innerText = "данные не могут быть получены";
                    }),
            2000
        );
    }
    window.onload = async () => {
        sessionStorage.setItem('is_covid_loading', "false")
        if (!sessionStorage.getItem('has_covid_loaded')) {
            sessionStorage.setItem('has_covid_loaded', "false")
        }
        let is_covid_loading = sessionStorage.getItem('is_covid_loading');
        let has_covid_loaded = sessionStorage.getItem('has_covid_loaded');
        const cases_field = document.getElementById('cases');
        if (has_covid_loaded === "true") {
            hideLoader();
            if (sessionStorage.getItem('recovered') === null) {
                cases_field.innerText = "данные не могут быть получены";
            } else {
                showData(sessionStorage.getItem('cases'),
                sessionStorage.getItem('recovered'),
                sessionStorage.getItem('deaths'))
            }
        } else if (is_covid_loading === 'false') {
            sessionStorage.setItem('is_covid_loading', "true");
            load_statistics();
        }


        if (!sessionStorage.getItem('MENU_SELECTED')) {
            sessionStorage.setItem('MENU_SELECTED', Menu.info)
        }

        const info = document.getElementById('info');
        const doctors = document.getElementById('doctors');
        const schedule = document.getElementById('schedule');
        const order = document.getElementById('order');
        const profile = document.getElementById('profile');
        const history = document.getElementById('history');
        const lastClicked = sessionStorage.getItem('MENU_SELECTED');

        const elements = {
            [Menu.info]: info,
            [Menu.doctors]: doctors,
            [Menu.schedule]: schedule,
            [Menu.order]: order,
            [Menu.profile]: profile,
            [Menu.history]: history
        };

        elements[lastClicked].classList.add('menu__selected');

        const getCallbackChangeSessionStorage = (changed) => () => {
            sessionStorage.setItem('MENU_SELECTED', changed);
            sessionStorage.removeItem('day_picked');
            sessionStorage.removeItem('talon_picked')
        };

        info.addEventListener('click', getCallbackChangeSessionStorage(Menu.info));
        doctors.addEventListener('click', getCallbackChangeSessionStorage(Menu.doctors));
        schedule.addEventListener('click', getCallbackChangeSessionStorage(Menu.schedule));
        order.addEventListener('click', getCallbackChangeSessionStorage(Menu.order));
        if (profile != null)
            profile.addEventListener('click', getCallbackChangeSessionStorage(Menu.profile));
        if (history != null)
            history.addEventListener('click', getCallbackChangeSessionStorage(Menu.history));

        const btns = document.querySelectorAll('.day');

        if (sessionStorage.getItem('day_picked')) {
            const day_number = sessionStorage.getItem('day_picked');
            btns.forEach(btn => {
                if (btn.value === day_number) {
                    btn.style.color = "red"
                }
            });
        }

        btns.forEach(btn => {
            btn.addEventListener('click', () => {
                sessionStorage.setItem('day_picked', btn.value);
                sessionStorage.removeItem('talon_picked')
            });
        });


        const talons = document.querySelectorAll('.not-taken');
        talons.forEach(talon => {
            talon.addEventListener('click', () => {
                sessionStorage.setItem('talon_picked', talon.value)
            });
        });

        if (sessionStorage.getItem('talon_picked')) {
            const talon_number = sessionStorage.getItem('talon_picked');
            talons.forEach(talon => {
                if (talon.value === talon_number) {
                    talon.style.color = "red"
                }
            });
        }

    };
