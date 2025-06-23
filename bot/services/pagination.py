from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def paginate(items: list, page: int, page_size: int):
    start = page * page_size
    end = start + page_size
    return items[start:end]


async def send_paginated_page(
    msg_or_callback,
    items: list,
    page: int,
    page_size: int,
    render_item_fn,
    callback_prefix: str,
    title: str = "Сторінка",
    extra_buttons_fn=None
):
    page_items = paginate(items, page, page_size)
    total_pages = (len(items) + page_size - 1) // page_size

    response = f"📄 <b>{title} {page + 1} з {total_pages}:</b>\n\n"
    builder = InlineKeyboardBuilder()

    for item in page_items:
        response += render_item_fn(item)

    if extra_buttons_fn:
        extra_buttons_fn(builder, page_items)

    # Навігація
    if page > 0:
        builder.button(text="⬅️ Назад", callback_data=f"{callback_prefix}_{page - 1}")
    if (page + 1) * page_size < len(items):
        builder.button(text="Вперед ➡️", callback_data=f"{callback_prefix}_{page + 1}")

    builder.adjust(1)
    keyboard = builder.as_markup()

    if isinstance(msg_or_callback, types.Message):
        await msg_or_callback.answer(response, parse_mode="HTML", reply_markup=keyboard)
    else:
        await msg_or_callback.message.edit_text(response, parse_mode="HTML", reply_markup=keyboard)
