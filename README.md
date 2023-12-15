# Django Chat App (DCA) project

A simple chat app powered by Django.


![ezgif com-video-to-gif-converted(1)](https://github.com/errfunm/chat_app/assets/53046898/0ef8438a-735c-40b3-9abb-5d14ebdd85f0)

## Architecture
- There is a list of chat rooms for each user. Whenever a user sends a request to one of them, a WebSocket handshake will occur, enabling real-time chat for users in that room.

- Users can retrieve all their recent messages unless they choose to 'clear history.'

- Unauthenticated users cannot use the app and will be redirected to the login/register page.

- Users have the option to restore their password if forgotten.

## Libraries Used

 - ###  Channels:
Using the Django Channels library provides real-time functionality and enables the handling of WebSockets. Django Channels extends the capabilities of Django to support WebSockets and other asynchronous protocols. I use Redis as a message broker; it efficiently handles the routing of messages between channels.

## Scaling
### Database:
For a start, I'm using the default db.sqlite3. For higher performance, you may use MySQL, PostgreSQL, or other databases.

## TODO

### There are a few tasks for adding to this project:
  1. Using frontend technologies to enhance the UI/UX.
  2. Adding user online status.
  3. Implementing message seen status.
  4. Showing 'typing...' status when a user is typing.
  5. Enabling users to edit their profiles (currently, the only way is using the Django admin panel).
  6. Adding comments/documentation strings."

## Run

To run this Django project locally, follow these steps:

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/errfunm/chat_app
   ```
   
3. **Navigate to the project directory**

   ```bash
   
   cd chat_app
   
   ```
   
4. **Create and activate a virtual environment:**
 
   ```bash
   
   python -m venv virtual_environment_name
   source virtual_environment_name/bin/activate  # On Windows, use `virtual_environment_name\Scripts\activate`
   
   ```

5. **Install dependencies:**

   ```bash
   
   pip install -r requirements.txt
   
   ```

6. **Run the Redis server:**

   ```bash
   
   redis-server
   
   ```

7. **Apply database migrations:**

   ```bash
   
   python manage.py migrate
   
   ```

8. **Create a super user:**

   ```bash
   
   python manage.py createsuperuser
   
   ```

9. **Run the development server**

   ```bash
   
   python manage.py runserver
   
   ```
   
