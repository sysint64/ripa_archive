const strings = {
    "Delete selected items?": {
        "ru": "Удалить выбранные элементы?"
    },
    "Something went wrong! Please contact with administrator.<br>Status code: ": {
        "ru": "Что-то пошло не так! Пожалуйста свяжитесь с администратором.<br>Status code: "
    },
    "Permission denied": {
        "ru": "Доступ запрещен"
    },
    "Unexpected error (server respond with status code ": {
        "ru": "Неожиданная ошибка (сервер вернул статус код )"
    },
    "Rename": {
        "ru": "Переименовать"
    },
    "Edit permissions": {
        "ru": "Редактировать права"
    },
    "Update status": {
        "ru": "Обновить статус"
    },
    "Cut": {
        "ru": "Вырезать"
    },
    "Copy": {
        "ru": "Копировать"
    },
    "Delete": {
        "ru": "Удалить"
    },
    "Create folder(s)": {
        "ru": "Создать папку(и)"
    },
    "Create document(s)": {
        "ru": "Создать документ(ы)"
    },
    "Paste": {
        "ru": "Вставить"
    },
    "Take this document for revision?": {
        "ru": "Взять документ на доработку?"
    },
    "Accept new version of document?": {
        "ru": "Принять новую версию документа?"
    },
    "Reject new version of document and revert previous?": {
        "ru": "Отклонить новую версию документа и откатить на предыдущую версию?"
    },
    "Do not follow": {
        "ru": "Не отслеживать"
    },
    "Follow": {
        "ru": "Отслеживать"
    },
    "Revert this version of document?": {
        "ru": "Откатить на эту версию документа?"
    },
    "Accept this remark?": {
        "ru": "Принять это замечание?"
    },
    "Reject this remark, and write another one?": {
        "ru": "Отклонить замечание и написать новое?"
    },
    "Mark this remark as \"finished\" and send notification to reviewer?": {
        "ru": "Отметить это замечание как \"выполненное\" и отправить уведомление рецензенту?"
    }
};

const language = $("#langauge_code").data("code");

function _(code) {
    if (language == "en" || !language)
        return code;

    return strings[code][language];
}
