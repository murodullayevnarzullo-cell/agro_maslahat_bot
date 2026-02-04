from aiogram.dispatcher.filters.state import State, StatesGroup

class AddAdminState(StatesGroup):
    waiting_for_id = State()

class DeleteAdminState(StatesGroup):
    waiting_for_id = State()
