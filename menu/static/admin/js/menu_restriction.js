/*
 * Ограничивает значения поля "Принадлежит пункту меню" только значениями принадлежащими выбранному значению
 * поля "Наименование меню"
 */
document.addEventListener("DOMContentLoaded", function () {
    let menuField = document.getElementById("id_menu");
    let menuNameField = document.getElementById("id_menu_name");
    let allMenuOptions = menuField.options;
    let convertedMenuItem = convertingMenuItem(allMenuOptions);
    // Запоминаю текущее значение выбранного меню,
    let currentItemSelectedValue = menuField.value;
    changeMenuFieldChoice(menuField, menuNameField.options[menuNameField.selectedIndex].innerText, convertedMenuItem);
    // чтобы после изменения списка подменю обратно выбрать именно этот пункт меню.
    menuField.value = currentItemSelectedValue;

    /** Устанавливает обработку события выбора наименования меню.*/
    menuNameField.addEventListener("change",(e) => {
        let field = e.target;
        // Изменят список в соответствии с выбранным именем меню.
        changeMenuFieldChoice(menuField, field.options[field.selectedIndex].innerText, convertedMenuItem);
    } )
})

/**
 * Конвертирует переданный список options в структурированный список подменю
 * @param options
 * @returns {{}}
 */
function convertingMenuItem(options) {
    let convertedMenu = {}
    Object.keys(options).forEach(i => {
        const el = options[i];
        const menuName = el.innerText.substring(0, el.innerText.indexOf(": "));
        const text = el.innerText.substring(el.innerText.indexOf(": ") + 2);
        const value = el.value;

        if (!convertedMenu.hasOwnProperty(menuName))
            convertedMenu[menuName] = [[value, text]];
        else
            convertedMenu[menuName].push([value, text])
    })
    return convertedMenu;
}

/**
 * Изменяет список выбора подменю
 * @param menuField {HTMLSelectElement} поле меню
 * @param menuName текущее значение имени меню
 * @param convertedMenuItem сконвертированный список меню
 */
function changeMenuFieldChoice(menuField, menuName, convertedMenuItem) {
    menuField.innerHTML = "";
    menuField.options.add(getOptions(convertedMenuItem[""][0]))
    convertedMenuItem[menuName].forEach(item => {
        menuField.options.add(getOptions(item));
    })
}

/**
 * Возвращает элемент option для select
 * @param item список пара значение - текст
 * @returns {HTMLOptionElement}
 */
function getOptions(item) {
    let option = document.createElement("option");
    option.value = item[0];
    option.innerText = item[1];
    return option
}