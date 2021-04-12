"use strict";

const Menu = {
    info: 1,
    doctors: 2,
    schedule: 3,
    order: 4,
};

window.onload = () => {
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

    const getCallbackChangeSessionStorage = (changed) => () => sessionStorage.setItem('MENU_SELECTED', changed);

    info.addEventListener('click', getCallbackChangeSessionStorage(Menu.info));
    doctors.addEventListener('click', getCallbackChangeSessionStorage(Menu.doctors));
    schedule.addEventListener('click', getCallbackChangeSessionStorage(Menu.schedule));
    order.addEventListener('click', getCallbackChangeSessionStorage(Menu.order));
};