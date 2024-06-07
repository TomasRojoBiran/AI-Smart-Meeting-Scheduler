# AI Smart Meeting Scheduler

A cutting-edge AI tool designed to streamline and automate meeting scheduling. Integrating with Google Calendar, Gmail, and Microsoft Outlook, this application intelligently schedules meetings at optimal times, considering participants' availability and preferences. The project leverages advanced natural language processing (NLP) techniques and a robust scheduling algorithm built with TensorFlow and Keras. It features seamless integration with Google Calendar, Gmail, and Microsoft Outlook, providing an efficient and user-friendly web interface developed using Flask. This repository includes the backend logic for CRUD operations, database models, and migration scripts, ensuring a scalable and maintainable codebase.

## Features

- **Calendar Integration**: Sync with Google Calendar.
- **Email Integration**: Automatically read emails from Gmail and Microsoft Outlook to understand meeting requests.
- **Optimal Scheduling**: Consider participants' preferences and availability.
- **Reminders and Follow-ups**: Send reminders for upcoming meetings and schedule follow-ups.
- **Meeting Room Booking**: Automatically book available meeting rooms.

## Technologies

- **Backend**: Flask, SQLAlchemy, Flask-Migrate
- **AI/ML**: TensorFlow, Keras, NLP with SpaCy and NLTK
- **Database**: PostgreSQL
- **Task Queue**: Celery with Redis

## Project Structure

- Organized into modules using Blueprints for scalability.
- Implements CRUD operations for user and meeting management.
- Includes migration scripts to manage database schema changes.

### Prerequisites

- Python 3.7+
- PostgreSQL
- Redis
