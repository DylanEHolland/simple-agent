from agent.helpers import get_agent, get_user_from_db, save_user

# print(get_agent())

# save_user({
#     "phone_number": "+6187516231",
#     "name": "Dylan"
# })

print(get_user_from_db("+16187516231"))