ACTIVITY_CREATE_DOCUMENT = "Created document \"{name}\" (path: Root/{path})"
ACTIVITY_CREATE_FOLDER = "Created folder \"{name}\" (path: Root/{path})"
ACTIVITY_RENAME_DOCUMENT = "Rename document from \"{old_name}\" to \"{new_name}\""
ACTIVITY_RENAME_FOLDER = "Rename folder from \"{old_name}\" to \"{new_name}\""
ACTIVITY_MOVE_DOCUMENT = "Move document from \"Root/{old_path}\" to \"Root/{new_path}\""
ACTIVITY_MOVE_FOLDER = "Move folder from \"Root/{old_path}\" to \"Root/{new_path}\""
ACTIVITY_REVERT_DOCUMENT = "Revert document from {datetime}"
ACTIVITY_COPY_DOCUMENT = "Copy document"
ACTIVITY_COPY_FOLDER = "Copy folder"
ACTIVITY_DELETE_FOLDER = "Delete folder \"Root/{path}\""
ACTIVITY_DELETE_DOCUMENT = "Delete document \"Root/{path}\""

ACTIVITY_REF_SOURCE_FOLDER = "Source folder"
ACTIVITY_REF_SOURCE_DOCUMENT = "Source document"

NOTIFICATION_REMARK_ACCEPTED = "Was accepted remark"
NOTIFICATION_REMARK_FINISHED = "Remark was marked as \"finished\""
NOTIFICATION_REMARK_REJECTED = "Was rejected remark"
NOTIFICATION_REMARK_WROTE = "Was wrote remark"
NOTIFICATION_DOCUMENT_ACCEPTED = "Was accepted new version of document"
NOTIFICATION_DOCUMENT_REJECTED = "Was rejected new version of document"


# Internationalization

ACTIVITY_STRINGS = {
    ACTIVITY_CREATE_DOCUMENT: {
        "ru": "Создание документа \"{name}\" (путь: Root/{path})"
    },
    ACTIVITY_CREATE_FOLDER: {
        "ru": "Создание папки \"{name}\" (путь: Root/{path})"
    },
    ACTIVITY_RENAME_DOCUMENT: {
        "ru": "Переименование документа из \"{old_name}\" в \"{new_name}\""
    },
    ACTIVITY_RENAME_FOLDER: {
        "ru": "Переименование папки из \"{old_name}\" вo \"{new_name}\""
    },
    ACTIVITY_MOVE_DOCUMENT: {
        "ru": "Переимещение документа из \"Root/{old_path}\" в \"Root/{new_path}\""
    },
    ACTIVITY_MOVE_FOLDER: {
        "ru": "Перемещение папки из \"Root/{old_path}\" в \"Root/{new_path}\""
    },
    ACTIVITY_REVERT_DOCUMENT: {
        "ru": "Откат документа от {datetime}"
    },
    ACTIVITY_COPY_DOCUMENT: {
        "ru": "Копирование документа"
    },
    ACTIVITY_COPY_FOLDER: {
        "ru": "Копирование папки"
    },
    ACTIVITY_DELETE_FOLDER: {
        "ru": "Удаление папки \"Root/{path}\""
    },
    ACTIVITY_DELETE_DOCUMENT: {
        "ru": "Удаление документа \"Root/{path}\""
    },
}

ACTIVITY_REF_STRINGS = {
    ACTIVITY_REF_SOURCE_FOLDER: {
        "ru": "Исходная папка"
    },
    ACTIVITY_REF_SOURCE_DOCUMENT: {
        "ru": "Иходный документ"
    }
}

NOTIFICATION_STRINGS = {
    NOTIFICATION_REMARK_ACCEPTED: {
        "ru": "Одобрено замечание"
    },
    NOTIFICATION_REMARK_FINISHED: {
        "ru": "Замечание отмечено как \"завершенное\""
    },
    NOTIFICATION_REMARK_REJECTED: {
        "ru": "Отклонено замечание"
    },
    NOTIFICATION_REMARK_WROTE: {
        "ru": "Было написано замечание"
    },
    NOTIFICATION_DOCUMENT_ACCEPTED: {
        "ru": "Одобрена новая версия документа"
    },
    NOTIFICATION_DOCUMENT_REJECTED: {
        "ru": "Отклонена новая версия документа"
    },
}


def i18n_format(str, **kwargs):
    new_kwargs = kwargs.copy()
    new_kwargs.update({"__code_string": str})
    return new_kwargs


def _parse_string(string, new_format_string=None):
    if isinstance(string, str):
        return new_format_string if new_format_string is not None else string
    elif isinstance(string, dict):
        if new_format_string is not None:
            format_string = new_format_string
        else:
            format_string = string["__code_string"]

        kwargs = string.copy()
        kwargs.pop("__code_string")

        assert format_string is not None
        return format_string.format(**kwargs)
    else:
        raise AssertionError("Unknown instance type")


def _get_code(string):
    if isinstance(string, str):
        return string
    elif isinstance(string, dict):
        return string["__code_string"]
    else:
        raise AssertionError("Unknown instance type")


def _get_text(code, strings, lang, default_none=False):
    str_code = _get_code(code)
    string = strings.get(str_code)

    if string is None:
        return None if default_none else str_code

    if lang == "en":
        return _parse_string(code)
    else:
        return _parse_string(code, string[lang])


def get_activity_text(code, lang):
    return _get_text(code, ACTIVITY_STRINGS, lang)


def get_activity_ref_text(code, lang):
    return _get_text(code, ACTIVITY_REF_STRINGS, lang)


def get_notification_text(code, lang):
    string = _get_text(code, NOTIFICATION_STRINGS, lang, True)

    if string is None:
        return get_activity_text(code, lang)
    else:
        return string
