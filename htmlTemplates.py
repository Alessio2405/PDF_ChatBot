css = '''
<style>
/* General Chat Container Styles */
.chat-message {
    padding: 1.2rem;
    border-radius: 8px;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    font-family: Arial, sans-serif;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* User and Bot Message Backgrounds */
.chat-message.user {
    background-color: #344055;
}
.chat-message.bot {
    background-color: #4d5668;
}

/* Avatar Container */
.chat-message .avatar {
    width: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 1rem;
}
.chat-message .avatar img {
    width: 100%;
    height: auto;
    border-radius: 50%;
    object-fit: cover;
}

/* Message Text Styling */
.chat-message .message {
    flex-grow: 1;
    padding: 0.8rem 1.2rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: #fff;
    font-size: 0.95rem;
    line-height: 1.5;
}
</style>
'''
