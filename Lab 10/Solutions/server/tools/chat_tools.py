from tools import user_tools, group_tools, message_tools


def get_chat_list(user_id: int):
    users_list = user_tools.get_users()
    users_list = filter(lambda u: u.id != user_id, users_list)
    groups_list = list(user_tools.get_user_groups(user_id))
    # groups_list.append({'name': 'General', 'id': 0})

    chat_list = []

    for user in users_list:
        mess = message_tools.get_last_message_user(user.id, user_id)
        unread = message_tools.get_number_of_unread_message_user(user_id, user.id)
        chat_list.append({
            'id': user.id,
            'name': user.login,
            'group': False,
            'message': mess,
            'unread': unread
        })

    for group in groups_list:
        mess = message_tools.get_last_message_group(group.id)
        unread = message_tools.get_number_of_unread_message_group(user_id, group.id)
        chat_list.append({
            'id': group.id,
            'name': group.name,
            'group': True,
            'message': mess,
            'unread': unread
        })

    mess = message_tools.get_last_message_group(0)
    unread = message_tools.get_number_of_unread_message_group(user_id, 0)
    chat_list.append({
        'id': 0,
        'name': 'General',
        'group': True,
        'message': mess,
        'unread': unread
    })

    return chat_list
