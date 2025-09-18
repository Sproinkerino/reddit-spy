"""
Debug the custom prompt issue
"""

# Test the problematic code
custom_prompt = "tell me about the user\n"
username = "sproinkerino"
user_data = "Some test data"

print("Testing custom prompt formatting...")
print(f"Custom prompt: '{custom_prompt}'")
print(f"Username: {username}")
print(f"User data: {user_data}")

try:
    # This is what the current code does
    user_prompt = custom_prompt.format(username=username, user_data=user_data)
    print("✅ Format successful!")
    print(f"Result: {user_prompt}")
except Exception as e:
    print(f"❌ Format failed: {e}")
    print("This is why the API is failing!")

print("\n" + "="*50)
print("SOLUTION: Check if custom prompt has format placeholders")
print("="*50)

# Better approach
if custom_prompt and ("{username}" in custom_prompt or "{user_data}" in custom_prompt):
    user_prompt = custom_prompt.format(username=username, user_data=user_data)
    print("✅ Custom prompt with placeholders formatted successfully")
else:
    # Just append the data to the custom prompt
    user_prompt = f"{custom_prompt}\n\nUser: u/{username}\nData: {user_data}"
    print("✅ Custom prompt without placeholders handled correctly")
    print(f"Result: {user_prompt}")
