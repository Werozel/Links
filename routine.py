from globals import api
from tree import Node
from user import User

import errors_handling
import logging
import pickle

# мб запускать рекурсию в отдельных процессах из двух потоков - один запускает, другой принимает результат
try:
    f = open("users.bin", "rb")
    users = pickle.load(f)
    f.close()
    print(users)
except Exception as e:
    logging.error("Couldn't load users")
    logging.error(e)
    users = {}


def get_user(id):
    user = users.get(id)
    if user is None:
        user = User(id)
        if user.avaliable:
            users.update({id: user})
    return user


# all_nodes - list of nodes, id - node to find
def get_node(all_nodes, id):
    for i in all_nodes:
        if i.data == id:
            return i
    return None


# first & second - ids of vk pages
def get_route(first, second):
    second_user = get_user(second)

    seen_ids = [first]
    ids_to_check = [first, ""]
    all_nodes = []

    depth = 0
    count = 0

    head = Node(first, None)
    all_nodes.append(head)
    curr_parent = head

    res = []
    flag = False
    flag_depth = depth

    for id in ids_to_check:
        error_raised = False

        if id == "":
            if flag:
                return res
            depth += 1
            print("Depth = " + str(depth))
            if depth > 7:
                return None
            ids_to_check.append("")
            continue

        if id < 0:
            curr_parent = get_node(all_nodes, -id)
            if curr_parent is None:
                logging.error("No such parent!")
                return None
            continue

        user = get_user(id)
        count += 1

        if id not in seen_ids:
            seen_ids.append(id)
            new_node = Node(id, curr_parent)
            all_nodes.append(new_node)
            curr_parent.insert(new_node)

            try:
                tmp_mutual = user.get_mutual(second_user)
            except Exception as e:
                error_raised = True
                errors_handling.get_mutual_error(e, "Couldn't get mutual friends for " + str(id))
                tmp_mutual = []

            if len(tmp_mutual) > 0:     # Находит общих в глубине 1 и не смотрит если есть общие через своих друзей (стопается на эмке и не проверяет другие варианты этой же глубины)
                print("Route found!")
                flag = True
                flag_depth = depth
                for tm in tmp_mutual:
                    buff = Node(tm, new_node)
                    if tm not in seen_ids:
                        all_nodes.append(buff)
                    new_node.insert(buff)
                    res.append(buff)
        else:
            print("Already seen this id - " + str(id))

        try:
            ids_to_check.append(-id)
            ids_to_check += user.friends
        except Exception as e:
            if not error_raised:
                errors_handling.users_get_error(e, "Couldn't get friends list for " + str(id))

        if flag and depth > flag_depth:
            return res

    return None


first_id = int(api.users.get()[0].get('id'))
first_user = get_user(first_id)


while True:
    link = input("Link - ")
    if link == "exit":
        break
    if not link.find("vk.com"):
        logging.error("Not a vk link!")
        continue

    second_tmp = link.partition('https://vk.com/')
    if len(second_tmp) > 3:
        logging.error("Not valid link!")
        continue

    second_id = int(api.users.get(user_ids=second_tmp[2])[0].get("id"))
    second_user = get_user(second_id)

    if second_user.info.get('is_friend') == 1:
        print("Already friends")
        exit()

    mutual = first_user.get_mutual(second_user)
    if len(mutual) > 0:
        print("You have mutual friends:")
        for i in mutual:
            tmp_user = get_user(i)
            print("- " + tmp_user.info.get('first_name') + " " + tmp_user.info.get('last_name'))
        continue

    result = get_route(first_id, second_id)
    if result is None:
        print("No such route!")
    else:
        for i in result:
            list_of_nodes = [Node(second_id)]
            tmp_node = i
            while tmp_node:
                list_of_nodes.append(tmp_node)
                tmp_node = tmp_node.parent
            list_of_nodes.reverse()
            str = ""
            for t in list_of_nodes:
                tmp_user = get_user(t.data)
                str += tmp_user.info.get('first_name') + " " + tmp_user.info.get('last_name')
                if t.data != second_id:
                    str += " -> "
            print(str)

try:
    f = open("users.bin", "wb")
    pickle.dump(users, f)
    f.close()
except Exception as e:
    logging.error("Couldn't dump users")
    logging.error(e)
exit()
